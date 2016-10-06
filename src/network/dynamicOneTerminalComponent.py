# A DynamicOneTerminalComponent is a component that attaches to only one node.
# The node is assumed to have already been created, and is passed in.  Note
# this differs from DynamicOneTerminalGate which assumes its node is an output
# node, and creates it.

import logmaster; from logmaster import *

from functions.unaryDifferentiableFunction    import UnaryDifferentiableFunction
from .linkport                       import Link,Port
from .dynamicNode                    import DynamicNode
from .dynamicComponent               import DynamicComponent
from .dynamicNetwork                 import DynamicNetwork,netName

_logger = getLogger(sysName + '.network')

class DynamicOneTerminalComponent(DynamicComponent):

    def __init__(inst, node:DynamicNode, name:str=None, portName:str='x',
                 network:DynamicNetwork=None,
                 potential:UnaryDifferentiableFunction=None):

        if network is None:  network = node.network

        netname = netName(network)

        if doDebug:
            _logger.debug(("Initializing a new DynamicOneTerminalComponent named '%s' "
                         + "with port name '%s' in network '%s'") %
                         (str(name), portName, netname))

            # First do generic initialization for dynamic components.

        DynamicComponent.__init__(inst, name=name, network=network)

            # Create our one port named <portName>.

        inst._addPorts(portName)

            # Remember our port name for future reference.

        inst.portName = portName

        inst.node = node

        if doInfo:
            _logger.info("DynamicOneTerminalComponent.__init__: Before linking output node:")            
            inst.node.printInfo()

            # Link our port named <portName> to our output node.

        inst.link(portName, inst.node)

        if doInfo:
            _logger.info("DynamicOneTerminalComponent.__init__: After linking output node:")
            inst.node.printInfo()

            # Set our potential energy function to the given function.

        if potential != None:  inst.potential = potential

            # Add our output node to the network.

        ##if network != None:  network.addNode(inst.node)

    @property
    def portName(this):
        if hasattr(this, '_portName'):
            return this._portName
        else:
            return None

    @portName.setter
    def portName(this, portName:str):
        this._portName = portName               # Remember our portname.
        if this.port != None:                   # If our port has been created,
            this.port.name = portName           #   actually set the port's name.
        if this.potential != None:              # If our potential has been set,
            this.potential.argName = portName   #   set its argument name.

    @property
    def port(this) -> Port:
        ports = this.ports      # Get our ports.
        #print("ports is %s" % (str(ports)))
        nPorts = len(ports)     # Count how many ports we have.
        if nPorts == 0:         # If we have zero ports,
            return None         # return that our port is None.
        #print("%d ports" % nPorts)
        if nPorts > 1:
            raise WrongNumberOfPortsException("One-terminal gate %s was found to have %d ports (%s)!" %
                                        (this, nPorts, str(ports)))
        assert nPorts == 1              # We should have exactly one port.
        return list(ports.values())[0]  # Return that port.

    @property
    def potential(this):
        if hasattr(this, '_potential'):
            return this._potential
        else:
            return None

    @potential.setter
    def potential(this, potential:UnaryDifferentiableFunction):

        if doDebug:
            _logger.debug("Setting %s's potential function to %s..." %
                         (this.name, str(potential)))

        # If the potential was previously set to something else, delete the old potential first.
        
        if this.potential != None:
            del this.potential          # Call's property's deleter method.

        # If our potential is being set to an actual, non-null potential,
        # then make sure that potential's argument name matches our port
        # name, and add it to this gate's interaction function list.

        if potential != None:

            if this.portName != None:
                potential.argName = this.portName
            
            this._potential = potential
            
            this._addInteraction(potential)
                # Add the potential to this component's interaction list.

    @potential.deleter
    def potential(this):
        
        if this.potential != None:
            this._removeInteraction(this._potential)      # Remove it from component's interaction list

        del this._potential
    

        
