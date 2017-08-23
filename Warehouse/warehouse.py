import os
import sys
import Savoir
import simplejson as json
from pubnub import Pubnub

parentpath = os.path.dirname(os.getcwd())
sys.path.insert(0,parentpath)
from MultichainPython import Multichainpython
from fileparser import ConfigFileParser

# Warehouse class
class Warehouse:
    def __init__(self,rpcuser,rpcpasswd,rpchost,rpcport,chainname):
        print "Warehouse"
        self.rpcuser = rpcuser
        self.rpcpasswd = rpcpasswd
        self.rpchost = rpchost
        self.rpcport = rpcport
        self.chainname = chainname
        self.mchain = Multichainpython(self.rpcuser,self.rpcpasswd,self.rpchost,self.rpcport,self.chainname)

    '''****************************************************************************************
    Function Name   :   connectTochain
    Description     :   Function used to make api call to connect to chain
    Parameters      :   None
    ****************************************************************************************'''
    def connectTochain(self):       
        return self.mchain.multichainConnect()
    '''****************************************************************************************
    Function Name   :   warehouseAddress
    Description     :   Function used to make api call to get the address of the node
    Parameters      :   None
    ****************************************************************************************'''
    def warehouseAddress(self):
        return self.mchain.accountAddress()
    '''****************************************************************************************
    Function Name   :   assetsubscribe
    Description     :   Function used to make api call to subscribe for an asset
    Parameters      :   None
    ****************************************************************************************'''
    def assetsubscribe(self,asset):
        self.mchain.subscribeToasset(asset)
    '''****************************************************************************************
    Function Name   :   assetbalances
    Description     :   Function used to make api call to get the asset total balances in the node
    Parameters      :   None
    ****************************************************************************************'''
    def assetbalances(self):
        assetbalances = self.mchain.gettotalbalances()
        return assetbalances
    '''****************************************************************************************
    Function Name   :   queryassetdetails
    Description     :   Function used to make api call to get the asset details
    Parameters      :   None
    ****************************************************************************************'''
    def queryassetdetails(self,assetname):
        assetdetails = self.mchain.queryassetsdetails(assetname)
        return assetdetails
    def getburnaddress(self):
        return self.mchain.getburnaddress()     
    def burnasset(self,address,asset_name,asset_qty):
        return self.mchain.sendAsset(address,asset_name,asset_qty)

    '''****************************************************************************************
    Function Name   :   issueWHasset
    Description     :   Function to issue asset in a node
    Parameters      :   None
    ****************************************************************************************'''
    def issueWHasset(self): 
        try:
            # Getting the address of the present node.
            assetaddress = self.mchain.accountAddress()
            
            self.assetname = "warehousemoney" # name of the asset
            assetdetails = {"name":self.assetname,"open":True} # making the asset open will able us to issuemore in future after creating the asset
            assetquantity = 1000  # quantity of the asset to be created
            assetunit = 1  # Units of the asset to be created
            assetnativeamount =0 
            # custom fields - any metadata regarding the asset 
            assetcustomfield = {'assetmetrics':'dollars','owner':'John-Distributor'}
            # api call to issue the asset
            issueWHasset_return = self.mchain.issueAsset(assetaddress,assetdetails,assetquantity,assetunit,assetnativeamount,assetcustomfield)
            assetdescription = {"assetname":self.assetname,"assetquantity":assetquantity,"assetmetrics":"dollars","assetowner":"John-Distributor"}
            # publishing the response message to the UI.
            message = {"op_return":issueWHasset_return,"assetdescription":assetdescription}
            
            self.assetsubscribe(self.assetname)
            publish_handler({"node":"warehouse","messagecode":"issueasset","messagetype":"resp","message":message})


        except Exception as e:
            print e,"error in issueWHasset"
            message = {"op_return":"error","message":e}
            publish_handler({"node":"warehouse","messagecode":"issueasset","messagetype":"resp","message":message})

    '''****************************************************************************************
    Function Name   :   createExchange
    Description     :   Function to start the exchange procedure
    Parameters      :   None
    ****************************************************************************************'''
        
    def createExchange(self):
        try:
            # Here asset will be a dictionary ex: {"asset1":1}
            # Assets involving in the exchange process
            ownasset = {"warehouse-crop":4} # offering asset
            otherasset = {"retailmoney":200} # asking asset
            # Step 1 - Locking the asset quantity that is for the exchange process
            prepare_return = self.mchain.preparelockunspentexchange(ownasset)
            print prepare_return
            if prepare_return != False or prepare_return.has_key("txid"):
                # Step 2 - Creating the raw exchange, involving the offer and asking assets
                createex_return = self.mchain.createrawExchange(prepare_return["txid"],prepare_return["vout"],otherasset)
                print createex_return
                # checking if createexchange api call success or not
                if type(createex_return) != dict:               

                    message = {"op_return":str(createex_return),"hexblob":str(createex_return)}
                    publish_handler({"node":"warehouse","messagecode":"createexchange","messagetype":"resp","message":message})
                else:
                    message = {"op_return":createex_return,"hexblob":""}
                    publish_handler({"node":"warehouse","messagecode":"createexchange","messagetype":"resp","message":message})                   
            else:
                publish_handler({"node":"warehouse","messagecode":"createexchange","messagetype":"resp","message":""})   
        except Exception as e:
            print e,"error in createExchange"
            publish_handler({"node":"warehouse","messagecode":"createexchange","messagetype":"resp","message":""})       

    '''****************************************************************************************
    Function Name   :   decodeExchange
    Description     :   Function to confirms the exchange process
    Parameters      :   None
    ****************************************************************************************'''
            

    def decodeExchange(self,hexBlob):
        # The following will give the details regarding the exchange
        try:    
            ownasset = {"warehousemoney":20} #asked asset
            otherasset = {"crop":20} # offered asset

            # --step1 decode the hexblob you got in the createexchange procedure
            decodedtranx =  self.mchain.decoderawExchange(hexBlob)
            if type(decodedtranx) == dict:
                if decodedtranx.has_key("offer") and decodedtranx.has_key("ask"):
                    # --step2
                    # We are locking the asset(ownasset)
                    prepare_return = self.mchain.preparelockunspentexchange(ownasset)
                    print prepare_return
                    if prepare_return != False:                
                        # --step3 
                        # Now we to do the appenexchange operation by giving hexblob and txid and otherasset 
                        append_return = self.mchain.appendrawExchange(hexBlob,prepare_return["txid"],prepare_return["vout"],otherasset)
                        print append_return
                        # -- step 4 
                        # This step is for sending the transaction details to the chain
                        if append_return["complete"] == True:
                            send_return = self.mchain.sendrawTransaction(append_return["hex"])
                            message = {"exchange_details":decodedtranx,"exchange_addedtochain":send_return} 
                    else:
                        message = {"exchange_details":False,"exchange_addedtochain":False} 
                else:
                    message = {"exchange_details":False,"exchange_addedtochain":False} 
            else:
                message = {"exchange_details":False,"exchange_addedtochain":False} 
                
            publish_handler({"node":"warehouse","messagecode":"decodeexchange","messagetype":"resp","message":message})         

        except Exception as e:
            message = {"exchange_details":False,"exchange_addedtochain":False} 
            publish_handler({"node":"warehouse","messagecode":"decodeexchange","messagetype":"resp","message":message})                            

    '''****************************************************************************************
    Function Name   :   convertasset
    Description     :   Function to do processing of the asset and burning the asset that is not required
    Parameters      :   None
    ****************************************************************************************'''           

    def convertasset(self):
        try:
            # step 1  - Getting the current asset balances
            # to get the names of the present assets in the node
            assetbalances = self.assetbalances()
            assetname = "warehousemoney"
            # Iterating through the result to find out the asset to be processed
            for i in range(0,len(assetbalances)):
                if assetbalances[i]["name"] != assetname:
                    self.convertasset_name = assetbalances[i]["name"]
                    self.convertasset_qty = assetbalances[i]["qty"]
                else:
                    message = {"op_return":False,"assetdescription":False,"burnasset_op_return":False}
            # step 2  - Getting the full details of an asset that is going to be converted.
            convertasset_details = self.queryassetdetails(self.convertasset_name)
            print convertasset_details
            # asset convertion process
            if len(convertasset_details) != 0:
                if convertasset_details[0].has_key("details"):
                    # giving a new name
                    convertedasset_name = "warehouse-crop"
                    assetdetails = {"name":convertedasset_name,"open":True} 
                    # giving new quantity for the asset
                    assetquantity = 4 
                    assetunit = 1 
                    assetnativeamount = 0
                    # Getting the node address
                    assetaddress = self.mchain.accountAddress()
                    # Updating the custom fields - meta data regarding the asset
                    assetcustomfield =convertasset_details[0]["details"]  
                    assetcustomfield.update({"assetmetrics":"packet(5 Kg)","origin":"farmland","owner":"John-Distributor","asset-arrivaldate":'2017-05-07',"asset-departuredate":'2017-05-10',"assetstorageconditions":"Good"}) 
                    issueWHasset_return = self.mchain.issueAsset(assetaddress,assetdetails,assetquantity,assetunit,assetnativeamount,assetcustomfield)
                    assetdescription = {"assetname":convertedasset_name,"assetquantity":assetquantity,"assetmetrics":"packet(5 kg)","assetowner":"John-Distributor"}

                    message = {"op_return":issueWHasset_return,"assetdescription":assetdescription}
                    print message
                    self.assetsubscribe(convertedasset_name)
                else:
                    message = {"op_return":False,"assetdescription":False,"burnasset_op_return":False}

            else:
                message = {"op_return":False,"assetdescription":False,"burnasset_op_return":False}

            # Step 3 - Process of sending the asset that is converted to the burnaddress of the chain
            # This will done after the conversion. 
            if message["op_return"] !=False:    
                # step 3.1 -  Get the chain's burn address
                burnaddress = self.getburnaddress()
                if burnaddress != False:
                    # Step 3.2 - api call to send the asset to the burn address.
                    burnasset_return = self.burnasset(burnaddress,self.convertasset_name,self.convertasset_qty)
                    message.update({"burnasset_op_return":burnasset_return})
                else:
                    message.update({"burnasset_op_return":burnasset_return})            

            else:
                message = {"op_return":False,"assetdescription":False,"burnasset_op_return":False}
            # publishing the response message to UI. 
            publish_handler({"node":"warehouse","messagecode":"convertasset","messagetype":"resp","message":message})	    
        except Exception as e:
            print e,"convertassetname" 
            message.update({"error":e})
            publish_handler({"node":"warehouse","messagecode":"convertasset","messagetype":"resp","message":message})            

    '''****************************************************************************************
    Function Name   :   updateassetbalance
    Description     :   Function to update the asset balances in all the nodes
    Parameters      :   None
    ****************************************************************************************'''
        
    def updateassetbalance(self):
        try:
            updateassetbalances_list = []
            assetdescription = {}
            temp_dict = {}
            # Getting the present total asset balances in the node.
            assetbalances = self.assetbalances()
            assetdetails = []
            print assetbalances
            # Checking if asset balances api call returned success or not
            if assetbalances !=False:    
                # Iterating through the assets that are there now in the node
                for i in range(0,len(assetbalances)):
                    temp_dict.update({assetbalances[i]["name"]:assetbalances[i]["qty"]})
                    # Getting the full description regarding an asset
                    assetdetails.append(self.queryassetdetails(assetbalances[i]["name"])[0])
                # Preparing the asset description 
                for j in range(0,len(assetdetails)):
                    assetdescription = {"assetquantity":temp_dict[assetdetails[j]["name"]],
                                "assetname":assetdetails[j]["name"],
                                "assetowner":assetdetails[j]["details"]["owner"],
                                "assetmetrics":assetdetails[j]["details"]["assetmetrics"]}
                    # update the list with the asset description 
                    updateassetbalances_list.append(assetdescription)
                print updateassetbalances_list
                message = {"op_return":updateassetbalances_list}
            else:                
                message = {"op_return":"error","message":""}
            # publish the message to the UI
            publish_handler({"node":"warehouse","messagecode":"updateassetbalance","messagetype":"resp","message":message})                        
        except Exception as e:
            message = {"op_return":"error","message":e}
            publish_handler({"node":"warehouse","messagecode":"updateassetbalance","messagetype":"resp","message":message})
            print ("The updateassetbalances error",e)    
