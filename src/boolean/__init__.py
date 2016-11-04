#|==============================================================================
#|                  TOP OF FILE:    boolean/__init__.py
#|------------------------------------------------------------------------------
#|   The below module documentation string will be displayed by pydoc3.
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""
    FILE NAME:          __init__.py         [Python package initialization file]

    FULL PATH:          $GIT_ROOT/dynamic/src/boolean/__init__.py

    SYSTEM NAME:        Dynamic (simulator for dynamic networks)

    PACKAGE NAME:       boolean

    COMPONENT NAME:     Dynamic.simulator


    FILE DESCRIPTION:
    -----------------

        This Python file is the package-initialization module for
        the 'boolean' package within the Dynamic software system.
        
        For general background on Python packages, see the comments
        within this file, or the online documentation at:
        [https://docs.python.org/3/tutorial/modules.html#packages].


    PACKAGE DESCRIPTION:
    --------------------

        The purpose of the 'boolean' package is to gather together
        the modules implementing classes for various types of standard
        Boolean logic gates.

        At present, we only support a single implementation of each
        type of gate, but in the future this could be generalized
        with many different alternative implementations of each type
        of gate, and a factory class that selects the implementation
        appropriately according to the policy/style/logic family used
        in a particular network.

        The gate types presently supported are NOT (logical inverter),
        and two-input AND, OR, and XOR (exclusive OR) gates.  All
        gates are implemented by simple quadratic potential-energy
        functions whose minimum is attained whenever all incident
        nodes have consistent logical values.  The potential-energy
        "valleys" that pass between the valid logical states are
        flat-bottomed, and so include many other minimum-energy points
        as well (e.g., x=0.5, y=0.5 for a NOT gate).  This flatness
        facilitates smooth transitions between valid logic values, but
        it means that there is some "entropic pressure" for the state
        to wander away from the valid levels, which can result in slow
        convergence of mean values to valid levels, especially in
        larger networks.  In future implementations, we may explore
        different shapes of potential-energy surfaces, to trade off
        these kinds of considerations.

        Other standard Boolean logic gate types which may be added to
        this package in the future include:  two-input NAND, NOR, XNOR,
        and N-input (for any N>2) versions of all of the gate types.
    

    PACKAGE DEPENDENCIES:
    ---------------------

        The boolean package uses the network and function packages, and
        is used by the examples package.
        
    
    MODULE HIERARCHY:
    -----------------

        The approximate hierarchy of modules within this package (also
        shown in the package's README.md file) is as follows:


        		 _______________
	Package 	/               \\
	module:		|    boolean    |
			| (__init__.py) |
			\_______________/
	Modules in		|
	package:		|
				V
			dynamicXORGate.py	(all parallel)
			dynamicORGate.py
			dynamicANDGate.py
			dynamicNOTGate.py
                                                                             """
#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#| End of module documentation string for boolean/__init__.py.
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

    # These are listed in the order in which they were implemented.
    
__all__ = [
    'dynamicNOTGate',   # The only one-input Boolean gate.
    'dynamicANDGate',   # Two-input Boolean gates.
    'dynamicORGate',
    'dynamicXORGate'
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
#|                    END OF FILE:    boolean/__init__.py
#|==============================================================================
