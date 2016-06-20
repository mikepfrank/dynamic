from port        import Port
from dynamicNode import DynamicNode

#-- This is a base class from which to derive subclasses for specific
#   Dynamic components.  The general features of a component are:
#
#       * It has a set of "ports," which are named interface
#           points that can be linked up to external dynamic nodes.

class BaseComponent:

    #-- Data members:
    #       port [dict] - Map from port name to Port object.

    #-- Initializer.  This creates an empty port map.

    def __init__(inst):
        inst.ports = dict()     # Dictionary mapping port name to port object.

    #-- .addPort(portName:str) - Creates a new port of this component
    #       named <portName>.

    def addPort(this, portName:str):

        this.ports[portName] = Port(this, portName)

    #-- .addPorts(nameList) - Creates new ports of this component
    #       with the names in <nameList>, which should be a list of strings.

    def addPorts(this, nameList):

        for name in nameList:
            this.addPort(name)

    #-- .link(portName, node) - Links the port named <portName> of this
    #       component to the external node <node>.

    def link(this, portName:str, node:DynamicNode):

        Link(this.port[portName], node)
        
