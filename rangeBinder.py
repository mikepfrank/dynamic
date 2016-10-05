# A RangeBinder is a dynamic one-terminal component that attaches
# to each node and keeps its value from drifting too far outside
# the range [0,1].  

import logmaster; from logmaster import *

from doubleWellFunction          import DoubleWellFunction

from dynamicNode                 import DynamicNode
from dynamicOneTerminalComponent import DynamicOneTerminalComponent
from dynamicNetwork              import DynamicNetwork,netName

logger = getLogger(logmaster.sysName + '.network')

class RangeBinder(DynamicOneTerminalComponent):

    #-- This initialize creates a range binder component.
    #   This has a double-well potential at 0 and 1.
    #   Default "stiffness" is 1/4 that of a memory cell

    def __init__(inst, node:DynamicNode, name:str=None,
                 network:DynamicNetwork=None,
                 stiffness = 1/4, outNodeName:str=None):

        if network is None:  network = node.network

        netname = netName(network)

        if doDebug:
            logger.debug("Initializing a new RangeBinder named '%s' in network '%s'" %
                         (str(name), netname))

            # Do generic initialization for dynamic one-terminal gates.
            # (Create port & output node, link it to our output port.)

        DynamicOneTerminalComponent.__init__(inst, node, name=name, network=network)

            # Create the double-well potential which keeps the value from
            # drifting too far from valid logic levels

##        if doDebug:
##            logger.debug(("Setting up %s's dynamic bias function with bias "+
##                          "value %f and stiffness %f...") %
##                              (str(inst), biasval, stiffness))

        doubleWell = DoubleWellFunction(0.0, 1.0, stiffness)

            # Set the potential function of this RangeBinder
            # to that function.

        inst.potential = doubleWell

        if doDebug:
            logger.debug("RangeBinder.__init__(): Output node momentum is: %f" % 
                          inst.node.coord.momentum.value)

    #__/ End RangeBinder.__init__()

#__/ End class RangeBinder

    
