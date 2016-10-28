
print("In dynamicLink.py")

    # Note that the formal module dependence chain for the basic
    # network classes is as follows:
    #
    #       DynamicNetwork.py
    #               |
    #               V
    #       DynamicComponent.py
    #               |
    #               V
    #       DynamicPort.py
    #               |
    #               V
    #       DynamicLink.py
    #               |
    #               V
    #       DynamicNode.py
    #
    # However, there are circular dependencies between these modules,
    # which are resolved by internal forward references.

from logmaster  import *
from network    import _logger

#import logmaster; from logmaster import *
#_logger = getLogger(logmaster.sysName + '.network')

class DynamicLink: pass

from .dynamicNode    import DynamicNode     as Node

from . import dynamicPort

__all__ = ['DynamicLink']

    # Forward class declarations to avoid circular references.

class Port: pass

class DynamicLink:

    # A rule for links is that the link should correctly refer back to
    # a port or node that it's connecting to or disconnecting from at the
    # time that that connection or disconnection event occurs.

    #-- Instance private data members:
    #
    #       ._port - The component port that this link connects to.
    #       ._node - The node that this link connects to.

    #-- Initializer.  Given a port and a node, first tells
    #       the port that it's connected to this link, then
    #       tells the node that we are one of its links.
    #       These actions set our data members appropriately.

    def __init__(inst, port:Port=None, node:Node=None):

        inst.port = port

        node.addLink(inst)      # This also sets our .node


    @property
    def port(this):
        if hasattr(this,'_port'):
            return this._port
        else:
            return None

    @port.setter
    def port(this, port:Port):
        
        # If we're already connected to some port, disconnect from it first.
        
        if this.port != None:
            del this.port

        # If new port isn't None then set our new port to it.
        
        if port != None:
            this._port = port
            port.connect(this)      # Tell port it's connected to us.

    @port.deleter
    def port(this):
        if this.port != None:
            this.port.disconnect()      # Tell port to disconnect from us.
        del this._port

    @property
    def node(this):
        if hasattr(this,'_node'):
            return this._node
        else:
            return None

    @node.setter
    def node(this, node:Node):

        # If we're already connected to some node, disconnect from it first.

        if this.node != None:
            del this.node

        # If new node isn't None then set our new node to it.

        if node != None:
            this._node = node
                # Are we not already in the node's links?
                # (Watch out for inefficiency here; maybe
                # make the .links list a dictionary, or some
                # efficient set type eventually.)
            if this not in node.links:      
                node.addLink(this)

    @node.deleter
    def node(this):
        if this.node != None:
            this.node.removeLink(this)      # Tell node to disconnect from us.
        del this._node


    def printInfo(this):
        if doInfo:
            _logger.info("\t\tLink: Node %s <-> Port %s" % (str(this.node), str(this.port)))

#__/ End class DynamicLink        
