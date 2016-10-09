from numbers            import Real    # Used by DynamicNetwork.thermalize().

import logmaster
from   logmaster          import *      # ErrorException

global logger
logger = logmaster.getLogger(logmaster.sysName + '.network')

from .dynamicNode       import  DynamicNode         as Node
from .dynamicLink       import  DynamicLink         as Link
from .dynamicPort       import  DynamicPort         as Port
from .dynamicComponent  import  DynamicComponent    as Component

from simulator.hamiltonian        import HamiltonianTerm,Hamiltonian

class SimulationContext: pass       # Forward declaration to avoid circularity

__all__ = ['DynamicNetwork', 'netName']

class NetworkException(Exception): pass

class NoSuchNode(ErrorException, NetworkException):
    def __init__(self, *args, **kwargs):
        ErrorException.__init__(self, *args, **kwargs)
    

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
    #
    #       inst._context:SimulationContext - The simulation context that
    #           will be used for simulating this network.
    
    def __init__(inst, name:str=None, title:str=None, context:SimulationContext=None):

        if name != None:    inst.name = name
        if title != None:   inst.title = title

        netname = netName(inst)

        if doDebug:
            logger.debug("Initializing a new DynamicNetwork named '%s' (\"%s\")..." %
                         (netname, str(title)))

        inst._nodes = dict()    # Initially empty set of nodes.
        inst._components = []   # Initially empty list of components.
        inst._links = []        # Initially empty list of links.

        inst._hamiltonian = None    # Initially null Hamiltonian.

        inst._seqno = 0     # Initial sequence number for node names is 0.

        inst.context = context      # Also points context at us as a side-effect.

    def __str__(self):
        return netName(self)

    @property
    def context(self):
        if hasattr(self,'_context'):
            return self._context
        else:
            return None

    @context.setter
    def context(self, context:SimulationContext=None):
        if context is None:
            if hasattr(self,'_context'):
                del self.context
        else:
            self._context = context
            
                # Tell the simulation context that we were just given that,
                # "Hey, buddy, looks like we are the network that you are
                # supposed to be simulating here."
            context.network = self

    @context.deleter
    def context(self):
        if hasattr(self,'_context'):
            if self._context is not None:
                self._context.network = None    # Tell our context to ditch us.
            del self._context
    
    #== Public instance methods.

    #-- inst.addComponent(part:BaseComponent) - Adds the given
    #       discrete component (and its connected nodes) to the
    #       network.

    def addComponent(self, part:Component):

        if doDebug:
            logger.debug("Adding component '%s' into network '%s'..." %
                         (str(part), str(self)))
            
        self._components.append(part)
        # Here we need to, like, also make sure that all of the component's connected nodes
        # (if any) are also in the network.

    @property
    def hamiltonian(self):
        if hasattr(self,'_hamiltonian'):
            return self._hamiltonian
        else:
            return None

    # If this network doesn't already have a Hamiltonian structure attached
    # to it, reate an initial (empty) Hamiltonian that we can build upon.

    def initHamiltonian(self):
        if self.hamiltonian == None:
            self._hamiltonian = Hamiltonian()

    def _addHamiltonianTerm(self, term:HamiltonianTerm):

        if doDebug:
            logger.debug("Adding term %s to network %s's Hamiltonian..." %
                         (str(term), str(self)))

            # First make sure this network's Hamiltonian structure
            # has been initialized, so we can start adding terms to it.
            # (This does nothing if it was already initialized earlier.)

        self.initHamiltonian()

            # Now add the given term into the Hamiltonian.
        
        self.hamiltonian.addTerm(term)
    
    #-- inst.addNode(node:Node) - Adds the given node to the
    #       network (and its connected links).  If no name is provided,
    #       use the existing name; if the name is not unique, append
    #       a sequence number chosen to make it unique.

    def addNode(self, node:Node, nodeName:str=None):
    
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

            if doDebug:
                logger.debug("Renaming node '%s' to '%s' for uniqueness within network '%s'..." %
                             (nodeName, newName, str(self)))

            nodeName = newName
        
        node.renameTo(nodeName)     # Does nothing if node already had that name.

        if doDebug:
            logger.debug("Adding node '%s' to network '%s'" % (nodeName, str(self)))

        self._nodes[nodeName] = node

    # This method registers that a node has changed names from the
    # given <oldName> to its new name.

    def noticeNodeNameChange(self, node:Node, oldName:str=None):
        del self._nodes[oldName]        # There's no longer a node w old name in network
        self.addNode(node, node.name)

    #-- inst.addLink(link:Link) - Add the given link to the network
    #       (and its connected items).

    def addLink(self, link:Link):
        self._links.append(link)

    # Assuming the network is already constructed but has no associated Hamiltonian yet,
    # constructs its Hamiltonian.  Does it make more sense to create it all at once, or
    # incrementally???

    def constructHamiltonian(self):
        logger.fatal("DynamicNetwork.constructHamiltonian() not yet implemented!")

    #-- inst.evolveTo() - Evolve the state of all generalized position
    #       variables in the network forwards to the given timestep.


    def evolveTo(self, timestep:int):

        if doDebug:
            logger.debug("Dynamic network is going to evolve to timestep %d..." % timestep)

            if len(self._nodes) == 0:
                logger.debug("Debug warning: Dynamic network has no nodes!!!")

        for node in self._nodes.values():
            
            node.evolveTo(timestep)

##            logger.normal("%s, %.9f, %.9f" %
##                          (str(node),
##                           node.coord.ccp._posVar.value,
##                           node.coord.ccp._momVar.value))
        
# We used to do this by just updating the Hamiltonian but it was harder to understand the sequencing... :/

##        logger.debug(("DynamicNetwork.evolveTo(): Requesting our Hamiltonian %s "
##                      "to evolve to time-step %d...") % (str(self.hamiltonian), timestep))
##        self.hamiltonian.evolveTo(timestep)

        # Get the list of nodes in this network.

    @property
    def nodes(me):
        if hasattr(me, '_nodes'):
            return me._nodes
        else:
            return []

    def node(self, nodeName:str):
        if nodeName in self.nodes:
            return self._nodes[nodeName]
        else:
            return None
            #raise NoSuchNode("There is no node named %s in network %s" % (nodeName, str(self)))

    #-- inst.test() - Test this network by initializing it and then
    #       simulating it forwards in time a few steps.

    def test(self):

        if doInfo:
            logger.info("Thermalizing network '%s' to unit temperature..." % str(self))

            # Initialize the network by thermalizing the
            # generalized momenta of all coordinates.
        
        self.thermalize(1.0)    # Temperature units are arbitrary for now.

            # Simulate the network forwards for a few time-steps.

        if doInfo:
            logger.info("Evolving network '%s' forwards ten time-steps..." % str(self))

        for t in range(10):
            self.evolveTo(t)       # Just a few steps, to exercise things.

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
# (Should we throw a WarningException in this case instead??)

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
