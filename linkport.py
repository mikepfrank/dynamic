import logmaster
_logger = logmaster.getLogger(logmaster.sysName + '.network')

from dynamicNode    import DynamicNode

__all__ = ['Link', 'Port']

    # Forward class declarations to avoid circular references.
    # This lets us later define these classes in whatever order,
    # despite that fact that their definitions refer to each other.

class Link: pass
class Port: pass

#-- A port is an interface terminal to a component.
#   A port is connected by a link to an external node.

#   We could have called this a "DynamicPort," but in and of itself,
#   it isn't anything very dynamic.

class Port:

    #-- Instance public data members:
    #
    #       .component   - The component that this is a port of.
    #       .name        - The name of this port (unique within the component).
    #       .link        - The external link that this port connects to.

    def __init__(inst, component, name):
        inst.component = component
        inst.name      = name
        
    def connect(this, link:Link):
        if link == None:
            this.disconnect()
        else:
            this.link = link

    def disconnect(this):
        del this.link

    @property
    def linked(this):
        return (hasattr(this,'link') and
                this.link != None and
                this.link.node != None)

    def __str__(this):
        return "%s(%s)" % (this.name, str(this.component))

    # A Link connects a port (of a primitive component) to a node.
    
    # We could have called this "DynamicLink," but there isn't
    # anything very dynamic about it.

class Link:

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

    def __init__(inst, port:Port=None, node:DynamicNode=None):

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
    def node(this, node:DynamicNode):

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
        _logger.normal("\t\tLink: Node %s <-> Port %s" % (str(this.node), str(this.port)))
        
