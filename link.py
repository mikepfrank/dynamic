
    # A Link connects a port (of a primitive component) to a node.

class Link:

    #-- Data members:
    #       .port - The component port that this link connects to.
    #       .node - The node that this link connects to.

    def __init__(inst, port, node):

        port.connect(inst)      # This also sets our port

        node.addLink(inst)      # This also sets our node

        
        
