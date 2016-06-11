
from BaseDifferentiableFunction import *

class DynamicNOTFunction(BaseDifferentiableFunction):

    def __init__(inst, stiffness):

        BaseDifferentiableFunction.__init__(inst)

        inst.setArglist(('x', 'y'))   # y is output

        inst.stiffness = stiffness

        inst.function = lambda (x, y):
            0.5 * inst.stiffness * (x + y - 1)**2

        inst.partials = [
            lambda (x, y):  inst.stiffness * (x + y - 1),   # partial wrt x
            lambda (x, y):  inst.stiffness * (x + y - 1)    # partial wrt y
        ]


class DynamicNOTGate(DynamicTwoTerminalGate):

    #-- This creator DynamicNotGate(inputNode) creates a dynamic
    #   NOT gate with the given input node; the output node is
    #   created.

    def __init__(inst, inputNode, stiffness = 1.0):

            # Do generic initialization for dynamic two-terminal gates.
            # (Create ports & output node, link it to our output port.)

        DynamicTwoTerminalGate.__init__(inst, inputNode)

            # Create the potential energy function relating the input
            # and output nodes.

        notFunc = DynamicNOTFunction(stiffness)

            # Set the interaction function of this DynamicTwoTerminalGate
            # to that function.

        inst.interaction = notFunc
        
            
        
