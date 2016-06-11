
from BaseDifferentiableFunction import *

class DynamicBiasFunction(BaseDifferentiableFunction):

    def __init__(inst, biasval, stiffness):

        BaseDifferentiableFunction.__init__(inst)

        inst.setArglist(('x',))   # x is output

        inst.biasval = biasval
        inst.stiffness = stiffness

        inst.function = lambda (x):
            0.5 * inst.stiffness * (x - inst.biasval)**2

        inst.partials = [
            lambda (x, y):  inst.stiffness * (x - inst.biasval)   # partial wrt x
        ]

class DynamicMemCell(DynamicOneTerminalGate):

    #-- This creator DynamicMemCell() creates a dynamic
    #   memory cell; the output node is also created.

    def __init__(inst, inputNode, biasval = 0.0, stiffness = 1.0):

            # Do generic initialization for dynamic one-terminal gates.
            # (Create port & output node, link it to our output port.)

        DynamicOneTerminalGate.__init__(inst)

            # Create the potential energy function relating the input
            # and output nodes.

        biasFunc = DynamicBiasFunction(biasval, stiffness)

            # Set the potential function of this DynamicOneTerminalGate
            # to that function.

        inst.potential = biasFunc

            
        
