#|=============================================================================
#|   appdefs.py                                  [python module source code]
#|
#|       Application-specific definitions.
#|
#|       This file defines some parameters specific to the present
#|       application.  It may be included from within general-
#|       purpose modules to customize those modules for this
#|       particular application.
#|
#|       At present, we are only using this to define <systemName>
#|       and <appName> parameters, which are used to compose names
#|       of system-specific and application-specific loggers.
#|
#|       E.g., the logger for a module or component that is specific
#|       to the system (but not to the particular application program)
#|       would be called "<systemName>.<othername>", whereas the logger
#|       for a module specific to the present application would be
#|       called "<appName>.<othername>".  Further, <appName> itself
#|       should begin with "<systemName>."
#|
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

__all__ = ['systemName',    # Name of the system this application is part of.
           'appName',       # Name of the current application program.
           'topFile'        # The filename of the top-level file of this app.
           ]

	#|===============================================================
	#|   Global variable definitions.                [code section]
	#|
	#|       User programs should do "from appdefs import *"
	#|       to get immediate copies of these globals.
	#|
	#|       If users wish to modify these globals, they must also
	#|       do "import appdefs" and then "appdefs.<global> = ..."
	#|       (Warning: This will not affect the values of these
	#|       globals seen by other modules that have already
	#|       imported this module!)
	#|
	#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global systemName, appName, topFile
    # Doesn't really do anything at top level.

        #|-----------------------------------------------------------------
        #|
        #|      systemName                      [global constant string]
        #|
        #|          This string gives the name of the overall
        #|          system that the present application is a
        #|          part of.  Lexically it should be a standard
        #|          identifier (alphanumeric string).
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

systemName  =   "Dynamic"       # This code is part of the "COSMICi" system.


        #|-----------------------------------------------------------------
        #|
        #|      appName                         [global constant string]
        #|
        #|          This string gives the name of the present
        #|          application (as a component of the overall
        #|          sytem).  It consists of the <systemName>
        #|          followed by a "." and an identifier
        #|          specifying this application (as distinct
        #|          from other components of the system).
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

appName     =   systemName + ".demo"
    #-This application program is the (main central) server component
    # of the system.

topFile = 'dynamic-demo'

#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#|  END FILE:   appdefs.py
#|=============================================================================
