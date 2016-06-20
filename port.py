from link import Link

__all__ = ["Port"]

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

        
