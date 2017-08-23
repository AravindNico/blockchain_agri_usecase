import os
import sys
import Savoir
import simplejson as json
from pubnub import Pubnub

parentpath = os.path.dirname(os.getcwd())
sys.path.insert(0,parentpath)
from MultichainPython import Multichainpython
from fileparser import ConfigFileParser

# Farmland class

class Farmland:
	def __init__(self,rpcuser,rpcpasswd,rpchost,rpcport,chainname):
		print "Farmland"
		self.rpcuser = rpcuser
		self.rpcpasswd = rpcpasswd
		self.rpchost = rpchost
		self.rpcport = rpcport
		self.chainname = chainname
		self.mchain = Multichainpython(self.rpcuser,self.rpcpasswd,self.rpchost,self.rpcport,self.chainname)

	'''****************************************************************************************
	Function Name 	:   connectTochain
	Description		:	Function used to make api call to connect to chain
	Parameters 		:	None
	****************************************************************************************'''
	def connectTochain(self):
		return self.mchain.multichainConnect()  
	'''****************************************************************************************
	Function Name 	:   farmAddress
	Description		:	Function used to make api call to get the address of the node
	Parameters 		:	None
	****************************************************************************************'''
	def farmAddress(self):
		return self.mchain.accountAddress()
	'''****************************************************************************************
	Function Name 	:   assetsubscribe
	Description		:	Function used to make api call to subscribe for an asset
	Parameters 		:	None
	****************************************************************************************'''
	def assetsubscribe(self,asset):
		self.mchain.subscribeToasset(asset)
	'''****************************************************************************************
	Function Name 	:   assetbalances
	Description		:	Function used to make api call to get the asset total balances in the node
	Parameters 		:	None
	****************************************************************************************'''
	def assetbalances(self):
		assetbalances = self.mchain.gettotalbalances()
		return assetbalances	
	'''****************************************************************************************
	Function Name 	:   queryassetdetails
	Description		:	Function used to make api call to get the asset details
	Parameters 		:	None
	****************************************************************************************'''
	def queryassetdetails(self,asset):
		assetdetails = self.mchain.queryassetsdetails(asset)
		return assetdetails

	'''****************************************************************************************
	Function Name 	:   issueFSasset
	Description		:	Function to issue asset in a node
	Parameters 		:	None
	****************************************************************************************'''
	
	def issueFSasset(self): 
		try:
			# Getting the address of the present node.
		    assetaddress = self.mchain.accountAddress()
		    assetname = "crop" # name of the asset 
		    assetdetails = {"name":assetname,"open":True} # making asset open will able us to issuemore in future after creating the asset
		    assetquantity = 1000 # quantity of the asset to be created
		    assetunit = 1 # Units of the asset to be created
		    assetnativeamount =0
		    # custom fields - any metadata regarding the asset 
		    assetcustomfield ={"assetmetrics":"kgs",'croptemp':'27','crophumidity':'10','startdate':'2017-03-01','enddate':'2017-04-30',"asset-departuredate":'2017-05-05','owner':'Mark-Farmer'}
		    # api call to issue the asset.
		    issueFSasset_return = self.mchain.issueAsset(assetaddress,assetdetails,assetquantity,assetunit,assetnativeamount,assetcustomfield)
		    # subscribing to the asset
		    # To query the asset details we have to subscribe to that asset in the chain.
		    self.assetsubscribe(assetname)
		    
		    assetdescription = {"assetname":assetname,"assetquantity":assetquantity,"assetmetrics":"kgs","assetowner":"Mark-Farmer"}
		    message = {"op_return":issueFSasset_return,"assetdescription":assetdescription}
		    # publishing the response message to the UI.
		    publish_handler({"node":"farmland","messagecode":"issueasset","messagetype":"resp","message":message})
		except Exception as e:
		    print e,"erro in issueFSasset"
		    message = {"op_return":"error","message":e}
		    publish_handler({"node":"farmland","messagecode":"issueasset","messagetype":"resp","message":message})

	'''****************************************************************************************
	Function Name 	:   createExchange
	Description		:	Function to start the exchange procedure
	Parameters 		:	None
	****************************************************************************************'''

	def createExchange(self):
		
		try:
			# Here asset will be a dictionary ex: {"asset1":1}
			# Assets involving in the exchange process
			ownasset = {"crop":20} # offering asset
			otherasset = {"warehousemoney":20} # asking asset
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
					publish_handler({"node":"farmland","messagecode":"createexchange","messagetype":"resp","message":message})
				else:
					message = {"op_return":createex_return,"hexblob":""}
					publish_handler({"node":"farmland","messagecode":"createexchange","messagetype":"resp","message":message})						
			else:
				publish_handler({"node":"farmland","messagecode":"createexchange","messagetype":"resp","message":""})   
		except Exception as e:
			print e,"error in createExchange"
			publish_handler({"node":"farmland","messagecode":"createexchange","messagetype":"resp","message":"","error":e})       


	'''****************************************************************************************
	Function Name 	:   updateassetbalance
	Description		:	Function to update the asset balances in all the nodes
	Parameters 		:	None
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
			# Checking if asset balances api call returned success or not.
			if assetbalances !=False:    
			    # Iterating through the assets that are there now in the node.
			    for i in range(0,len(assetbalances)):
			        temp_dict.update({assetbalances[i]["name"]:assetbalances[i]["qty"]})
			        # Getting the full description regarding an asset.
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
			publish_handler({"node":"farmland","messagecode":"updateassetbalance","messagetype":"resp","message":message})
		except Exception as e:
			message = {"op_return":"error","message":e}
			publish_handler({"node":"farmland","messagecode":"updateassetbalance","messagetype":"resp","message":message})
            		print ("The updateassetbalances error",e)    


'''****************************************************************************************
Function Name 	:   pub_Init
Description		:	Function to intialize the pubnub
Parameters 		:	None
****************************************************************************************'''

def pub_Init(): 
	global pubnub
	try:
	    pubnub = Pubnub(publish_key=pub_key,subscribe_key=sub_key) 
	    pubnub.subscribe(channels=subchannel, callback=callback,error=error,
	    connect=connect, reconnect=reconnect, disconnect=disconnect)    
	    return True
	except Exception as pubException:
	    print("The pubException is %s %s"%(pubException,type(pubException)))
	    return False    

                        
'''****************************************************************************************
Function Name 	:   callback
Description		:	Function to receive the messages
Parameters 		:	message - The message that received
					channel - channel used to receiving messages
