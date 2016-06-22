from typing         import Iterable
from linkport       import Link,Port
from dynamicNode    import DynamicNode

#-- This is a base class from which to derive subclasses for specific
#   types of Dynamic components.  The general features of a component
#   are:
#
#       * It has a set of "ports," which are named interface
#           points that can be linked up to external dynamic nodes.
#
#       * It has a set of interaction functions that interrelate
#           the dynamical states of subsets of nodes connected to
#           various ports.  For our present purposes, these consist
#           of potential energy functions of one or more variables
#           (one per node in a set).  In the context of a network,
#           these translate to Hamiltonian interactions between
#           the nodes' coordinates.

class DynamicComponent:

    #-- Private data members:
    #
    #       ._ports [dict] - Map from port name to Port object.
    #
    #       ._interactions [list] - Set of interaction functions.
    #           The argument list of each function should be a
    #           subset of the set of our port names.

    #-- Initializer.  This just creates an initially-empty port
    #       map and interaction set.

    def __init__(inst):
        inst._ports = dict()     # Initially-empty dictionary mapping port name to port object.
        inst._interactions = []     # Initially-empty list of interaction functions.

    #== Private methods.

    #-- inst._addPort(portName:str) - Creates a new port of this component
    #       named <portName>.  It's initially not linked to anything.

    def _addPort(this, portName:str):
        this._ports[portName] = Port(this, portName)

    #-- inst._addPorts(nameList) - Creates new ports of this component
    #       with the names in <nameList>, which should be a list of strings.

    def _addPorts(this, *nameList:Iterable[str]):
        for name in nameList:
            print("Adding port %s..."%name)
            this._addPort(name)

    #-- .link(portName, node) - Links the port named <portName> of this
    #       component to the external node <node>.

    def link(this, portName:str, node:DynamicNode):

        Link(this._ports[portName], node)
        
