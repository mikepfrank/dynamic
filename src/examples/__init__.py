#|==============================================================================
#|                  TOP OF FILE:    examples/__init__.py
#|------------------------------------------------------------------------------
#|   The below module documentation string will be displayed by pydoc3.
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""
    FILE NAME:          __init__.py         [Python package initialization file]

    FULL PATH:          $GIT_ROOT/dynamic/src/examples/__init__.py

    SYSTEM NAME:        Dynamic (simulator for dynamic networks)

    PACKAGE NAME:       examples

    COMPONENT NAME:     Dynamic.examples


    FILE DESCRIPTION:
    -----------------

        This Python file is the package-initialization module for
        the 'examples' package within the Dynamic software system.
        
        For general background on Python packages, see the comments
        within this file, or the online documentation at:
        [https://docs.python.org/3/tutorial/modules.html#packages].


    PACKAGE DESCRIPTION:
    --------------------

        The purpose of the 'examples' package is to define various
        examples of dynamic devices and networks for demonstration
        purposes.

        At present, the example devices include:

            (1) a simple adjustable (but otherwise read-only) "memory
                cell" device, which supplies a constant quadratic
                bias potential, and

            (2) a "range binder" device that supplies a double-well
                potential that is intended to keep logic values from
                drifting too far outside their nominal ranges.

        The example networks include networks for:

            (1) A single memory cell by itself;

            (2) A memory cell feeding a NOT gate (logical inverter);

            (3) Two memory cells feeding an AND gate;

            (4) Two memory cells feeding a half-adder circuit;

            (5) Three memory cells feeding a full-adder circuit.

        Additional example devices and networks may be added to the
        package over time.
    

    PACKAGE DEPENDENCIES:
    ---------------------

        The examples package uses the boolean package, and is used by
        the simulator package.
        
    
    MODULE HIERARCHY:
    -----------------

        The approximate hierarchy of modules within this package (also
        shown in the package's README.md file) is as follows:


			 _______________
	Package 	/               \\
	module:		|    examples   |
			| (__init__.py) |
			\_______________/
	Modules in	    |	    |
	package:	    |	    |
			    |	    V
			    |	exampleNetworks.py
			    |		|
			    V		V
		 rangeBinder.py	  dynamicMemCell.py
        
                                                                             """
#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#| End of module documentation string for examples/__init__.py.
#|------------------------------------------------------------------------------

# examples/__init__.py - Initialization for the examples package.

# When a package's __init__.py file is loaded, the namespace is pre-loaded
# with the attribute __path__ which contains the full filesystem path to the 
# package's directory, which in this case the the "examples/" subdirectory
# of the top-level source directory for the Dynamic system.

# Then the package may define __all__, which is a list of the module names
# that would be imported if the user did "from <package> import *".

# However, the preferred way to import modules from a package is one at a
# time, as in "from <package> import <module>", or you can also import
# specific module attributes like "from <package>.<module> import <attr>".

# Modules can import other modules in the same package using the syntax,
# "from .<module> import <attr>" and from other modules in sibling packages
# using syntax like "from ..<package> import <module>".

__all__ = [
    'dynamicMemCell',
    'rangeBinder',
    'exampleNetworks'   # split out halfadder, fulladder etc.
    ]

#print("__path__ is %s" % __path__)

    # Create a logger for this package (as a software component).

from logmaster import *

_component = __path__[0].split('\\')[-1]    # Component name = package name.
_logger = getComponentLogger(_component)    # Create the component logger.

#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#|                    END OF FILE:    examples/__init__.py
#|==============================================================================
