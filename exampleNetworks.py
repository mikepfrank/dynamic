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

import logmaster
_logger = logmaster.getLogger(logmaster.sysName + '.examples')


    #------------------------------------------------------------------
    # Import some names we'll reference from various simulator modules.

from dynamicNetwork     import  DynamicNetwork, netName     # Dynamic networks.
from dynamicMemCell     import  DynamicMemCell              # Memory-cell component.
from dynamicNOTGate     import  DynamicNOTGate              # Inverter component.
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

        _logger.debug("Creating a new DynamicMemCell in network "
                      "'%s'..." % netname)
        
        inst._memCell = DynamicMemCell('memcell', network=inst)

    #__/ End method MemCellNet.__init__().
        
#__/ End class MemCellNet.

class InverterNet(DynamicNetwork):
    def __init__(inst, context:SimulationContext=None):
        DynamicNetwork.__init__(inst, name='exampleNet_inverter',
                                title="Example network: Inverter",
                                context=context)
        netname = netName(inst)     # Should retrieve name set above.

        inst._memCell = DynamicMemCell('memcell', network=inst)

        inNode = inst._memCell.outputNode     # Output node of memcell = input to inverter.

        inNode.renameTo('p')    # Call the inverter's input node 'p'.

        inst._notGate = DynamicNOTGate(inNode, 'notgate', network=inst)

        outNode = inst._notGate.outputNode

        outNode.renameTo('q')   # Call the inverter's output node 'q'.
    
    #__/ End method InverterNet.__init__().

#__/ End class InverterNet.
        

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
        
        
