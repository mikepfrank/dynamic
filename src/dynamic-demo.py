#|==============================================================================
#|                      TOP OF FILE:    dynamic-demo.py
#|------------------------------------------------------------------------------
#|   The below module documentation string will be displayed by pydoc3.
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""
    FILE NAME:      dynamic-demo.py         [Python application source code]

    FULL PATH:      $GIT_ROOT/dynamic/dynamic-demo.py

    MASTER REPO:    git@gitlab.sandia.gov:mpfrank/dynamic.git

    SYSTEM NAME:    Dynamic (simulator for dynamic networks)

    APP NAME:       Dynamic.demo (Dynamic demonstration application)


    DESCRIPTION:
    ------------

          This Python script (intended to be run at top level,
          not imported as a module) implements the demonstration
          application for the Dynamic simulator framework.  See
          the README.md file in this directory for more detailed
          information about the Dynamic system in general.


    Initial development platform:
    -----------------------------

          * Language:     Python 3.5.1 64-bit
          * OS:           Microsoft Windows 8.1 Professional (64-bit)
          * Processor:    Intel Xeon E5-2620 (64-bit)


    Copyright Notice
    ----------------

          This file, and all other files in this repository, are
          copyright (C) 2016 by Michael P. Frank.  All Rights
          Reserved until further notice.


    Revision history:
    -----------------

          6/21/16 (M.P. Frank) - Started writing initial version.
          10/6/16 (MPF) - At this point, full-adder demo works.  No GUI yet.
                                                                            """
#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#| End of module documentation string.
#|------------------------------------------------------------------------------


    #|--------------------------------------------------------------------------
    #|
    #|      RAW_DEBUG:bool                             [module global parameter]
    #|
    #|          Raw debugging flag.  This is a very low-level
    #|          facility, preliminary to any more sophisticated
    #|          error-logging capability.  Just check this flag
    #|          before doing low-level diagnostic output.  This
    #|          allows all such diagnostic output to be
    #|          suppressed easily.
    #|
    #|          Please note that this is the only global that
    #|          appears before the "Globals" code section, so
    #|          that we can begin using it right away.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global  RAW_DEBUG   # Declare this to be a module-level global.

RAW_DEBUG = False   # Change this to True as needed during initial development.

    # Conditionally display some initial diagnostics if RAW_DEBUG is on...

if RAW_DEBUG:
    print("Turned on raw debugging...")

if __name__ == "__main__":
    if RAW_DEBUG:
        print("__main__: Loading dynamic-demo.py...")


    #|==========================================================================
    #|
    #|   1. Module imports.                                [module code section]
    #|
    #|          Load and import names of (and/or names from) various
    #|          other python modules and pacakges for use from within
    #|          the present module.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|  1.1. Imports of standard python modules.    [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

if __name__ == "__main__":
    if RAW_DEBUG:
        print("__main__: Importing standard Python library modules...")

import sys        
from sys import stderr      # Used for error output to console.


        #|======================================================================
        #|  1.2. Imports of custom application modules. [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

if __name__ == "__main__": 
    if RAW_DEBUG:
        print("__main__: Importing custom application modules...", file=stderr)

    #|----------------------------------------------------------------
    #|  The following modules, although custom, are generic utilities,
    #|  not specific to the present application.

from logmaster import (appLogger, configLogMaster, setComponent,
                       setThreadRole, doInfo, doNorm, updateStderr)
    #   \
    #   The logmaster module defines our logging framework; we import
    #   some definitions that we need from it (configLogMaster, appLogger,
    #   setThreadRole, doInfo, doNorm).  Cleaner than import *.

    #|----------------------------------------------------------------
    #|  The following modules are specific to the present application.

from appdefs                        import  appName
    # Name of the present application.  Used for configuring logmaster.

from simulator.simmor               import  Simmor
    # Manages the whole simulation.

    #--------------------------------------
    # Import GUI modules we're using here.

from    gui         import guiapp, tikiterm, dyngui, worklist


    #|==========================================================================
    #|
    #|  2.  Global constants, variables, and objects.      [module code section]
    #|
    #|          Declare and/or define various global variables and
    #|          constants.  Top-level global declarations are not
    #|          strictly required, but they serve to verify that
    #|          these names were not previously used, and also
    #|          serve as documentation.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|
        #|  2.1.  Special globals.                      [module code subsection]
        #|
        #|          These globals have special meanings defined by the
        #|          Python language.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global  __all__         # List of public symbols exported by this module.

__all__ = ['is_top']    # Boolean; is this module running at top level?


        #|======================================================================
        #|
        #|   2.2.  Public module globals.               [module code subsection]
        #|
        #|      These are the globals specific to this module that we
        #|      encourage other modules to access and utilize.
        #|
        #|      The documentation for these should be included in the
        #|      module documentation string at the top of this file.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global  is_top      # Boolean; is this module running at top level?


        #|======================================================================
        #|
        #|  2.3.  Private globals.                      [module code subsection]
        #|
        #|          In this section, we define global variables that
        #|          are used within this module, but that are not
        #|          exported nor intended to be used by other modules.
        #|
        #|          Since these are private, they aren't documented
        #|          in the module's documentation string.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    # The logmaster-based logger object that we'll use for logging
    # within this module.  Initialized in _main().
    
global  _logger

global  _guibot

    #|==========================================================================
    #|
    #|  3.  Module-level function definitions.             [module code section]
    #|
    #|          These functions are defined at top level within the
    #|          module; they are not part of any particular class.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def _initLogging():
    global _logger
    
        #---------------------------------
        # Configure the logging facility.

    if RAW_DEBUG:
        print("__main__._initLogging(): Configuring the 'logmaster' logging module...",
              file=stderr)

    # Uncomment the first line below and comment the second to turn on
    # log-file debug messages.
    
    configLogMaster(logdebug = True, role = 'startup', component = appName)
    #configLogMaster(role = 'startup', component = appName)
        # Configure the logger with default settings (NORMAL and higher
        # output to console, INFO and higher to log file), set this main
        # thread's role to "startup" and set the thread component to
        # "demoApp".

    _logger = appLogger  # Get our application logger.


def _initGui():
    global _guibot
    
            #|====================================================
            #|  The following code initializes the GUI framework.

        #-------------------------------------------------------------
        # Declares (in the log file) that we are now working on behalf
        # of the GUI component.

    setComponent('GUI')

        #-------------------------------------------------------------
        # Create & start the guiapp module's guibot worker thread.
        # (This is done after the above b/c it may produce debug log
        # messages.)

    if doInfo:
        _logger.info("Starting the GUI application's worker thread...")

    guiapp.initGuiApp()         # This creates the guibot, in guiapp.guibot.
    _guibot = guiapp.guibot     # Private global copy in this module.

        #-------------------------------------------------------------    
        # Create our main terminal window for interactive standard I/O
        # to user.  This must be done after the call to initGuiApp().

    if doInfo:
        _logger.info("Creating new GUI-based console window...")

    console = tikiterm.TikiTerm(title="Dynamic Demo Console",
                                width=120, height=35)
        # Note the window size of 90x30 chars is a bit bigger than a
        # standard 80x24 console.  This is big enough to show our
        # splash logo and some text below it.

    if doInfo:
        _logger.info("Redirecting stdout & stderr streams to "
                     "GUI-based console...")

        #|--------------------------------------------------------------------------
        #|  Display a message in the default console window to explain to the
        #|  user the status of this now mostly-superfluous window.  Note this
        #|  is the last thing that is done before stdout is redirected.

    if doNorm:        
        print("\n"
              "You may now minimize this console window; "
              "it's no longer needed.\n"
              "NOTE: Closing this window will kill the %s application.\n"
              % appName)

        #-------------------------------------------------------------
        # Before we actually reassign stdin/stdout/stderr streams to 
        # use our new console, we first make sure we have a record of
        # our original stdin/stdout/stderr streams (if any), so we can
        # restore them later if/when the console window closes.

    # If the default stdout is not already set (e.g. we're running under IDLE),
    if sys.__stdout__ == None:   
        sys.__stdout__ = sys.stdout     # Set it to our actual current stdout.
        
    if sys.__stderr__ == None:          # Likewise with stderr.
        sys.__stderr__ = sys.stderr
        
    if sys.__stdin__  == None:          # And also stdin.
        sys.__stdin__  = sys.stdin


        #-------------------------------------------------------------
        # Have our new console take over the stdin, stdout and stderr
        # stream functions.       

    console.grab_stdio()
    updateStderr()  # Tells logmaster we have a new stderr now.
        # ^- Without this, we could not see abnormal log messages on
        #    our new console.

        #----------------------------------------------
        # Display splash logo image in console window.
        
    _guibot(lambda:dyngui.setLogoImage(console))
    print() # This just ends the line that the image is on.

        # OK, GUI-related initial setup is done.  

def _waitGuiEnd():      # Wait for the user to exit the GUI.
    _guibot.join()


        #|----------------------------------------------------------------------
        #|
        #|   _main()                                [module private function]
        #|
        #|      Main routine of this module.  It is private; we do not
        #|      export it, and other modules should not attempt to call it.
        #|
        #|      The _main() routine is traditionally called within a
        #|      module's main body code, within the context of a
        #|      conditional like
        #|
        #|           if __name__ == "__main__":
        #|
        #|      so that it won't be automatically executed when this module
        #|      is only being imported as a sub-module of a larger system.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def _main():
    """Main routine of the dynamic-demo.py script.  Called from within
        the script's main body code, if the script is run at top level
        as opposed to being imported as a module of a larger system."""
    
    if RAW_DEBUG:
        print("__main__._main(): Entered application's _main() routine...",
              file=stderr)

    _initLogging()      # Configure the logmaster module.

        #----------------------------------------------
        # Application startup:  Display splash text.

    if doInfo: _logger.info("Dynamic demo application is starting up...")

    if doNorm:
        print() # Just visual whitespace; no need to log it.
        _logger.normal("Welcome to the Dynamic demo program, v0.1.")
        _logger.normal("Copyright (c)2016 by Michael P. Frank.")
        _logger.normal("All Rights Reserved.")
        print()


    _initGui()  # Initialize the graphical user interface.
    
            #=====================================================
            # Below follows the main code of the demo application.

        #---------------------------------------------------------------
        # Create a "simmor" object, which will create, run and manage
        # simulations for us.

    simmor = Simmor()

        #-----------------------------------------------------------------
        # Tell the simmor to do a simple default demonstration of the
        # simulator's capabilities.

    simmor.doDemo()
    
    setComponent('appName')

        #------------------------------------------------------------
        # At this point we have nothing left to do, so we join with
        # the guibot thread and wait for the user to exit the GUI.
        # Better would be to run a command-processing loop reading
        # user commands from stdin.

    setThreadRole('waiting')
    _waitGuiEnd()

    setThreadRole('shutdown')

    if doNorm:
        _logger.normal("Dynamic demo application is shutting down...")

            # End of main code of demo application.
            #=======================================
    
    if RAW_DEBUG:
        print("__main__._main(): Exiting from _main()...", file=stderr)

#--/ End function main().


    #|==========================================================================
    #|
    #|   4.  Main script body.                             [script code section]
    #|
    #|          Above this section should only be definitions and
    #|          assignments.  Below is the main executable body of
    #|          the script.  It just calls the main() function (if
    #|          this script is not just being loaded as a submodule).
    #|  
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

is_top = (__name__ == "__main__")
    # Remember this for benefit of stuff called from within _main().
           
if is_top:
    
    if RAW_DEBUG:
        print("__main__: Top-level module is invoking _main() routine of " +
              "application...", file=stderr)
        
    _main()     # Call the private _main() function, defined above.
    
    if RAW_DEBUG:
        print("__main__: Application's _main() routine has exited.",
              file=stderr)
        print("__main__: Exiting top-level module...",
              file=stderr)
        
else:
    
    if RAW_DEBUG:
        print("Finished recursive import of top-level module...")

#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#|                      END OF FILE:    dynamic-demo.py
#|==============================================================================