'''****************************************************************************************
Function Name   :   pub_Init
Description     :   Function to intialize the pubnub
Parameters      :   None
****************************************************************************************'''
def pub_Init(): 
    global pubnub
    try:
        pubnub = Pubnub(publish_key=pub_key,subscribe_key=sub_key) 
        pubnub.subscribe(channels=subchannel, callback=callback,error=error,
        connect=connect, reconnect=reconnect, disconnect=disconnect)    
        return True
    except Exception as pubException:
        print ("The pubException is %s %s"%(pubException,type(pubException)))
        return False    

                        
'''****************************************************************************************
Function Name   :   callback
Description     :   Function to receive the messages
Parameters      :   message - The message that received
                    channel - channel used to receiving messages
****************************************************************************************'''

def callback(message,channel):
    try:
        print message
        if message["messagetype"] == "req":
            if message["messagecode"] == "issueasset":
                WH.issueWHasset()
            if message["messagecode"] == "createexchange":
                WH.createExchange()
            if message["messagecode"] == "decodeexchange":
                WH.decodeExchange(message["hexblob"])
            if message["messagecode"] == "convertasset":
                WH.convertasset()
            if message["messagecode"] == "updateassetbalance":
                WH.updateassetbalance()
    except Exception as e:
        print ("The callback exception is %s,%s"%(e,type(e)))           
    

