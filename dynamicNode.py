import logmaster
logger = logmaster.getLogger(logmaster.sysName + '.network')

from dynamicCoordinate import DynamicCoordinate

class DynamicNetwork: pass  # Forward declaration to avoid circularity

class NodeNameCollision(Exception): pass

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

    def __init__(inst, network:DynamicNetwork, name:str=None):

        logger.debug("Creating a new dynamic node named %s in network %s..." %
                        (name, str(network)))

        inst.network = network      # Remember our network
        
        if name != None:  inst.name = name
        inst.links = []     # Node has an empty list of links initially.

        # Next we create the node's dynamical coordinate, initially
        # having (p,q)=(0,0) at timestep 0.

            # First make sure the network has a Hamiltonian structure
            # attached to it, or else we can't usually start creating
            # dynamical coordinates associated with our nodes.

        network.initHamiltonian()
            
        inst.coord = DynamicCoordinate(network.hamiltonian, name,
                                       context=network.context)

        logger.debug("DynamicNode.__init__(): Coordinate momentum is %f" %
                      inst.coord.ccp._momVar.value)

    def evolveTo(inst, timestep:int):
        logger.debug("Node %s is going to evolve to timestep %d...", inst.name, timestep)
        inst.coord.evolveTo(timestep)

    # The following two methods should really be turned into a .name property...

    def getName(this):      # Get something that can be used as a node name.
        if hasattr(this,'name'):
            return this.name
        else:
            return 'node'

    def renameTo(this, name:str):
        if not hasattr(this, 'name') or this.name != name:

            # Before we rename the node, make sure there is not another node
            # already in this node's network with the same name.  If there is,
            # throw an error (NodeNameCollision).
            
            if this.network != None:
                if this.network.node(name) != None:
                    raise NodeNameCollision("DynamicNode.renameTo(): "
                                            "Can't rename node %s to %s because "
                                            "that name is already used in network %s."
                                            % (str(this), name, str(this.network)))
            
            logger.info("Renaming node '%s' to '%s'" % (str(this), name))
            oldName = this.name
            this.name = name

            this.coord.renameTo(name)

            if this.network != None:
                this.network.noticeNodeNameChange(this, oldName)

    def __str__(this):
        if hasattr(this,'name'):
            return str(this.name)
        else:
            return '(unnamed node)'

    def addLink(this, link):
        this.links.append(link)
        if link.node != this:
            link.node = this

    def removeLink(this, link):
        this.links.remove(link)

    def printInfo(this):
        logger.normal("Detailed information for node %s:" % str(this))
        logger.normal("\tLinks are:")
        for link in this.links:
            link.printInfo()
        logger.normal("\tCoordinate information is:")
        this.coord.printInfo()
        logger.normal("\tNetwork's Hamiltonian is:")
        this.network.hamiltonian.printInfo()
