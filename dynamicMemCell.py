import logmaster
from logmaster import *

from quadraticFunction          import QuadraticFunction
from dynamicOneTerminalGate     import DynamicOneTerminalGate
from dynamicNetwork             import DynamicNetwork,netName
from dynamicBiasFunction        import DynamicBiasFunction

logger = getLogger(logmaster.sysName + '.network')

class DynamicMemCell(DynamicOneTerminalGate):

    #-- This creator DynamicMemCell() creates a dynamic
    #   memory cell; the output node is also created.
    #   By default we have zero bias, and unit "stiffness."

    def __init__(inst, name:str=None, network:DynamicNetwork=None,
                 biasval = 0.0, stiffness = 1.0, outNodeName:str=None):

        netname = netName(network)

        if doDebug:
            logger.debug("Initializing a new DynamicMemCell named '%s' in network '%s'" %
                         (str(name), netname))

            # Do generic initialization for dynamic one-terminal gates.
            # (Create port & output node, link it to our output port.)

        DynamicOneTerminalGate.__init__(inst, name=name, network=network,
                                        outNodeName=outNodeName)

            # Create the potential energy function relating the input
            # and output nodes.

        if doDebug:
            logger.debug(("Setting up %s's dynamic bias function with bias "+
                          "value %f and stiffness %f...") %
                              (str(inst), biasval, stiffness))

        biasFunc = DynamicBiasFunction(biasval, stiffness)

            # Set the potential function of this DynamicOneTerminalGate
            # to that function.

        inst.potential = biasFunc

        if doDebug:
            logger.debug("DynamicMemCell.__init__(): Output node momentum is: %f" % 
                          inst.outputNode.coord.momentum.value)

            # Initialize position to minimum-energy value.

        if biasval != 0:
            inst.outputNode.coord.position.value = biasval

    #__/ End DynamicMemCell.__init__()

#__/ End class DynamicMemCell
