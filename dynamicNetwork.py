import numbers  # Defines "Real" class.

#-- In dynamic, a Network consists of:
#
#       A set of named dynamic nodes (class Node)
#       A set of primitive component instances (gates and other devices).
#       A set of links connecting ports of components to nodes.
#

class DynamicNetwork:

    #-- Data members:
    #
    #       inst.nodes [dict] - Map from node names to objects in this network.
    #       inst.components [list] - The set of components in this network.
    #       inst.links [list] - The set of links in this network.
    
    def __init__(inst):
        
    
    #== Public instance functions.

    #-- inst.thermalize() - This function randomizes the velocities
    #       of all generalized coordinates in the network according
    #       to a thermal distribution, with an average energy per
    #       degree of freedom of kT.

    def thermalize(inst, temperature:numbers.Real):
        pass
