import logmaster

from unaryDifferentiableFunction    import UnaryDifferentiableFunction
from linkport                       import Link,Port
from dynamicNode                    import DynamicNode
from dynamicComponent               import DynamicComponent
from dynamicNetwork                 import DynamicNetwork,netName

logger = logmaster.getLogger(logmaster.sysName + '.network')

class TooManyPortsException(Exception): pass

#-- A DynamicOneTerminalGate has one node called "output"
#   together with a single built-in potential energy function.
#   It may also have internal coordinates, but is not required to.

class DynamicOneTerminalGate(DynamicComponent):

    #-- Instance public properties:
    

    #-- Instance private data members:
    #
    #       inst._portName:str
    #
    #           One-terminal gates in Dynamic have a single port,
    #           which is typically conceived as an output since it
    #           could be influenced by the internal state of the
    #           gate (if any).  This data member remembers the name
    #           of this port.  We enforce that its name must be the
    #           same as the name of the argument to our potential
    #           energy function, so they can be matched up by the
    #           code in dynamicComponent that handles the effects of
    #           introducing an interaction (creating corresponding
    #           terms in the network's Hamiltonian).
    #
    #       inst._potential [BaseDifferentiableFunction] -
    #
    #               Potential energy function for the output node's coordinate x.

    #-- To initialize a dynamic one-terminal "gate," we simply
    #   create one port called "output," create a simple dynamic
    #   node to be our output node, and link it to our output port.

    def __init__(inst, name:str=None, portName:str='q',
                 network:DynamicNetwork=None,
                 potential:UnaryDifferentiableFunction=None):

        netname = netName(network)

        logger.debug(("Initializing a new DynamicOneTerminalGate named '%s' "
                     + "with port name '%s' in network '%s'") %
                     (str(name), portName, netname))

            # First do generic initialization for dynamic components.

        DynamicComponent.__init__(inst, name=name, network=network)

            # Create our one port named <portName>.

        inst._addPorts(portName)

            # Remember our port name for future reference.

        inst.portName = portName

            # Create and remember our output node, initially with the
            # same name as our output port that we'll connect it to.

        inst.outputNode = DynamicNode(portName)

            # Link our port named <portName> to our output node.

        inst.link(portName, inst.outputNode)

            # Set our potential energy function to the given function.

        if potential != None:  inst.potential = potential

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
            raise TooManyPortsException("One-terminal gate %s was found to have %d ports (%s)!" %
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
            
            this._addInteraction(this._potential)
                # Add the potential to this component's interaction list.

    @potential.deleter
    def potential(this):
        
        if this.potential != None:
            this._removeInteraction(this._potential)      # Remove it from component's interaction list

        del this._potential
    




        
