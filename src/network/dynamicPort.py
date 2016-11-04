#print("In dynamicPort.py")

from logmaster  import *
from network    import _logger

#import logmaster; from logmaster import *
#_logger = getLogger(logmaster.sysName + '.network')


class DynamicPort: pass

from    .dynamicNode    import  DynamicNode as  Node
from    .dynamicLink    import  DynamicLink as  Link

from .dynamicComponent import DynamicComponent as Component


__all__ = ['DynamicPort']

#-- A port is an interface terminal to a component.
#   A port is connected by a link to an external node.

#   We call this a "DynamicPort," but in and of itself,
#   it isn't anything very dynamic.

print("Defining DynamicPort")
class DynamicPort:

    #-- Instance public data members:
    #
    #       .component   - The component that this is a port of.
    #       .name        - The name of this port (unique within the component).
    #       .link        - The external link that this port connects to.

    def __init__(inst, component:Component, name):
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

