import logmaster

from typing         import Iterable
from linkport       import Link,Port
from dynamicNode    import DynamicNode

import dynamicNetwork

__all__ = ['DynamicComponent']

logger = logmaster.getLogger(logmaster.sysName + '.network')

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
    #       ._network [DynamicNetwork] - Network this component is in.
    #
    #       ._ports [dict] - Map from port name to Port object.
    #
    #       ._interactions [list] - Set of interaction functions.
    #           The argument list of each function should be a
    #           subset of the set of our port names.
    #
    #       ._hamTerms [dict] - Map from interaction indices to
    #           the corresponding terms in the network's Hamiltonian.

    #-- Initializer.  This just creates an initially-empty port
    #       map and interaction set.

    def __init__(inst, name:str=None, network=None):

        if name != None: inst.name = name
        if network != None: inst._network = network

        netname = dynamicNetwork.netName(network)
        
        logger.debug("Initializing a new DynamicComponent named '%s' in network '%s'" %
                     (str(name), netname))
        
        inst._ports = dict()        # Initially-empty dictionary mapping port name to port object.
        inst._interactions = []     # Initially-empty list of interaction functions.
        inst._hamTerms = dict()     # Initially-empty dictionary mapping interaction indices to Hamiltonian terms.

        inst._enterOurNetwork()    # Tell ourselves, yeah, now actually go into our network (if any).

    @property
    def network(self):
        if hasattr(self, '_network'):
            return self._network
        else:
            return None

    @property
    def ports(self):
        if hasattr(self, '_ports'):
            return self._ports
        else:
            return []

    def _enterOurNetwork(self):

        net = self.network

        if net != None:
            net.addComponent(self)      # Tell our network to take us into itself.

    def __str__(self):
        if hasattr(self,'name'):
            return str(self.name)
        else:
            return '(unnamed component)'

    #== Private methods.

    #-- inst._addPort(portName:str) - Creates a new port of this component
    #       named <portName>.  It's initially not linked to anything.

    def _addPort(this, portName:str):
        
        logger.debug("Adding a port named '%s' to component '%s'..."
                     % (portName, str(this)))
        
        this._ports[portName] = Port(this, portName)

    #-- inst._addPorts(nameList) - Creates new ports of this component
    #       with the names in <nameList>, which should be a list of strings.

    def _addPorts(this, *nameList:Iterable[str]):
        for name in nameList:
            #print("Adding port %s..."%name)
            this._addPort(name)

    #-- .link(portName, node) - Links the port named <portName> of this
    #       component to the external node <node>.

    def link(this, portName:str, node:DynamicNode):

        logger.debug("Linking port '%s' of component '%s' to node '%s'..."
                     % (portName, str(this), str(node)))

        Link(this._ports[portName], node)

    #-- inst.portLinked(portName) - Returns True if our port named 'portName' is linked
    #       to some node currently; returns False otherwise (including if we have no such port).

    def portLinked(this, portName:str):
        port = this.portNamed(portName)     # Get our port of the given name.
        if port == None: return False       # If we didn't have one of that name, return False.
        return port.linked()                # Return True if the port is liked to a node, else False.

    # Return True if all the ports of a given one of our interactions are linked to actual nodes.

    def interactionPortsLinked(this, interactionID:int):

        interaction = this._interactions[interactionID]

        argNames = interaction.argNames       # Get the list of arguments for this potential.

        return all(map(lambda argName: this.portLinked(argName))):

    def _hamiltonianTermFor(this, interactionIndex:int):

        if not interactionIndex in this._hamTerms:
            this._hamTerms[interactionIndex] = 
            
        return this._hamTerms[interactionIndex]

    # Adds a given interaction function to this component's list of interaction functions.
    # This is marked private because it should normally only be used as subclasses while they are
    # building up the component.

    def _addInteraction(this, potential:BaseDifferentiableFunction):

        interactionIndex = len(this._interactions)

        # Add the given potential to our list.  (Note that even if it was already
        # present, the semantics here is to add it again... Generating another
        # parallel term in the Hamiltonian which effectively increases the potential.)

        this._interactions.append(potential)

        # If all the named ports are linked to nodes, we can go ahead and create
        # a Hamiltonian term for the interaction.

        if this.interactionPortsLinked(interactionIndex):

                # This returns the Hamiltonian term for this interaction if we haven't
                # previously constructed it.
            
            term = this._hamiltonianTermFor(interactionIndex)

                # Add this new term to the network's Hamiltonian.

            this.network.addHamiltonianTerm(term)

    # Removes a given interaction function from this component's list of interactions functions.

    def _removeInteraction(this, potential:BaseDifferentiableFunction):

        # Be sure to remove the corresponding Hamiltonian term (if any) as well.
        
        pass    # To be implemented.

