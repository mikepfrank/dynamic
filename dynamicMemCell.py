from quadraticFunction          import QuadraticFunction
from dynamicOneTerminalGate     import DynamicOneTerminalGate

class DynamicBiasFunction(QuadraticFunction):

    def __init__(inst, biasval, stiffness):

        # Set coefficients of quadratic function terms accordingly per
        #           0.5k(x-b)^2  =  0.5kx^2 -kbx + 0.5kb^2.

        c2  =    0.5 * stiffness
        c1  =  -       stiffness * biasval
        c0  =    0.5 * stiffness * biasval**2

        QuadraticFunction.__init__(inst, c2, c1, c0)

        # Remember the bias value and stiffness for future reference.

        inst.biasval   = biasval
        inst.stiffness = stiffness

##        inst.function = lambda (x):
##            0.5 * inst.stiffness * (x - inst.biasval)**2
##
##        inst.partials = [
##            lambda (x, y):  inst.stiffness * (x - inst.biasval)   # partial wrt x
##        ]

class DynamicMemCell(DynamicOneTerminalGate):

    #-- This creator DynamicMemCell() creates a dynamic
    #   memory cell; the output node is also created.
    #   By default we have zero bias, and unit "stiffness."

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


        
