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

    #/--------------------------------------------------------------------------
    #|
    #|  GENERAL COMMENTS ON PYTHON PACKAGE INITIALIZATION FILES:
    #|
    #|          A package in Python is defined by a subdirectory of the
    #|      Python program's top-level directory, whose name is the package
    #|      name, and which contains an __init__.py file, like this one.
    #|      That file defines a module named <package>, which is the package.
    #|      Any other .py files in the directory are modules in the package.
    #|      Packages may also contain nested sub-packages in subdirectories.
    #|
    #|          When a package's __init__.py file is loaded, the namespace
    #|      gets pre-loaded with the attribute __path__, which contains
    #|      the full filesystem path to the package's directory, which (in
    #|      this case) is the "simulator/" subdirectory of the top-level
    #|      source directory for the Dynamic system.
    #|
    #|          Then, the package may define __all__, which is a list of
    #|      the module names that would be automatically imported if the
    #|      user of the package did "from <package> import *".
    #|
    #|          However, the stylistically-preferred way to import modules
    #|      from a package is one at a time, as in the syntax
    #|
    #|                  from <package> import <module>                  ,
    #|
    #|      or you can also import specific module attributes like this:
    #|
    #|                  from <package>.<module> import <attr>           .
    #|
    #|          Modules in packages can import other "sibling" modules
    #|      residing in the same ("parent") package as themselves using
    #|      the abbreviated syntax,
    #|
    #|                  from .<siblingModule> import <attr>             ,
    #|
    #|      and from other "cousin" modules residing in "uncle" packages
    #|      (i.e., packages that are siblings of the module's parent
    #|      package) using syntax like
    #|
    #|                  from ..<unclePackage> import <cousinModule>     .
    #|
    #|      However, that syntax is not advantageous except from within
    #|      nested packages, because otherwise the '..' can be omitted.
    #|
    #\--------------------------------------------------------------------------

        #/----------------------------------------------------------------------
        #|
        #|      __all__                                 [special package global]
        #|
        #|              Within the __init__ file of a package, the
        #|              __all__ global defines the list of module
        #|              names that will be automatically imported
        #|              if the user does "from <package> import *".
        #|              These can be considered to be the "public"
        #|              modules of the package.  A package may also
        #|              include private modules (whose names would
        #|              conventionally start with underscores).
        #|              Those modules would not be listed here.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

__all__ = [
        # Example devices.
    'dynamicMemCell',   # Quadratic-potential ROM cell,
    'rangeBinder',      # and quartic bistable well.
        # Example networks.
    'exampleNetworks'   # Still need to split out halfadder, fulladder etc.
    ]


    #---------------------------------------------------------------------------
    #   Consider this package to be a software component, and create a
    #   logger for it.  Child modules may access this logger using the
    #   syntax "from . import _logger" rather than calling getLogger().
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

from logmaster import getComponentLogger    # Function we use to get logger.

_component = __path__[0].split('\\')[-1]    # Component name = package name.
_logger = getComponentLogger(_component)    # Create the component logger.

#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#|                    END OF FILE:    examples/__init__.py
#|==============================================================================
