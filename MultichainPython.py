import Savoir
import simplejson as json
import logging


LOG_FILENAME = 'MultichainPython.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s, %(levelname)s, %(message)s', datefmt='%Y-%m-%d %H:%M:%S')




class Multichainpython:

	def __init__(self,rpcuser,rpcpasswd,rpchost,rpcport,chainname):
		self.rpcuser = rpcuser
		self.rpcpasswd = rpcpasswd
		self.rpchost = rpchost
		self.rpcport = rpcport
		self.chainname = chainname

	'''****************************************************************************************
	Function Name 	:   multichainConnect
	Description		:	Function used to make api call to connect to chain
	Parameters 		:	None
	****************************************************************************************'''		
	def multichainConnect(self):
		try:
			# The api connection 
			self.api = Savoir.Savoir(self.rpcuser, self.rpcpasswd, self.rpchost, self.rpcport, self.chainname)
			return self.api
		except Exception as e:
			logging.error("The multichainConnect error %s,%s"%(e,type(e)))
			return False
	'''****************************************************************************************
	Function Name 	:   gettotalbalances
	Description		:	Function used to make api call to get the asset total balances in the node
	Parameters 		:	None
	****************************************************************************************'''
	def gettotalbalances(self):
		try:
		    totalbalances = self.api.gettotalbalances()
		    return totalbalances
		except Exception as e:
		    print e
		    return False
	def getburnaddress(self):
		try:
			burnaddress = self.api.getinfo()["burnaddress"]
			return burnaddress
		except Exception as e:
			print e
			return False	    
	'''****************************************************************************************
	Function Name 	:   accountAddress
	Description		:	Function used to make api call to get the address of the node
	Parameters 		:	None
	****************************************************************************************'''
	def accountAddress(self):
		try:
			accountaddress = self.api.getaddressesbyaccount("")[0]
			return accountaddress
		except Exception as e:
			logging.error("The accountAddress error %s,%s"%(e,type(e)))
			return False
	'''****************************************************************************************
	Function Name 	:   sendAsset
	Description		:	Function used to make api call to issue asset for a node
	Parameters 		:	assetaddress      - address of the node that we are issueing asset				 
						assetdetails      - name of the asset and other details
						assetquantity     - quantity of the asset that we are issueing
						assetunit         - units of the asset
						assetnativeamount - -
						assetcustomfield  - metadata regarding the asset
	****************************************************************************************'''
	def issueAsset(self,assetaddress,assetdetails,assetquantity,assetunit,assetnativeamount,assetcustomfield):
		try:
			issueasset = self.api.issue(assetaddress,assetdetails,assetquantity,assetunit,assetnativeamount,assetcustomfield)
			return issueasset
		except Exception as e:
			logging.error("The issueAsset error %s,%s"%(e,type(e)))	
			return False
	'''****************************************************************************************
	Function Name 	:   issueMoreAsset
	Description		:	Function used to make api call to issue more asset of an existing asset
	Parameters 		:	assetaddress      - address of the other node where we are sending the asset				 
						assetname         - name of the asset that we are sending
						assetcustomfield  - metadata regarding the asset 
	****************************************************************************************'''
	def issueMoreAsset(self,assetaddress,assetname,assetcustomfield):
		try:
			issueassetmore = self.api.issuemore(assetaddress,assetname,0,0,assetcustomfield)
			return issueassetmore
		except Exception as e:
			logging.error("The issueMoreAsset error %s,%s"%(e,type(e)))		
			return False

	'''****************************************************************************************
	Function Name 	:   sendAsset
	Description		:	Function used to make api call to send an asset to other nodes
	Parameters 		:	assetaddress   - address of the other node where we are sending the asset				 
						assetname      - name of the asset that we are sending
						assetquantity  - quantity of the asset that we are sending
	****************************************************************************************'''
	def sendAsset(self,assetaddress,assetname,assetquantity):
		try:
			sendasset = self.api.sendassettoaddress(assetaddress,assetname,assetquantity)
			return sendasset
		except Exception as e:
			logging.error("The sendAsset error %s,%s"%(e,type(e)))			
			return False
	'''****************************************************************************************
	Function Name 	:   preparelockunspentexchange
	Description		:	Function used to make api to lock the asset quantity that we are using for exchange process
	Parameters 		:	asset            - name of the asset
	****************************************************************************************'''
	def preparelockunspentexchange(self,asset):
		try:
			preparelock = self.api.preparelockunspent(asset)
			return preparelock
		except Exception as e:
			logging.error("The preparelockunspentexchange error is %s,%s"%(e,type(e)))		
			return false
	'''****************************************************************************************
	Function Name 	:   createrawExchange
	Description		:	Function used to make api call to create an exchange process
	Parameters 		:	txid             - transction id that returned in the preparelockunspentexchange process					 
						vout             - vout that returned in the preparelockunspentexchange process default 0
						asset            - name of the asset
	****************************************************************************************'''
	def createrawExchange(self,txid,vout,asset):
		try:
			createexchange = self.api.createrawexchange(txid,vout,asset)
			return createexchange
		except Exception as e:
			logging.error("The createrawExchange error is %s,%s"%(e,type(e)))		
			return False

	'''****************************************************************************************
	Function Name 	:   decoderawExchange
	Description		:	Function used to make api call to confirms the exchange process
	Parameters 		:	createex_hexBlob - Hexblob returned in the createexchange process
	****************************************************************************************'''
	def decoderawExchange(self,createex_hexBlob):
		try:
			decodeexchange = self.api.decoderawexchange(createex_hexBlob)
			return decodeexchange
		except Exception as e:
			logging.error("The decoderawExchange error %s,%s"%(e,type(e)))		
			return False

	'''****************************************************************************************
	Function Name 	:   appendrawExchange
	Description		:	Function used to make api call to append the exchange with offer and ask assets
	Parameters 		:	createex_hexBlob - Hexblob returned in the createexchange process
						txid             - transction id that returned in the createexchange process					 
						vout             - vout that returned in the createexchange process default 0
						asset            - name of the asset
	****************************************************************************************'''
			
	def appendrawExchange(self,createex_hexBlob,txid,vout,asset):
		try:
			appendexchange = self.api.appendrawexchange(createex_hexBlob,txid,vout,asset)
			return appendexchange
		except Exception as e:
			logging.error("The appendrawExchange error %s,%s"%(e,type(e)))
			return False
	'''****************************************************************************************
	Function Name 	:   sendrawTransaction
	Description		:	Function used to make api call send the exchange process result to the chain
	Parameters 		:	appex_hexBlob - Hexblob that returned in the appendrawExchange process
	****************************************************************************************'''
	def sendrawTransaction(self,appex_hexBlob):
		try:
			sendexchange = self.api.sendrawtransaction(appex_hexBlob)
			return sendexchange
		except Exception as e:
			logging.error("The sendrawTransaction error %s,%s"%(e,type(e)))		
			return False
	
	# - ------- - - - - - -- Following functions are for querying the asset ---- - - - - 
	'''****************************************************************************************
	Function Name 	:   subscribeToasset
	Description		:	Function used to make api call to subscribe for an asset
	Parameters 		:	assetname - Name of the asset
	****************************************************************************************'''
	def subscribeToasset(self,assetname):
		try:
			subscrbtoasst = self.api.subscribe(assetname)
			return subscrbtoasst
		except Exception as e:
			logging.error("The subscribeToasset error %s,%s"%(e,type(e)))
			return False	
	'''****************************************************************************************
	Function Name 	:   queryAssetTransactions
	Description		:	Function used to make api call to get the asset transactions
	Parameters 		:	assetname - Name of the asset
	****************************************************************************************'''
	def queryAssetTransactions(self,assetname):
		try:
			queryassttrans = self.api.listassettransactions(assetname)
			return queryassttrans 
		except Exception as e:
			logging.error("The queryAssetTransactions error %s,%s"%(e,type(e)))		 
			return False
	'''****************************************************************************************
	Function Name 	:   queryassetdetails
	Description		:	Function used to make api call to get the asset details
	Parameters 		:	assetname - Name of the asset
	****************************************************************************************'''
	def queryassetsdetails(self,assetname):
		try:
			assetdetails = self.api.listassets(assetname,True) # Here True is for fetching full details its called verbose
			return assetdetails
		except Exception as e:
			logging.error("The queryassetdetails error %s,%s"%(e,type(e)))		