'''****************************************************************************************
Function Name   :   publish_handler
Description     :   Function to Publish the messages
Parameters      :   message - The message to publish
****************************************************************************************'''
def publish_handler(message):

    try:
        pbreturn = pubnub.publish(channel = pubchannel ,message = message,error=error)

    except Exception as e:
        print ("The publish_handler exception is %s,%s"%(e,type(e)))


'''****************************************************************************************
Function Name   :   error
Description     :   If error in the channel, prints the error
Parameters      :   message - error message
****************************************************************************************'''                
def error(message):
    print ("ERROR on Pubnub: " + str(message))

'''****************************************************************************************
Function Name   :connect
Description     :   Responds if server connects with pubnub
Parameters      :   message
****************************************************************************************'''    
def connect(message):
    print ("CONNECTED")

'''****************************************************************************************
Function Name       :   reconnect
Description     :   Responds if server connects with pubnub
Parameters      :   message
****************************************************************************************'''
def reconnect(message):
    print ("RECONNECTED")
'''****************************************************************************************
Function Name       :   disconnect
Description     :   Responds if server disconnects from pubnub
Parameters      :   message
****************************************************************************************'''
def disconnect(message):
    print ("DISCONNECTED")


'''****************************************************************************************
Function Name   :   __main__
Description     :   Program starts executing here
****************************************************************************************'''
                
if __name__ == '__main__':
    pubnub = None   
    # config file name
    filename = "config.ini"
    cf = ConfigFileParser()     
    cf.parseConfig(filename)

    # PUBNUB KEYS
    pub_key = cf.getConfig("pubkey")
    sub_key = cf.getConfig("subkey")  

    # PUBNUB channels
    pubchannel = cf.getConfig("pubchannel") # channel to publish messages
    subchannel = cf.getConfig("subchannel") # channel to receive messages

    # Multichain  Credentials
    rpcuser= cf.getConfig("rpcuser")
    rpcpasswd=cf.getConfig("rpcpasswd")
    rpchost = cf.getConfig("rpchost")
    rpcport = cf.getConfig("rpcport")
    chainname = cf.getConfig("chainname")

    # Initializing the Warehouse class
    WH = Warehouse(rpcuser,rpcpasswd,rpchost,rpcport,chainname)
    WH.connectTochain()
    #Initializing the pubnub
    pub_Init()

