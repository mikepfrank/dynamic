
class BaseComponent:

    #-- Data members:
    #       port [dict] - Map from port name to Port object.

    def __init__(inst):  pass

    def addPort(this, portName):

        this.port[portName] = Port(this, portName)

    def addPorts(this, nameList):

        for name in nameList:
            this.addPort(name)

    def link(this, portName, node):

        Link(this.port[portName], node)
        
