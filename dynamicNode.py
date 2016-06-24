from dynamicCoordinate import DynamicCoordinate

#   In Dynamic, a (simple) "node" has the following features (at least):
#
#       * A name (optional)
#
#       * A list of links to ports of primitive components
#           in the network that interact with this node.
#
#       * A generalized-position coordinate variable (a.k.a.
#           degree of freedom).  (This is a smart object that
#           has an associated effective mass and kinetic
#           energy function, and knows how to update itself.)
#
#   This class may later be extended by derived classes that could
#   (for example) add additional coordinate variables.

class DynamicNode:

    #-- Data members:
    #
    #       name - The name of this node within the network that
    #               it's a part of.
    #
    #       links - A tuple of links that connect to this node.
    #               The other end of each link is a port of a component.
    #
    #       coord - Coordinate object associated with this node.

    # Initializer.  If the <name> argument is provided, it is used
    #   to initialize the node's .name data member.  Initially the
    #   node has an empty list of links.

    def __init__(inst, name=None):

        if name != None:  inst.name = name
        
        inst.links = []     # Node has an empty list of links initially.

        inst.coord = DynamicCoordinate(name)   # Create the node's coordinate, initially (0,0).

    def getName(this):      # Get something that can be used as a node name.
        if hasattr(this,'name'):
            return this.name
        else:
            return 'node'

    def renameTo(this, name:str):

        if not hasattr(this, 'name') or this.name != name:
            logger.debug("Renaming node '%s' to '%s'" % (str(this), name))
            inst.name = name

    def __str__(this):

        if hasattr(this,'name'):
            return str(this.name)
        else:
            return '(unnamed node)'

    def addLink(this, link):

        this.links.append(link)

        link.node = this

