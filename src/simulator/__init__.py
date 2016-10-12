#|==============================================================================
#|                  TOP OF FILE:    simulator/__init__.py
#|------------------------------------------------------------------------------
#|   The below module documentation string will be displayed by pydoc3.
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""
    FILE NAME:          __init__.py         [Python package initialization file]

    FULL PATH:          $GIT_ROOT/dynamic/src/simulator/__init__.py

    SYSTEM NAME:        Dynamic (simulator for dynamic networks)

    PACKAGE NAME:       simulator

    COMPONENT NAME:     Dynamic.simulator


    FILE DESCRIPTION:
    -----------------

        This Python file is the package-initialization module for
        the 'simulator' package.  For general background on Python
        packages, see the comments within this file, or the doc
        https://docs.python.org/3/tutorial/modules.html#packages.


    PACKAGE DESCRIPTION:
    --------------------

        The purpose of the 'simulator' package is to gather together
        the modules implementing the core, essential pieces of the
        Dynamic simulation framework.  This includes modules
        implementing the basic concept of dynamically-updatable
        variables, including canonical coordinate pairs whose time
        derivatives are automatically determined using Hamilton's
        equations.  It also includes modules representing or
        controlling overall aspects of a given simulation (so far
        just the simulationContext and simmor modules).

        Note that this package does not know anything about concepts
        like the circuit structure of a dynamic logic network; that
        is all handled by higher-level packages such as the 'network'
        and 'boolean' packages, which utilize this package internally.


    MODULE HIERARCHY:
    -----------------

        The approximate hierarchy of modules within this package (also
        shown in the package's README.md file) is as follows:
        
                         _______________
            Package     /               \\
            module:     |   simulator   |
                        | (__init__.py) |
                        \_______________/
            Modules in      |         | 
            package:        |         V 
                            |       simmor.py
                            |               \\
                            V                \\
                      dynamicCoordinate.py    \\
                                |              \\
                                V               \\
                     hamiltonianVariable.py      \\
                                |                 \\
                                V                 |
                         hamiltonian.py           |
                                |                 |
                                V                 |
                differentiableDynamicFunction.py  |
                                |                 /
                                V                /
                     derivedDynamicFunction.py  /
                                |              /
                                V             /
                        dynamicVariable.py   /
                            |       |       /
                            V       |      /
              dynamicFunction.py    |      |
                                    V      V
                            simulationContext.py


    MODULE DESCRIPTIONS:
    --------------------

        The following are brief descriptions of the purposes of the
        different modules in the simulator packages, roughly in order
        from the lowest-level modules (those which do not depend on
        other modules) to the higher-level modules that depend upon
        them.

            simulationContext.py - Simulation context module.
            
                This module defines global properties that apply to
                the entiresimulation, e.g., the time step size.

            dynamicFunction.py - Dynamic functions module.

                This module defines general classes for dynamic
                functions, which are functions of time whose value
                at a given time is computed by first stepping the
                simulation forwards or backwards as needed to arrive
                at that time, and then evaluating the function.

            dynamicVariable.py - Dynamic variables module.

                This module defines a class for dynamic variables,
                which can step their own value forwards or backwards
                in time as needed by applying a known time-derivative
                function.  The core centered-difference state-updating
                algorithm for time integration is implemented here.

            derivedDynamicFunction.py - Derived dynamic functions module.

                This module defines a class for derived dynamic
                functions, that is, dynamic functions of one or more
                dynamic variables, which are evaluated by stepping
                those variables forwards or backwards and time as
                needed, and then evaluating the function.

            differentiableDynamicFunction.py - Differentiable dynamic functions module.

                This module defines a class for differentiable dynamic
                functions, which are derived dynamic functions that
                are also differentiable with respect to any of their
                dynamic variables, and whose partial derivative with
                respect to any given variable is itself another
                derived dynamic function.

            hamiltonian.py - Hamiltonian module.

                This module defines classes for representing
                individual additive terms in a Hamiltonian, as 
                well as general Hamiltonian functions which may be
                expressed as a sum of such terms.

            hamiltonianVariable.py - Hamiltonian variable module.

                This module defines a class for Hamiltonian variables,
                which are dynamic variables that keep track of the
                Hamiltonian function that they are associated with,
                so they can infer their own time-derivative from it.

            dynamicCoordinate.py - Dynamic coordinate module.

                This module defines a class for dynamical coordinates,
                which means canonical coordinate pairs consisting of a
                generalized position coordinate and an associated
                generalized momentum coordinate.  The 'leapfrog'-style
                approach for time integration (which here means,
                alternately updating the position and momentum
                coordinates) is implemented here.

            simmor.py - Simulator object module.

                This module (still experimental) defines a top-level
                class called Simmor to manage the entire simulation.

        Note that presently, all modules in the simulator package are
        designated public (which really just means that we haven't yet
        subdivided them into public and private modules).  Good
        candidates for private modules would be modules that are not
        directly referenced anywhere outside the simulator package.
                                                                             """
#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#| End of module documentation string for simulator/__init__.py.
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

    # In the following list, modules are shown roughly in hierarchical order
    # with the lowest-level modules listed first.
    
__all__ = [                     # All public modules exported from this package.
    'simulationContext',                # Global properties of a simulation.
    'dynamicFunction',                  # Functions tied to the simulator state.
    'dynamicVariable',                  # Update themselves using time derivs.
    'derivedDynamicFunction',           # Functions of dynamic variables.
    'differentiableDynamicFunction',    # Ones that are also differentiable.
    'hamiltonian',                      # Single terms and sums-of-terms.
    'hamiltonianVariable',              # Variables that know their Hamiltonian.
    'dynamicCoordinate',                # Canonical position-momentum pairs.
    'simmor'                            # Object managing a whole simulation.
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
#|                    END OF FILE:    simulator/__init__.py
#|==============================================================================
