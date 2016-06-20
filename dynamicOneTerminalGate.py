from baseComponent import BaseComponent

#-- A DynamicOneTerminalGate has one node called "output"
#   together with a single built-in potential energy function.
#   It may also have internal coordinates, but is not required to.

class DynamicOneTerminalGate(BaseComponent):

    #-- Data members:
    #       potential [BaseDifferentiableFunction] -
    #           Potential energy function for the
    #           output node's coordinate x.

    #-- To initialize a dynamic one-terminal "gate," we simply
    #   create one port called "output," create a simple dynamic
    #   node to be our output node, and link it to our output port.

    def __init__(inst, inputNode):

            # Create our one port, named "output."

        inst.addPorts(('output',))

            # Create and remember our output node.

        inst.outputNode = DynamicNode()

            # Link our port named "output" to our output node.

        inst.link('output', inst.outputNode)
        
