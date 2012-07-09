#!
# -*- coding: utf-8 -*-
"""
Extension pour faciliter l'intégration du logiciel Coda.
Gestion de la fenêtre des options.

Copyright : Agence universitaire de la Francophonie
Licence : GNU General Public Licence, version 2
Auteur : Jean Christophe André
Date de création : juillet 2009

Adapted by Therp BV <http://therp.nl>
"""
import uno
import unohelper

# interfaces
from com.sun.star.lang import XServiceInfo
from com.sun.star.awt import XContainerWindowEventHandler

PROTOCOLS = ['XML-RPC', 'XML-RPC secure']

def log(msg):
    #TODO: some portable logging
    pass

PROTOCOLS = ['XML-RPC', 'XML-RPC secure']

protocol_map = {
    'XML-RPC': 'http://',
    'XML-RPC secure': 'https://',
    }  

# Global dictionary for the settings
options = {}

# Set True when options change
# Reset when options are requested
options_dirty = True

class ConfigurationProvider(object):
    def __init__(self, ctx):
        self.xConfig = ctx.ServiceManager.createInstanceWithContext( 
            "com.sun.star.configuration.ConfigurationProvider", ctx)
        self.node = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
        self.node.Name = "nodepath"
        self.node.Value = "/org.openerp.OpenERPOptions/OpenERPOptions"
        self.cfg_names = [
            "Server",
            "ServerPort",
            "ServerProtocol",
            "Database",
            "Username",
            "Password",
            ]
        global options
        options.update(self.configreader())

    # read configuration
    def configreader(self):
        settings = {}
        try:
            ConfigReader = self.xConfig.createInstanceWithArguments( 
                "com.sun.star.configuration.ConfigurationAccess",
                (self.node,))
            #cfg_values = ConfigReader.getPropertyValues(self.cfg_names)
            for name in self.cfg_names:
                cfg_value = ConfigReader.getByName(name)
                settings[name] = cfg_value
        except:
            pass
        return settings

    # write configuration, cfg_values: tuple
    # keep the order of the values
    def configwriter(self, cfg_values):
        try:
            ConfigWriter = self.xConfig.createInstanceWithArguments( 
                "com.sun.star.configuration.ConfigurationUpdateAccess",
                (self.node,))
            #ConfigWriter.setPropertyValues(self.cfg_names, cfg_values)
            for key, value in cfg_values.items():
                ConfigWriter.replaceByName(key, value)
            ConfigWriter.commitChanges()
        except Exception, e:
            log(e)

    def get_options(self):
        """ 
        Provide an interface to the options dictionary global
        to this file.
        Return a quintle(url, database, username, password, options_changed).
        Reset options_dirty, as the caller should reconnect if it receives a
        True value for options_changed.
        """
        global options_dirty
        url = (
            protocol_map.get(options.get('ServerProtocol'), False) and
            options.get('Server') and
            options.get('ServerPort') and
            "%s%s:%s" % (
                protocol_map.get(options.get('ServerProtocol')),
                options.get('Server'),
                options.get('ServerPort')
                )
            )
        log("options_dirty: %s" % options_dirty)
        res = (
            url,
            options.get('Database', False),
            options.get('Username', False),
            options.get('Password', False),
            options_dirty,
            )
        options_dirty = False
        return res

# main class
class OptionsHandler(unohelper.Base, XServiceInfo, XContainerWindowEventHandler):
    def __init__(self, ctx):
        self.ConfigurationProvider = ConfigurationProvider(ctx)

    # XContainerWindowEventHandler
    def callHandlerMethod(self, window, eventObject, method):
        if method == "external_event":
            try:
                self.handleExternalEvent(window, eventObject)
            except:
                pass
        return True

    # XContainerWindowEventHandler
    def getSupportedMethodNames(self):
        return ("external_event",)

    def supportsService(self, name):
        return False

    def getImplementationName(self):
        return "org.openerp.OptionsHandler"

    def getSupportedServiceNames(self):
        return ()

    def handleExternalEvent(self, window, eventName):
        if eventName == "ok":
            self.saveData(window)
        elif eventName == "back":
            self.loadData(window, "back")
        elif eventName == "initialize":
            self.loadData(window, "initialize")
        return True

    # load and set the data
    def loadData(self, window, ev):
        name = window.getModel().Name
        settings = self.ConfigurationProvider.configreader()
        if not settings:
            log("No settings, return")
            return
        for name in self.ConfigurationProvider.cfg_names:
            if name == 'ServerProtocol':
                seq = 0
                for proto in PROTOCOLS:
                    window.getControl(name).addItem(proto, seq)
                    seq += 1
            window.getControl(name).setText(settings.get(name, ''))
        return

    # making the save data
    def saveData(self, window):
        global options
        global options_dirty
        settings = {}
        for name in self.ConfigurationProvider.cfg_names:
            settings[name] = window.getControl(name).getText()
            if settings[name] != options.get(name):
                options[name] = settings[name]
                options_dirty = True
        self.ConfigurationProvider.configwriter(settings)
        return

# uno implementation
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    OptionsHandler, "org.openerp.OptionsHandler",
    ("org.openerp.OptionsHandler",),)
