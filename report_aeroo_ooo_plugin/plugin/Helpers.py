#### usefull helpers ####
#taken from http://user.services.openoffice.org/en/forum/viewtopic.php?f=44&t=19202#p87686
 
import uno
import unohelper
import sys,os
from com.sun.star.connection import NoConnectException
from com.sun.star.beans import PropertyValue
 
class OOoTools:
    '''Frequently used methods in office context'''
    def __init__(self, ctx=uno.getComponentContext()):
        self.ctx = ctx
        self.smgr = self.ctx.ServiceManager
       
    def createUnoService(self, service):
        return self.smgr.createInstance(service)
 
    def getOOoSetupNode(self, sNodePath):
        aConfigProvider = self.createUnoService("com.sun.star.configuration.ConfigurationProvider")
        arg = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
        arg.Name = "nodepath"
        arg.Value = sNodePath
        return aConfigProvider.createInstanceWithArguments("com.sun.star.configuration.ConfigurationAccess", (arg,))
 
    def getOOoSetupValue(self, sNodePath,sProperty):
        oNode = self.getOOoSetupNode(sNodePath)
        return oNode.getByName(sProperty)
 
    def setOOoSetupValue(self, sNodePath, sProperty, sValue):
        xconfig = self.createUnoService("com.sun.star.configuration.ConfigurationProvider")
        arg = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
        arg.Name = "nodepath"
        arg.Value = sNodePath
        try:
            xAccess = xconfig.createInstanceWithArguments("com.sun.star.configuration.ConfigurationUpdateAccess",(arg,))
            xAccess.setPropertyValue(sProperty, sValue)
            xAccess.commitChanges()
        except:
            return False
        else:
            return True
