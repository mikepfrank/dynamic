import port                                 # Port class.
from dynamicNode    import DynamicNode

__all__ = ["Link"]


    # A Link connects a port (of a primitive component) to a node.
    
    # We could have called this "DynamicLink," but there isn't
    # anything very dynamic about it.

class Link:

    #-- Data members:
    #       .port - The component port that this link connects to.
    #       .node - The node that this link connects to.

    #-- Initializer.  Given a port and a node, first tells
    #       the port that it's connected to this link, then
    #       tells the node that we are one of its links.
    #       These actions set our data members appropriately.

    def __init__(inst, port:port.Port, node:DynamicNode):

        port.connect(inst)      # This also sets our .port

        node.addLink(inst)      # This also sets our .node

        
        
