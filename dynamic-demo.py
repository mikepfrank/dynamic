#|==============================================================================
#|                      TOP OF FILE:    dynamic-demo.py
#|------------------------------------------------------------------------------
#|
#|      FILE NAME:  dynamic-demo.py         [Python application source code]
#|
#|      Initial development platform:
#|
#|          * Language:     Python 3.5.1 64-bit
#|          * OS:           Microsoft Windows 8.1 Professional (64-bit)
#|          * Processor:    Intel Xeon E5-2620 (64-bit)
#|
#|      Revision history:
#|
#|          6/21/16 (M. Frank) - Started writing initial version.
#|
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

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
RAW_DEBUG = True    # Turn it on temporarily during initial development.

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
        
from sys import stderr

        #|================================================
	#|   Imports of our own custom modules.
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

if __name__ == "__main__": 
    if RAW_DEBUG:
        print("__main__: Importing custom application modules...", file=stderr)

from exampleNetworks import ExampleNetwork_MemCell
    # The exampleNetworks module defines various simple example modules to be
    # used for development and testing.  ExampleNetwork_MemCell is a minimally-
    # simple example network to be used for initial development purposes.

    #|==========================================================================
    #|
    #|   Globals					    [code section]
    #|
    #|      Declare and/or define various global variables and
    #|      constants.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

# These top-level global declarations verify that these names were
# not previously used, and also serve as documentation.

global  is_top

    #|==========================================================================
    #|
    #|   Module-level function definitions.                   [code section]
    #|
    #|
    #|       These functions are not part of any particular class.
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|
        #|   _main()                                [module private function]
        #|
        #|      Main routine of module.
        #|
        #|      This routine is traditionally called within a module's main
        #|      body code, within the context of a conditional like
        #|
        #|           if __name__ == "__main__":
        #|
        #|      so it won't be automatically executed when this module is only
        #|      being imported as a sub-module of a larger system.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def _main():
    
    if RAW_DEBUG:
        print("__main__.main(): Entered application's main routine...",
              file=stderr)

    # Fill in main code of application below...

        # Create an extremely simple example network for initial
        # testing during development.
        
    net = ExampleNetwork_MemCell()
    
    net.test()  # This method exercises some basic simulation capabilities.
    
    if RAW_DEBUG:
        print("__main__.main(): Exiting from main()...", file=stderr)

#--/ End function main().

    #|==========================================================================
    #|
    #|   Main script body.                                   [code section]
    #|
    #|      Above this section should only be definitions and
    #|      assignments.  Below is the main executable body of
    #|      the script.  It just calls the main() function (if
    #|      this script is not just being loaded as a submodule).
    #|  
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    

if __name__ == "__main__":
    
    is_top = True   # For benefit of stuff called from within _main().

    if RAW_DEBUG:
        print("__main__: Top-level module is invoking main() routine of " +
              "application...", file=stderr)
        
    _main()
    
    if RAW_DEBUG:
        print("__main__: Application's main() routine has exited.",
              file=stderr)
        print("__main__: Exiting top-level module...",
              file=stderr)
        
else:
    
    if RAW_DEBUG:
        print("Finished recursive import of top-level module...")

#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#|                      END OF FILE:    dynamic-demo.py
#|==============================================================================
