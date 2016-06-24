from numbers            import Real    # Used by DynamicNetwork.thermalize().

import logmaster

from dynamicNode        import DynamicNode
from dynamicComponent   import DynamicComponent
from linkport           import Link 
from hamiltonian        import HamiltonianTerm,Hamiltonian

__all__ = ['DynamicNetwork']

logger = logmaster.getLogger(logmaster.sysName + '.network')

#   DynamicNetwork class.  In Dynamic, a Network conceptually consists of:
#
#       * A set of named dynamic nodes.  The names of these must be
#           unique within the network.
#
#       * A set of primitive component instances (gates and other
#           devices).
#
#       * A set of links connecting ports of components to nodes.
#
#       * A Hamiltonian determining the dynamical behavior of the
#           network.  This gets derived automatically from the
#           structure of the network.
#
#       Nodes, gates, and links can be added to a DynamicNetwork at
#       any time and the Hamiltonian is automatically restructured.
#       If a gate is added, its input and output nodes are also
#       automatically added.  If a node is added, all its links are
#       added; if a link is added, the items it links are added.

class DynamicNetwork:

    #-- Public data members:
    #
    #       inst.name [str] - Concise name for this network.
    #       inst.title [str] - More verbose title of this network (for display).
    #
    #-- Private data members:
    #
    #       inst._nodes [dict] - Map from node names to objects in this network.
    #       inst._components [list] - The set of components in this network.
    #       inst._links [list] - The set of links in this network.
    #
    #       inst._hamiltonian [Hamiltonian] - The Hamiltonian of this network.
    #
    #       inst._seqno [int] - Sequence number used internally to generate
    #                               new unique node names as needed.
    
    def __init__(inst, name:str=None, title:str=None):

        if name != None:    inst.name = name
        if title != None:   inst.title = title

        netname = netName(inst)

        logger.info("Initializing a new DynamicNetwork named '%s' (\"%s\")..." %
                    (netname, str(title)))

        inst._nodes = dict()    # Initially empty set of nodes.
        inst._components = []   # Initially empty list of components.
        inst._links = []        # Initially empty list of links.

        inst._hamiltonian = None    # Initially null Hamiltonian.

        inst._seqno = 0     # Initial sequence number for node names is 0.

    def __str__(self):
        return netName(self)
    
    #== Public instance methods.

    #-- inst.addComponent(part:BaseComponent) - Adds the given
    #       discrete component (and its connected nodes) to the
    #       network.

    def addComponent(self, part:DynamicComponent):
        logger.debug("Adding component '%s' into network '%s'..." % (str(part), str(self)))
        self._components.append(part)
        # Here we need to, like, also make sure that all of the component's connected nodes
        # (if any) are also in the network.

    @property
    def hamiltonian(self):
        if hasattr(self,'_hamiltonian'):
            return self._hamiltonian
        else:
            return None

    def _addHamiltonianTerm(self, term:HamiltonianTerm):

            # If this network does not even have any Hamiltonian
            # yet, create an empty one to start with.

        if self.hamiltonian == None:
            self._hamiltonian = Hamiltonian()    # Create new empty Hamiltonian.

            # Add the given term into the Hamiltonian.
        
        self.hamiltonian.addTerm(term)
    
    #-- inst.addNode(node:DynamicNode) - Adds the given node to the
    #       network (and its connected links).  If no name is provided,
    #       use the existing name; if the name is not unique, append
    #       a sequence number chosen to make it unique.

    def addNode(self, node:DynamicNode, nodeName:str=None):
    
        # First, make sure the given node is not already in the network.
        # If it is already in the network, we just return without doing anything.
        # (I suppose we could verify that its name is recorded correctly and that
        # its connected links are also in the network, but really that should have
        # been done earlier...)

        if node in self._nodes.values():
            return

        # OK, it's not already in the network, so let's actually add it now.

        if nodeName == None:  nodeName = node.getName()

        if nodeName in self._nodes:     # Name is not unique in this network!  Make it unique...

            self._seqno = self._seqno + 1

            newName = "%s%d" % (nodeName, self._seqno)

            logger.debug("Renaming node '%s' to '%s' for uniqueness within network '%s'..." %
                         (nodeName, newName, str(self)))

            nodeName = newName
        
        node.renameTo(nodeName)     # Does nothing if node already had that name.

        logger.debug("Adding node '%s' to network '%s'" % (nodename, str(self)))

        self._nodes[nodeName] = node

    #-- inst.addLink(link:Link) - Add the given link to the network
    #       (and its connected items).

    def addLink(self, link:Link):
        self._links.append(link)

    # Assuming the network is already constructed but has no associated Hamiltonian yet,
    # constructs its Hamiltonian.  Does it make more sense to create it all at once, or
    # incrementally???

    def constructHamiltonian(self):
        pass

    #-- inst.evolveTo() - Evolve the state of all generalized position
    #       variables in the network forwards to the given timestep.

    def evolveTo(self, timestep:int):
        pass    # To be implemented!

    #-- inst.test() - Test this network by initializing it and then
    #       simulating it forwards in time a few steps.

    def test(self):

        logger.info("Thermalizing network '%s' to unit temperature..." % str(self))

            # Initialize the network by thermalizing the
            # generalized momenta of all coordinates.
        
        self.thermalize(1.0)    # Temperature units are arbitrary for now.

            # Simulate the network forwards for a few time-steps.

        logger.info("Evolving network '%s' forwards ten time-steps..." % str(self))
        
        self.evolveTo(10)       # Just a few steps, to exercise things.

    #-- inst.thermalize() - This function randomizes the velocities
    #       of all generalized coordinates in the network according
    #       to a thermal distribution, with an average energy per
    #       degree of freedom of kT.

    def thermalize(inst, temperature:Real):

        # Really we need to pick gaussian-distributed velocities, but
        # for initial debugging purposes maybe we will just pick uniformly
        # distributed velocities within some range
        
        pass    # To be implemented!

# Module-level helper function to return a string representation of the name
# of a given network, or a string indicating an error if it's not a network!

def netName(obj):
    if obj == None:
        netname = '(no network)'
    elif not isinstance(obj,DynamicNetwork):
        netname = '[ERROR: NOT A NETWORK!]'
    elif not hasattr(obj, 'name'):
        netname = '(unnamed network)'
    else:
        netname = obj.name
    return netname
