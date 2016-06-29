import logmaster

from quadraticFunction          import QuadraticFunction
from dynamicOneTerminalGate     import DynamicOneTerminalGate
from dynamicNetwork             import DynamicNetwork,netName

logger = logmaster.getLogger(logmaster.sysName + '.network')

class DynamicBiasFunction(QuadraticFunction):

    def __init__(inst, biasval, stiffness):

        # Set coefficients of quadratic function terms accordingly per
        #           0.5k(x-b)^2  =  0.5kx^2 -kbx + 0.5kb^2.

        c2  =    0.5 * stiffness
        c1  =  -       stiffness * biasval
        c0  =    0.5 * stiffness * biasval**2

        QuadraticFunction.__init__(inst, name='B', c2=c2, c1=c1, c0=c0)

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

    def __init__(inst, name:str=None, network:DynamicNetwork=None, biasval = 0.0, stiffness = 1.0):

        netname = netName(network)

        logger.debug("Initializing a new DynamicMemCell named '%s' in network '%s'" %
                     (str(name), netname))

            # Do generic initialization for dynamic one-terminal gates.
            # (Create port & output node, link it to our output port.)

        DynamicOneTerminalGate.__init__(inst, name=name, network=network)

            # Create the potential energy function relating the input
            # and output nodes.

        logger.debug(("Setting up %s's dynamic bias function with bias "+
                      "value %f and stiffness %f...") %
                          (str(inst), biasval, stiffness))

        biasFunc = DynamicBiasFunction(biasval, stiffness)

            # Set the potential function of this DynamicOneTerminalGate
            # to that function.

        inst.potential = biasFunc

        logger.debug("DynamicMemCell.__init__(): Output node momentum is: %f" % 
                      inst.outputNode.coord.ccp._momVar.value)

        
