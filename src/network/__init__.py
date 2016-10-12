# network/__init__.py - Initialization for the network package.

# When a package's __init__.py file is loaded, the namespace is pre-loaded
# with the attribute __path__ which contains the full filesystem path to the 
# package's directory, which in this case the the "network/" subdirectory
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
    'dynamicNode',
	'dynamicLink',
	'dynamicPort',
    'dynamicComponent',
    'dynamicOneTerminalComponent',
    'dynamicOneTerminalGate',
    'dynamicTwoTerminalGate',
    'dynamicThreeTerminalGate',
    'dynamicNetwork'
    ]

#print("__path__ is %s" % __path__)

    # Create a logger for this package (as a software component).

from logmaster import *

_component = __path__[0].split('\\')[-1]    # Component name = package name.
_logger = getComponentLogger(_component)    # Create the component logger.
