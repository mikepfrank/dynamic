
#-- A DynamicTwoTerminalGate has two nodes called "input" and "output"
#   with a single interaction term between them.  It's assumed that there's
#   no internal state other than the position/velocity values associated
#   with the two nodes.

class DynamicTwoTerminalGate(BaseComponent):

    #-- Data members:
    #       interaction [BinaryPotentialEnergyTerm] -
    #           Interaction potential energy function between the
    #           input and output node's coordinates (x,y).

    #-- To initialize a dynamic two-terminal "gate," we simply
    #   create two ports called "input" and "output," create
    #   a simple dynamic node to be our output node, and link
    #   it to our output port.

    def __init__(inst, inputNode):

            # Create our two ports, named "input" and "output".

        inst.addPorts('input', 'output')

            # Create and remember our output node named "out".

        inst.outputNode = DynamicNode('out')

            # Link our port named "output" to our output node.

        inst.link('output', inst.outputNode)
        
