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

          6/21/16 (M. Frank) - Started writing initial version.
                                                                            """
#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#| End of module documentation string.
#|------------------------------------------------------------------------------

    #|--------------------------------------------------------------------------
    #|
    #|      RAW_DEBUG:bool                             [module global]
    #|
    #|          Raw debugging flag.  This is a very low-level
    #|          facility, preliminary to any more sophisticated
    #|          error-logging capability.  Just check this flag
    #|          before doing low-level diagnostic output.  This
    #|          allows all such diagnostic output to be
    #|          suppressed easily.
    #|
    #|          Please note that this is the only global that
    #|          appears before the "Globals" code sections, so
    #|          that we can begin using it right away.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global RAW_DEBUG    # Declare this to be a module-level global.
RAW_DEBUG = False   # Change this to True as needed during initial development.

if RAW_DEBUG:
    print("Turned on raw debugging...")

if __name__ == "__main__":
    if RAW_DEBUG:
        print("__main__: Loading dynamic-demo.py...")

    #|==========================================================================
    #|
    #|   Imports					    [code section]
    #|
    #|       Load and import names of (and/or names from) various
    #|       other python modules and pacakges for use from the
    #|       present module.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|=================================================
	#|   Imports of standard python library modules.
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

if __name__ == "__main__":
    if RAW_DEBUG:
        print("__main__: Importing standard Python library modules...")
        
from sys import stderr      # Used for error output to console.

        #|================================================
	#|   Imports of our own custom modules.
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

if __name__ == "__main__": 
    if RAW_DEBUG:
        print("__main__: Importing custom application modules...", file=stderr)

import  logmaster
from    logmaster   import configLogMaster,appLogger,info,normal
    # The logmaster module defines our logging framework; we import
    # several definitions that we need from it.

import  appdefs
from    appdefs     import appName
    # Name of the present application.  Used for configuring logmaster.

import  simulationContext
from    simulationContext   import SimulationContext
    # Used for tracking global state of the simulation.

import  exampleNetworks
from    exampleNetworks import ExampleNetwork_MemCell
    # The exampleNetworks module defines various simple example modules to be
    # used for development and testing.  ExampleNetwork_MemCell is a minimally-
    # simple example network to be used for initial development purposes.

    #|==========================================================================
    #|
    #|   Globals					    [code section]
    #|
    #|      Declare and/or define various global variables and
    #|      constants.  Top-level global declarations are not
    #|      strictly required, but they serve to verify that
    #|      these names were not previously used, and also
    #|      serve as documentation.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv


        #|======================================================================
        #|
        #|  Special globals.                                    [code section]
        #|
        #|      These globals have special meanings defined by the
        #|      Python language.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global  __all__         # List of public symbols exported by this module.
__all__ = ['is_top']    # Boolean; is this file running at top level?


        #|======================================================================
        #|
        #|  Module globals.                                    [code section]
        #|
        #|      These globals are specific to the present module.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global  is_top      # Boolean; is this module running at top level?

    #|==========================================================================
    #|
    #|   Module-level function definitions.                   [code section]
    #|
    #|      These functions are at top level within the module; 
    #|      they are not part of any particular class.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

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

    #---------------------------------
    # Configure the logging facility.

    if RAW_DEBUG:
        print("__main__._main(): Configuring the 'logmaster' logging module...",
              file=stderr)

    configLogMaster(loginfo = True, role = 'startup', component = appName)
        # Configure the logger to turn on log-file info output, set this
        # main thread's role to "startup" and set the thread component to
        # "demoApp".

    logger = appLogger  # Get our application logger.

    #----------------------------------------------
    # Application startup:  Display splash text.

    logger.info("Dynamic demo application is starting up...")

    print() # Just visual whitespace; no need to log it.
    logger.normal("Welcome to the Dynamic demo program, v0.1.")
    logger.normal("Copyright (c)2016 by Michael P. Frank.")
    logger.normal("All Rights Reserved.")
    print()

    #------------------------------------------------------
    # Below follows the main code of the demo application.

        #-----------------------------------------------------------------
        # First create a new simulation context object, initially empty.
        # This stores global parameters of the simulation (such as the
        # time delta value) and tracks global variables of the simulation
        # (such as the current time-step number).  We'll let it take its
        # default values for now.  At this point, the network to be
        # simulated has not been created yet.

    sc = SimulationContext()

        #---------------------------------------------------------
        # Create an extremely simple example network for initial
        # testing during development.  Tell it that it's going to
        # be using that simulation context that we just created.

    logger.normal("Creating an ExampleNetwork_MemCell instance...")                
    net = ExampleNetwork_MemCell(context=sc)

    logger.debug("Initial node q momentum is: %f" % 
                  net.node('q').coord.momentum.value)

        #---------------------------------------------------------
        # Run the built-in .test() method of the example network.

    logger.normal("Requesting simulator to run a simple test...")
    
    logmaster.setThreadRole('running')
    
    sc.test()  # This method exercises some basic simulation capabilities.

    logmaster.setThreadRole('shutdown')

    logger.normal("Dynamic demo application is shutting down...")

    # End of main code of demo application.
    #---------------------------------------
    
    if RAW_DEBUG:
        print("__main__._main(): Exiting from _main()...", file=stderr)

#--/ End function main().

    #|==========================================================================
    #|
    #|   Main script body.                              [script code section]
    #|
    #|      Above this section should only be definitions and
    #|      assignments.  Below is the main executable body of
    #|      the script.  It just calls the main() function (if
    #|      this script is not just being loaded as a submodule).
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
