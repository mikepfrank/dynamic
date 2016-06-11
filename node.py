class DynamicNode:

    #-- Data members:
    #
    #       links - A tuple of links that connect to this node.
    #               The other end of each link is a port of a component.
    #
    #       coord - Coordinate object associated with this node.

    def __init__(inst):
        inst.links = ()     # Node has an empty tuple of links initially.

        inst.coord = Coordinate()   # Create the node's coordinate, initially (0,0).

    def addLink(this, link):

        this.links = this.links + (link,)

        link.node = this

