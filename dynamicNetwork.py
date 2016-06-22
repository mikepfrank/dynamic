from dynamicNode        import DynamicNode
from dynamicComponent   import DynamicComponent
from linkport           import Link 
from numbers            import Real    # Used by DynamicNetwork.thermalize().

__all__ = ["DynamicNetwork"]

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
    
    def __init__(inst):

        inst._nodes = dict()    # Initially empty set of nodes.
        inst._components = []   # Initially empty list of components.
        inst._links = []        # Initially empty list of links.

        inst._hamiltonian = None    # Initially null Hamiltonian.

        inst._seqno = 0     # Initial sequence number for node names is 0.
    
    #== Public instance methods.

    #-- inst.addComponent(part:BaseComponent) - Adds the given
    #       discrete component (and its connected nodes) to the
    #       network.

    def addComponent(self, part:DynamicComponent):
        pass
    
    #-- inst.addNode(node:DynamicNode) - Adds the given node to the
    #       network (and its connected links).  If no name is provided,
    #       use the existing name; if the name is not unique, append
    #       a sequence number chosen to make it unique.

    def addNode(self, node:DynamicNode, nodeName:str=None):
        pass

    #-- inst.addLink(link:Link) - Add the given link to the network
    #       (and its connected items).

    def addLink(self, link:Link):
        pass

    #-- inst.evolveTo() - Evolve the state of all generalized position
    #       variables in the network forwards to the given timestep.

    def evolveTo(self, timestep:int):
        pass

    #-- inst.test() - Test this network by initializing it and then
    #       simulating it forwards in time a few steps.

    def test(self):

            # Initialize the network by thermalizing the
            # generalized momenta of all coordinates.
        
        self.thermalize(1.0)    # Temperature units are arbitrary for now.

            # Simulate the network forwards for a few time-steps.
        
        self.evolveTo(10)       # Just a few steps, to exercise things.

    #-- inst.thermalize() - This function randomizes the velocities
    #       of all generalized coordinates in the network according
    #       to a thermal distribution, with an average energy per
    #       degree of freedom of kT.

    def thermalize(inst, temperature:Real):
        pass