****************************************************************************************'''

def callback(message,channel):
	try:
		print message
		if message["messagetype"] == "req":
			if message["messagecode"] == "issueasset":
				FL.issueFSasset()
			if message["messagecode"] == "createexchange":
				FL.createExchange()
			if message["messagecode"] == "updateassetbalance":
				FL.updateassetbalance()
	except Exception as e:
		print("The callback exception is %s,%s"%(e,type(e)))            
		


'''****************************************************************************************
Function Name 	:   publish_handler
Description		:	Function to Publish the messages
Parameters 		:	message - The message to publish
****************************************************************************************'''
def publish_handler(message):
	try:
	    pbreturn = pubnub.publish(channel = pubchannel ,message = message,error=error)

	except Exception as e:
	    print ("The publish_handler exception is %s,%s"%(e,type(e)))

 

'''****************************************************************************************
Function Name 	:	error
Description		:	If error in the channel, prints the error
Parameters 		:	message - error message
****************************************************************************************'''                
def error(message):
    print("ERROR on Pubnub: " + str(message))
'''****************************************************************************************
Function Name 	:connect
Description		:	Responds if server connects with pubnub
Parameters 		:	message
****************************************************************************************'''    
def connect(message):
    print("CONNECTED")
'''****************************************************************************************
Function Name 		:	reconnect
Description		:	Responds if server connects with pubnub
Parameters 		:	message
****************************************************************************************'''
def reconnect(message):
	print("RECONNECTED")

'''****************************************************************************************
Function Name 		:	disconnect
Description		:	Responds if server disconnects from pubnub
Parameters 		:	message
****************************************************************************************'''
def disconnect(message):
	print("DISCONNECTED")
                
                



'''****************************************************************************************
Function Name 	:   __main__
Description		:	Program starts executing here
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
	pubchannel = cf.getConfig("pubchannel")  # channel to publish messages
	subchannel = cf.getConfig("subchannel")  # channel to receive messages

	# Multichain  Credentials
	rpcuser= cf.getConfig("rpcuser")
	rpcpasswd=cf.getConfig("rpcpasswd")
	rpchost = cf.getConfig("rpchost")
	rpcport = cf.getConfig("rpcport")
	chainname = cf.getConfig("chainname")

	# Initializing the Farmland class
	FL = Farmland(rpcuser,rpcpasswd,rpchost,rpcport,chainname)
	FL.connectTochain()
	# Initializing the pubnub
	pub_Init()








