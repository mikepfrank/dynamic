import logmaster
_logger = logmaster.getLogger(logmaster.sysName + '.simulator')

from functions.binaryDifferentiableFunction import BinaryDifferentiableFunction

from .dynamicNode        import DynamicNode
from .dynamicPort        import DynamicPort         as Port
from .dynamicComponent   import DynamicComponent
from .dynamicNetwork     import DynamicNetwork

#-- A DynamicTwoTerminalGate has two nodes called "input" and "output"
#   with a single interaction term between them.  It's assumed that there's
#   no internal state other than the position/velocity values associated
#   with the two nodes.

class DynamicTwoTerminalGate(DynamicComponent):

    #-- Data members:
    #       interaction [BinaryDifferentiableFunction] -
    #           Interaction potential energy function between the
    #           input and output node's coordinates (x,y).

    #-- To initialize a dynamic two-terminal "gate," we simply
    #   create two ports called "input" and "output," create
    #   a simple dynamic node to be our output node, and link
    #   it to our output port.

    def __init__(inst, inputNode:DynamicNode, name:str=None,
                 network:DynamicNetwork=None, inPortName:str='input',
                 outPortName:str='output',
                 interaction:BinaryDifferentiableFunction=None,
                 outNodeName:str=None, initOutPos:Real=None):

            # First do generic initialization for dynamic components.

        _logger.normal("DynamicTwoTerminalGate.__init__(): Initializing "
                       "component named %s in network %s." %
                       (name, str(network)))
        
        DynamicComponent.__init__(inst, name=name, network=network)

            # Create our two ports, named "input" and "output".

        _logger.normal("DynamicTwoTerminalGate.__init__(): Creating two "
                       "ports named %s and %s..." %
                       (inPortName, outPortName))
        
        inst._addPorts(inPortName, outPortName)

            # Remember our port name for future reference.

        inst.inPortName  = inPortName
        inst.outPortName = outPortName

            # Link our input node to our input port.

        _logger.normal("DynamicTwoTerminalGate.__init__(): Linking input "
                       "node %s to our port named %s..." %
                       (str(inputNode), inPortName))

        inst.inputNode = inputNode
        inst.link(inPortName, inputNode)

        _logger.normal("DynamicTwoTerminalGate.__init__(): Right after "
                       "linking input node, it is as follows:")
        inputNode.printInfo()

            # Create and remember our output node named "out".

        initialOutputNodeName = outNodeName or 'out'

        _logger.normal("DynamicTwoTerminalGate.__init__(): Creating output "
                       "node initially named %s..." % initialOutputNodeName)
        
        inst.outputNode = DynamicNode(network, name=initialOutputNodeName)

        if initOutPos is not None:
            inst.outputNode.coord.position.value = Fixed(initOutPos)

        _logger.normal("DynamicTwoTerminalGate.__init__(): Linking new "
                       "output node %s to our port named %s..." %
                       (str(inst.outputNode), outPortName))

            # Link our port named "output" to our output node.

        inst.link(outPortName, inst.outputNode)

            # Set our interaction function to the given function.

        _logger.normal("DynamicTwoTerminalGate.__init__(): Setting "
                       "interaction function to %s..." %
                       str(interaction))

        if interaction != None:  inst.interaction = interaction
        
# The below shouldn't be needed since the node was created in the network already.
#
##            # Add our output node to the network.
##
##        if network != None:  network.addNode(inst.outputNode)

    #__/ End method DynamicTwoTerminalGate.__init__().

    @property
    def inPortName(this):
        if hasattr(this, '_inPortName'):
            return this._inPortName
        else:
            return None

    @inPortName.setter
    def inPortName(this, inPortName:str):
        this._inPortName = inPortName               # Remember our portname.
        if this.inPort != None:                   # If our port has been created,
            this.inPort.name = inPortName           #   actually set the port's name.
        if this.interaction != None:              # If our potential has been set,
            this.interaction.argName1 = inPortName   #   set its argument name.

    @property
    def outPortName(this):
        if hasattr(this, '_outPortName'):
            return this._outPortName
        else:
            return None

    @outPortName.setter
    def outPortName(this, outPortName:str):
        this._outPortName = outPortName               # Remember our portname.
        if this.outPort != None:                   # If our port has been created,
            this.outPort.name = outPortName           #   actually set the port's name.
        if this.interaction != None:              # If our potential has been set,
            this.interaction.argName2 = outPortName   #   set its argument name.

    @property
    def inPort(this) -> Port:
        ports = this.ports      # Get our ports.
        #print("ports is %s" % (str(ports)))
        nPorts = len(ports)     # Count how many ports we have.
        if nPorts == 0:         # If we have zero ports,
            return None         # return that our port is None.
        #print("%d ports" % nPorts)
        if nPorts != 2:
            raise WrongNumberOfPortsException("Two-terminal gate %s was found to have %d ports (%s)!" %
                                        (this, nPorts, str(ports)))
        assert nPorts == 2              # We should have exactly two ports.
        return list(ports.values())[0]  # Return the first port.

    @property
    def outPort(this) -> Port:
        ports = this.ports      # Get our ports.
        #print("ports is %s" % (str(ports)))
        nPorts = len(ports)     # Count how many ports we have.
        if nPorts == 0:         # If we have zero ports,
            return None         # return that our port is None.
        #print("%d ports" % nPorts)
        if nPorts != 2:
            raise WrongNumberOfPortsException("Two-terminal gate %s was found to have %d ports (%s)!" %
                                        (this, nPorts, str(ports)))
        assert nPorts == 2              # We should have exactly two ports.
        return list(ports.values())[1]  # Return the second port.

    @property
    def interaction(this):      # The interaction between input & output terminals.
        if hasattr(this, '_interaction'):
            return this._interaction
        else:
            return None

    @interaction.setter
    def interaction(this, interaction:BinaryDifferentiableFunction):

        if this.interaction != None:
            del this.interaction

        if interaction != None:

            if this.inPortName != None:
                interaction.argName1 = this.inPortName

            if this.outPortName != None:
                interaction.argName2 = this.outPortName

            this._interaction = interaction

            this._addInteraction(interaction)

    @interaction.deleter
    def interaction(this):

        if this.interaction != None:
            this._removeInteraction(this._interaction)

        del this._interaction
        
