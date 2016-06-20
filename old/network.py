import numbers  # Defines "Real" class.

#-- In dynamic, a Network consists of:
#
#       A set of dynamic nodes (class Node)
#       A set of component instances (gates and other devices).
#       A set of links connecting ports of components to nodes.
#

class DynamicNetwork:

    #-- Data members:
    #
    #       inst.nodes [list] - The set of nodes in this network.
    #       inst.components [list] - The set of components in this network.
    #       inst.links [list] - The set of links in this network.
    
    def __init__(inst): pass
    
    #== Public instance functions.

    #-- inst.thermalize() - This function randomizes the velocities
    #       of all generalized coordinates in the network according
    #       to a thermal distribution, with an average energy per
    #       degree of freedom of kT.

    def thermalize(inst, temperature:numbers.Real):
        pass
