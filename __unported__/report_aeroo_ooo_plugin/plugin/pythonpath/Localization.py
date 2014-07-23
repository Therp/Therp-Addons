###########################################################################
# A homebuilt localization system.
#
# Taken from the EuroOffice Extensions Creator https://launchpad.net/eoec/,
# which seems to be based on Danny Brewer's work in the OpenOffice forum.
# http://www.oooforum.org/forum/viewtopic.phtml?t=14552,
#
# FWIW Danny preferred LGPL, EOEC is GPL3.
#
###########################################################################

import os
import glob
import sys
import uno
import unohelper

def typednamedvalues( type, *args, **kwargs ):
    if args:
        dict = args[0]
    else:
        dict = kwargs
    props = []
    for k, v in dict.items():
        p = uno.createUnoStruct( type )
        p.Name = k
        p.Value = v
        props.append( p )
    return tuple( props )

def props( *args, **kwargs ):
    return typednamedvalues( 'com.sun.star.beans.PropertyValue', *args, **kwargs )

class LocalizedObject(unohelper.Base):
    def initpath( self ):
        path = self.config.Origin
        expander = self.ctx.getValueByName( '/singletons/com.sun.star.util.theMacroExpander' )
        path = expander.expandMacros( path )
        path = path[len( 'vnd.sun.star.expand:' ):]
        path = unohelper.absolutize( os.getcwd(), path )
        path = unohelper.fileUrlToSystemPath( path )
        self.path = path

    def __init__( self, *args ):
        # store the component context for later use
        self.SUPPORTED_LANGUAGES = [
            'en',
            'nl',
            ]
        try:
            self.ctx = args[0]
            self.config = self.getconfig('org.openerp.OpenERPOptions/ConfigNode')
            self.initpath()
            self.initlanguage()
        except Exception, e:
            print >> sys.stderr, e

    def getconfig( self, nodepath, update = False ):
        if update:
            update = 'Update'
        else:
            update = ''
        psm = self.ctx.ServiceManager
        configprovider = psm.createInstance( 'com.sun.star.configuration.ConfigurationProvider' )
        configaccess = configprovider.createInstanceWithArguments( 'com.sun.star.configuration.Configuration%sAccess'%update, props( nodepath = nodepath ) )
        return configaccess

    def initlanguage( self ):
        config = self.getconfig( '/org.openoffice.Setup' )
        self.uilanguage = config.L10N.ooLocale.encode( 'ascii' ).split( '-' )[0]
        if self.uilanguage not in self.SUPPORTED_LANGUAGES:
            self.uilanguage = self.SUPPORTED_LANGUAGES[0]

    def localize( self, string, language = None ):
        if language is None:
            language = self.uilanguage
        if not hasattr( self, 'localization' ):
            try:
                self.loadlocalization()
            except Exception, e:
                print e
        print string
        if string not in self.localization: return 'unlocalized: %s' % string
        print language
        if language in self.localization[string]:
            return self.localization[string][language]
        elif self.SUPPORTED_LANGUAGES[0] in self.localization[string]:
            return self.localization[string][self.SUPPORTED_LANGUAGES[0]]
        return 'unlocalized for %s: %s'%(language, string)
        
    def loadlocalization( self ):
        self.localization = {}
        try:
            path = os.path.join(
		    self.path,
                    'Dialogs',
                    self.__class__.__name__
                    )
	    for f in glob.glob(os.path.join(path, 'DialogStrings_*.properties')):
                    print >> sys.stderr, f
		    sf = os.path.split( f )[-1]
		    lang = sf[sf.index( '_' )+1:sf.index( '_' )+3]
		    for l in file( f ):
			    l = l.split( '#' )[0].strip()
			    if len( l ) == 0: continue
			    assert '=' in l
			    key, value = l.split( '=', 1 )
			    key = key.strip()
			    value = value.strip()
			    if key not in self.localization:
				    self.localization[key] = {}
			    self.localization[key][lang] = value.decode( 'unicode_escape' ).replace( '\\', '' )
        except Exception, e:
            print >> sys.stderr, e

# uno implementation
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    LocalizedObject, "org.openerp.LocalizedObject",
    ("org.openerp.LocalizedObject",),)
