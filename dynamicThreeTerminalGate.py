# dynamicThreeTerminalGate.py

import logmaster
_logger = logmaster.getLogger(logmaster.sysName + '.simulator')

from ternaryDifferentiableFunction import TernaryDifferentiableFunction

from linkport           import Port

from dynamicNode        import DynamicNode
from dynamicComponent   import DynamicComponent
from dynamicNetwork     import DynamicNetwork

    # A generic DynamicThreeTerminalGate has three ports named
    # "portA", "portB", and "portC" with a single three-way
    # interaction term between them.  It's assumed that there is
    # no internal state other than the position/velocity values
    # associated with the nodes attached to the three ports.  We
    # provide a constructor that takes nodeA and nodeB as input
    # and creates nodeC (useful when nodeC is an output).

class DynamicThreeTerminalGate(DynamicComponent):

    # Data members:
    #   interaction:TernaryDifferentiableFunction -
    #       Interaction potential energy function between the
    #       coordinates (x,y,z) of the three nodes.

    # Initializer (default constructor):
    #   We create three ports named "portA", "portB," and "portC", create
    #   a dynamic node nodeC to be our "output" node, and link it to portC.

    def __init__(me, nodeA:DynamicNode, nodeB:DynamicNode,
                 name:str = None, network:DynamicNetwork = None,
                 portAName:str='portA', portBName:str='portB', portCName:str='portC',
                 interaction:TernaryDifferentiableFunction=None):

        DynamicComponent.__init__(me, name=name, network=network)

        me._addPorts(portAName, portBName, portCName)

        me.portAName = portAName
        me.portBName = portBName
        me.portCName = portCName

        me.nodeA = nodeA
        me.nodeB = nodeB

        me.link(portAName, nodeA)
        me.link(portBName, nodeB)

        initialNodeCName = 'nodeC'

        me.nodeC = DynamicNode(network, name=initialNodeCName)

        me.link(portCName, me.nodeC)

        if interaction is not None: inst.interaction = interaction

    @property
    def portAName(me) -> str:
        if hasattr(me, '_portAName'):
            return me._portAName
        else:
            return None

    @portAName.setter
    def portAName(me, newName:str):
        me._portAName = newName
        if me.portA is not None:
            me.portA.name = newName
        if me.interaction is not None:
            me.interaction.argName1 = newName

    @property
    def portBName(me) -> str:
        if hasattr(me, '_portBName'):
            return me._portBName
        else:
            return None

    @portBName.setter
    def portBName(me, newName:str):
        me._portBName = newName
        if me.portB is not None:
            me.portB.name = newName
        if me.interaction is not None:
            me.interaction.argName2 = newName

    @property
    def portCName(me) -> str:
        if hasattr(me, '_portCName'):
            return me._portCName
        else:
            return None

    @portCName.setter
    def portCName(me, newName:str):
        me._portCName = newName
        if me.portC is not None:
            me.portC.name = newName
        if me.interaction is not None:
            me.interaction.argName3 = newName

    @property
    def portA(me) -> Port:
        ports = me.ports
        nPorts = len(ports)
        if nPorts == 0:
            return None
        if nPorts != 3:
            raise WrongNumberOfPortsException("Three-terminal gate %s was "
                                              "found to have %d ports (%s)!" %
                                              (this, nPorts, str(ports)))
        assert nPorts == 3
        return list(ports.values())[0]
            
    @property
    def portB(me) -> Port:
        ports = me.ports
        nPorts = len(ports)
        if nPorts == 0:
            return None
        if nPorts != 3:
            raise WrongNumberOfPortsException("Three-terminal gate %s was "
                                              "found to have %d ports (%s)!" %
                                              (this, nPorts, str(ports)))
        assert nPorts == 3
        return list(ports.values())[1]

    @property
    def portC(me) -> Port:
        ports = me.ports
        nPorts = len(ports)
        if nPorts == 0:
            return None
        if nPorts != 3:
            raise WrongNumberOfPortsException("Three-terminal gate %s was "
                                              "found to have %d ports (%s)!" %
                                              (this, nPorts, str(ports)))
        assert nPorts == 3
        return list(ports.values())[2]

    @property
    def interaction(me) -> TernaryDifferentiableFunction:
        if hasattr(me, '_interaction'):
            return me._interaction
        else:
            return None

    @interaction.setter
    def interaction(me, interaction:TernaryDifferentiableFunction):

        if me.interaction is not None:
            del me.interaction

        if interaction is not None:

            if me.portAName is not None:
                interaction.argName1 = me.portAName

            if me.portBName is not None:
                interaction.argName2 = me.portBName

            if me.portCName is not None:
                interaction.argName3 = me.portCName

            me._interaction = interaction

            me._addInteraction(interaction)

    @interaction.deleter
    def interaction(me):

        if me.interaction is not None:
            me._removeInteraction(me._interaction)

        del me._interaction
    
