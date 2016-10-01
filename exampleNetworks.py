#|==============================================================================
#|                      TOP OF FILE:    exampleNetworks.py
#|------------------------------------------------------------------------------
#|   The below module documentation string will be displayed by pydoc3.
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""

    FILE NAME:              exampleNetworks.py     [Python 3 module source code]

    MODULE NAME:            exampleNetworks

    SOFTWARE SYSTEM:        Dynamic (simulator for dynamic networks)

    SOFTWARE COMPONENT:     Dynamic.examples


    MODULE DESCRIPTION:
    -------------------

        This module simply defines a few hard-coded examples of
        Dynamic networks, for testing purposes.


    MODULE USAGE:
    -------------

        First, create a simulation context for the simulator:

            sc = SimulationContext()

        Next, instantiate one of the example network classes,
        passing it the simulation context:

            net = exampleNetworks.MemCellNet(context=sc)

        At this point, you can tell the simulation context
        to run a self-test:

            sc.test()


    PUBLIC CLASSES:
    ---------------

        exampleNetworks.MemCellNet                         [module public class]

            (The following still need to be implemented)

        exampleNetworks.NotGateNet                         [module public class]

        exampleNetworks.AndGateNet                         [module public class]

        exampleNetworks.HalfAdderNet                       [module public class]

            (The following still needs to be tested)

        exampleNetworks.FullAdderNet                       [module public class]


    Module revision history:
    ------------------------

        v0.1 (2016-07) [mpf] - Initial revision; MemCellNet tested.


    Work to do/in progress:
    -----------------------

        [ ] Implement and test larger networks. (>1 node)
                                                                             """
#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#| End of module documentation string.
#|------------------------------------------------------------------------------

    #|==========================================================================
    #|   1. Module imports.                                [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|  1.1. Imports of custom application modules. [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    #-----------------------------------------------------------------
    # Import our logging facility, and create a logger for the present
    # software component (Dynamic.examples), which we will use.

import logmaster; from logmaster import *
_logger = getLogger(logmaster.sysName + '.examples')


from fixed import Fixed

    #------------------------------------------------------------------
    # Import some names we'll reference from various simulator modules.

from dynamicNetwork     import  DynamicNetwork, netName     # Dynamic networks.
from dynamicMemCell     import  DynamicMemCell              # Memory-cell component.
from dynamicNOTGate     import  DynamicNOTGate              # Inverter component.
from dynamicANDGate     import  DynamicANDGate              # AND gate component.
from simulationContext  import  SimulationContext           # Context for simulation.


    #|==========================================================================
    #|  2.  Global constants, variables, and objects.      [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|  2.1.  Special globals.                      [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            #|------------------------------------------------------------------
            #|
            #|   exampleNetworks.__all__:List[str]              [special global]
            #|
            #|      List of explicitly exported public names.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

__all__ = [
    'MemCellNet',       # A single memory cell, one output node.
    'NotGateNet',       # A memory cell feeding a NOT gate.  Two nodes.
    'AndGateNet',       # Two memory cells feeding an AND gate.  Three nodes.
    'HalfAdderNet',     # A half-adder.  Four nodes.  Two inputs, two outputs.
    'FullAdderNet',     # A full-adder.  Six nodes.  Three inputs, two outputs, one internal node.
    ]
    

    #|==========================================================================
    #|
    #|  3.  Class definitions.                             [module code section]
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|
        #|   3.1.  Normal public classes.               [module code subsection]
        #|
        #|      In this code section, we define our public classes
        #|      (other than exception classes).
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            #|------------------------------------------------------------------
            #|
            #|  MemCellNet(dynamicNetwork.DynamicNetwork)         [public class]
            #|                                                  
            #|      This specialized subclass of DynamicNetwork
            #|      creates a very simple dynamic network, pretty
            #|      much the simplest possible non-empty network.
            #|      It includes just a single dynamic memory cell
            #|      with a single output node.  This is mainly only
            #|      useful for testing during initial development.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class MemCellNet(DynamicNetwork):
    
    """This specialized subclass of DynamicNetwork creates a very
       simple dynamic network, pretty much the simplest possible
       non-empty network.  It includes just a single dynamic memory
       cell with a single output node.  This is mainly only useful
       for testing during initial development.

            USAGE:
            ------
            
                sc = simulationContext.SimulationContext()
                net = exampleNetworks.MemCellNet(sc)
                sc.test()
                                                                             """

        #|----------------------------------------------------------------------
        #|(in class MemCellNet)
        #|
        #|      Private instance attributes.          [class code documentation]
        #|      ----------------------------
        #|
        #|          inst._memCell [DynamicMemCell]      [private object attrib.]
        #|
        #|              This private attribute allows remembering and
        #|              easily accessing the DynamicMemCell object
        #|              that is the single component within this
        #|              network.
        #|
        #|----------------------------------------------------------------------
    

    def __init__(inst, context:SimulationContext=None):
        
        """This initializer contains just one argument, a simulation
           context, and it creates a new dynamic memory cell "network"
           (a single cell with a single output node) in that context."""

            # Verbose diagnostics (entering this initializer).

        if doDebug:
            _logger.debug("Initializing a new exampleNetworks.MemCellNet in "
                          "simulation context %s..." % str(context))

            #--------------------------------------------------------
            # First, do generic initialization for dynamic networks.
            # This sets a default short name and long title for the
            # network, and initializes internal data structures.

        DynamicNetwork.__init__(inst,
                                name='exampleNet_dynMemCell',
                                title="Example network: Dynamic memory cell",
                                context=context)

        netname = netName(inst)     # Should retrieve name set above.

            #---------------------------------------------------------
            # Next, go ahead and create our single dynamic memory cell
            # and add it to the network.

        if doDebug:
            _logger.debug("Creating a new DynamicMemCell in network "
                          "'%s'..." % netname)
        
        inst._memCell = DynamicMemCell('memcell', network=inst)

    #__/ End method MemCellNet.__init__().
        
#__/ End class MemCellNet.

            #|------------------------------------------------------------------
            #|
            #|  InverterNet(dynamicNetwork.DynamicNetwork)        [public class]
            #|                                                  
            #|      This specialized subclass of DynamicNetwork
            #|      creates a simple dynamic network which contains
            #|      just a single dynamic memory cell feeding a
            #|      single dynamic NOT gate.  This is mainly only
            #|      useful for testing during initial development.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class InverterNet(DynamicNetwork):
    
    def __init__(inst, context:SimulationContext=None):
        
        DynamicNetwork.__init__(inst, name='exampleNet_inverter',
                                title="Example network: Inverter",
                                context=context)
        
        netname = netName(inst)     # Should retrieve name set above.

        inst._memCell = DynamicMemCell('memcell', network=inst)

        inNode = inst._memCell.outputNode     # Output node of memcell = input to inverter.

        if doNorm:
            _logger.normal("Before creating NOT gate, input node details are:")
            inNode.printInfo()  # Temporary diagnostic for debugging.

        inNode.renameTo('X')    # Call the inverter's input node 'X'.

        if doNorm:
            _logger.normal("Renamed input node from q to X; now its details are:")
            inNode.printInfo()

        inst._notGate = DynamicNOTGate(inNode, 'notgate', network=inst)

        outNode = inst._notGate.outputNode

        outNode.renameTo('Y')   # Call the inverter's output node 'Y'.
        outNode.coord.position.value = Fixed(1)

        if doNorm:
            _logger.normal("Finished creating %s.  Now input node details are:" % netname)        
            inNode.printInfo()  # Temporary diagnostic for debugging.

            _logger.normal("Meanwhile, output node details are:")    
            outNode.printInfo()  # Temporary diagnostic for debugging.

    #__/ End method InverterNet.__init__().

    def printDiagnostics(me):
        if doNorm:
            _logger.normal("%d, %.9f, %d, %.9f, %d, %.9f, %d, %.9f" %
                          (me.nodes['X'].coord.position.time,
                           me.nodes['X'].coord.position(),
                           me.nodes['X'].coord.momentum.time,
                           me.nodes['X'].coord.momentum(),
                           me.nodes['Y'].coord.position.time,
                           me.nodes['Y'].coord.position(),
                           me.nodes['Y'].coord.momentum.time,
                           me.nodes['Y'].coord.momentum()
                           ))
        

#__/ End class InverterNet.


class AndGateNet(DynamicNetwork):
    
    def __init__(me, context:SimulationContext=None):

        DynamicNetwork.__init__(me, name='exampleNet_andGate',
                                title="Example network: AND gate",
                                context=context)

        netname = netName(me)   # Should retrieve name set above.

        me._memCellA = memCellA = DynamicMemCell('memcellA', network=me, biasval=0.0)
        me._nodeA = nodeA = memCellA.outputNode
        nodeA.renameTo('A')
        #nodeA.coord.position.value = Fixed(1)
        
        me._memCellB = memCellB = DynamicMemCell('memcellB', network=me, biasval=1.0)
        me._nodeB = nodeB = memCellB.outputNode
        nodeB.renameTo('B')
        nodeB.coord.position.value = Fixed(1)

        me._andGate = andGate = DynamicANDGate(nodeA, nodeB, 'andgate', network=me)
        me._nodeQ = nodeQ = andGate.nodeC
        nodeQ.renameTo('Q')
        #nodeQ.coord.position.value = Fixed(1)

    def printDiagnostics(me):
        if doNorm:
            _logger.normal("%d, %.9f, %d, %.9f, %d, %.9f, %d, %.9f, %d, %.9f, %d, %.9f" %
                           (me.nodes['A'].coord.position.time,
                            me.nodes['A'].coord.position(),
                            me.nodes['A'].coord.momentum.time,
                            me.nodes['A'].coord.momentum(),
                            me.nodes['B'].coord.position.time,
                            me.nodes['B'].coord.position(),
                            me.nodes['B'].coord.momentum.time,
                            me.nodes['B'].coord.momentum(),
                            me.nodes['Q'].coord.position.time,
                            me.nodes['Q'].coord.position(),
                            me.nodes['Q'].coord.momentum.time,
                            me.nodes['Q'].coord.momentum()
                            ))

    def initStats(me):
        me.nSamples = 0
        me.totalA = Fixed(0)
        me.totalB = Fixed(0)
        me.totalQ = Fixed(0)

    def gatherStats(me):
        me.nSamples += 1
        me.totalA += me.nodes['A'].coord.position()
        me.totalB += me.nodes['B'].coord.position()
        me.totalQ += me.nodes['Q'].coord.position()

    def printStats(me):
        if doNorm:
            _logger.normal("Average positions:  A = %f, B = %f, Q = %f" %
                           ((me.totalA / me.nSamples),
                            (me.totalB / me.nSamples),
                            (me.totalQ / me.nSamples)))
                        

        # ***** CONTINUE CLEANUP BELOW HERE *****
        

#-- This example network includes a full adder whose
#   input nodes are output by memory cells.  NOT YET TESTED.

class FullAdderNet(DynamicNetwork):

    def __init__(inst):

        # First do generic initialization for dynamic networks.
        DynamicNetwork.__init__(inst)

        #-- Create 3 dynamic memory cells to hold the network's input.
        Ma = DynamicMemCell(inst)
        Mb = DynamicMemCell(inst)
        Mc = DynamicMemCell(inst)

        #-- Get our 3 input nodes (which are output nodes of those cells).
        a = Ma.outputNode
        b = Mb.outputNode
        c = Mc.outputNode

        #-- Create a full-adder operating on those nodes.        
        FA = FullAdder(inst,a,b,c)
        
        
