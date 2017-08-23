import os
import sys
import Savoir
import simplejson as json
from pubnub import Pubnub

parentpath = os.path.dirname(os.getcwd())
sys.path.insert(0,parentpath)
from MultichainPython import Multichainpython
from fileparser import ConfigFileParser



# Retail store class 

class Retailstore:
    def __init__(self,rpcuser,rpcpasswd,rpchost,rpcport,chainname):
        print "Retailstore"
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
    Function Name   :   retailstoreAddress
    Description     :   Function used to make api call to get the address of the node
    Parameters      :   None
    ****************************************************************************************'''
    def retailstoreAddress(self):
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
    def queryassetdetails(self,asset):
        assetdetails = self.mchain.queryassetsdetails(asset)
        return assetdetails
        
    '''****************************************************************************************
    Function Name   :   issueRSasset
    Description     :   Function to issue asset in a node
    Parameters      :   None
    ****************************************************************************************'''
    
    def issueRSasset(self): 
        try:
            assetaddress = self.mchain.accountAddress()
            assetname = "retailmoney" 
            assetdetails = {"name":assetname,"open":True} # along withthat a unique timestamp will be added
            assetquantity = 1000 
            assetunit = 1 
            assetnativeamount =0 
            assetcustomfield = {'assetmetrics':'dollars','owner':'Peter-Retailer'}# will be generated based on sensor data, fields will be decided$
            issueRSasset_return = self.mchain.issueAsset(assetaddress,assetdetails,assetquantity,assetunit,assetnativeamount,assetcustomfield)
            assetdescription = {"assetname":assetname,"assetquantity":assetquantity,"assetmetrics":"dollars","assetowner":"Peter-Retailer"}
            
            message = {"op_return":issueRSasset_return,"assetdescription":assetdescription}
            
            self.assetsubscribe(assetname)
            publish_handler({"node":"retailstore","messagecode":"issueasset","messagetype":"resp","message":message})


        except Exception as e:
            print e,"error in issueHWasset"
            message = {"op_return":"error","message":e}
            publish_handler({"node":"retailstore","messagecode":"issueasset","messagetype":"resp","message":message})

    
    '''****************************************************************************************
    Function Name   :   decodeExchange
    Description     :   Function to confirm the exchange process
    Parameters      :   None
    ****************************************************************************************'''
            
    def decodeExchange(self,hexBlob):
        try:
            # The following will give the details regarding the exchange

            ownasset = {"retailmoney":200} #asked asset 
            otherasset = {"warehouse-crop":4} # offered asset

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
        
            publish_handler({"node":"retailstore","messagecode":"decodeexchange","messagetype":"resp","message":message})         
        except Exception as e:
            print e
            message = {"exchange_details":False,"exchange_addedtochain":False} 
            publish_handler({"node":"retailstore","messagecode":"decodeexchange","messagetype":"resp","message":message})                            

    
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
            # Getting the present total asset balancesin the node
            assetbalances = self.assetbalances()
            assetdetails = []
            print assetbalances
            # Checking if asset balances api call returned success or not
            if assetbalances !=False:
                # Iterating through the assets that are there in the node now.
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
            
            # publishing the message to the UI.
            publish_handler({"node":"retailstore","messagecode":"updateassetbalance","messagetype":"resp","message":message})                        
        except Exception as e:
            message = {"op_return":"error","message":e}
            publish_handler({"node":"retailstore","messagecode":"updateassetbalance","messagetype":"resp","message":message})
            print ("The updteassetbalances error",e)            

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
                    RS.issueRSasset()            
            if message["messagecode"] == "decodeexchange":
                    RS.decodeExchange(message["hexblob"])            
            if message["messagecode"] == "assetbalance":
                    RS.assetbalances()
            if message["messagecode"] == "updateassetbalance":
                    RS.updateassetbalance()        

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
    print("ERROR on Pubnub: " + str(message))

'''****************************************************************************************
Function Name   :connect
Description     :   Responds if server connects with pubnub
Parameters      :   message
****************************************************************************************'''    
def connect(message):
    print("CONNECTED")

'''****************************************************************************************
Function Name       :   reconnect
Description     :   Responds if server connects with pubnub
Parameters      :   message
****************************************************************************************'''
def reconnect(message):
    print("RECONNECTED")

'''****************************************************************************************
Function Name       :   disconnect
Description     :   Responds if server disconnects from pubnub
Parameters      :   message
****************************************************************************************'''
def disconnect(message):
    print("DISCONNECTED")


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

    # Initializing the Retailstore class
    RS = Retailstore(rpcuser,rpcpasswd,rpchost,rpcport,chainname)
    RS.connectTochain()
    # Inititalizing the pubnub
    pub_Init()

