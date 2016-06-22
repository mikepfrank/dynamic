from dynamicNode    import DynamicNode

__all__ = ['Link', 'Port']

    # Forward class declarations to avoid circular references.
    # This lets us later define these classes in whatever order,
    # despite that fact that their definitions refer to each other.

class Link: pass
class Port: pass

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

    def __init__(inst, port:Port, node:DynamicNode):

        port.connect(inst)      # This also sets our .port

        node.addLink(inst)      # This also sets our .node

 

#-- A port is an interface terminal to a component.
#   A port is connected by a link to an external node.

#   We could have called this a "DynamicPort," but in and of itself,
#   it isn't anything very dynamic.

class Port:

    #-- Data members:
    #       .component   - The component that this is a port of.
    #       .name        - The name of this port (unique within the component).
    #       .connectedTo - The external link that this port connects to.


    def __init__(inst, component, name):

        inst.component = component
        inst.name      = name
        

    def connect(this, link:Link):
        
        this.connectedTo = link
        link.port        = this

        
