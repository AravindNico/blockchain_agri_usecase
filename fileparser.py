import ConfigParser

class ConfigFileParser:
	def __init__(self):
		self.Config = ConfigParser.ConfigParser()

	def ConfigSectionMap(self,section):
	    dict1 = {}
	    options = self.Config.options(section)
	    for option in options:
	        try:
	            dict1[option] = self.Config.get(section, option)
	            if dict1[option] == -1:
	                DebugPrint("skip: %s" % option)
	        except:
	            print("exception on %s!" % option)
	            dict1[option] = None
	    return dict1
	
	def parseConfig(self,Filename):
		self.parseDict = {}	
		self.Config.read(Filename)

		field = self.Config.sections()[0]
		self.parseDict = self.ConfigSectionMap(field)
		
		# return self.parseDict.keys()
				# or
		return self.parseDict

	def getConfig(self,fieldname):
		if self.parseDict.has_key(fieldname):
			return self.parseDict[fieldname]
		else:
			return None

