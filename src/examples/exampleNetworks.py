#|==============================================================================
#|                      TOP OF FILE:    exampleNetworks.py
#|------------------------------------------------------------------------------
#|   The below module documentation string will be displayed by pydoc3.
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""
    FILE NAME:              exampleNetworks.py       [Python module source code]

    FILE PATH:              $GIT_ROOT/dynamic/src/examples/exampleNetworks.py

    MODULE NAME:            examples.exampleNetworks

    SOFTWARE SYSTEM:        Dynamic (simulator for dynamic networks)

    SOFTWARE COMPONENT:     Dynamic.examples


    MODULE DESCRIPTION:
    -------------------

        This module simply defines a few hard-coded examples of
        Dynamic networks, for testing purposes.


    BASIC MODULE USAGE:
    -------------------

        First, create a simulation context for the simulator:

            sc = SimulationContext()

        Next, instantiate one of the example network classes,
        passing it that simulation context.  The new network
        will be created within that context.

            net = exampleNetworks.FullAdderNet(context=sc)

        At this point, you can tell the simulation context
        to run a self-test, which will simulate the given
        network for a number of steps:

            sc.test()


    PUBLIC CLASSES:
    ---------------

        See the classes' docstrings for details.

            exampleNetworks.MemCellNet                     [module public class]

                A network consisting of a single memory cell.

            exampleNetworks.NotGateNet                     [module public class]

                A network consisting of a memory cell feeding a NOT
                gate.

            exampleNetworks.AndGateNet                     [module public class]

                A network consisting of two memory cells feeding a 2-
                input AND gate.

            exampleNetworks.HalfAdderNet                   [module public class]

                A network consisting of two memory cells feeding a
                half adder circuit (an AND gate and an XOR gate in
                parallel).

            exampleNetworks.FullAdderNet                   [module public class]

                A network consisting of three memory cells feeding a
                5-gate full adder circuit.


    Module dependencies:
    --------------------

        This module depends on the following other Dynamic modules:

            logmaster               - Logging facility
            fixed                   - Fixed-point arithmetic
            examples                - Parent package
            network.dynamicNetwork  - Dynamic networks
            examples.dynamicMemCell - Read-only memory cells
            boolean.dynamicNOTGate  - Inverter components
            boolean.dynamicANDGate  - AND gate components
            boolean.dynamicORGate   - OR gate components
            boolean.dynamicXORGate  - XOR gate components
            

    Module revision history:
    ------------------------

        v0.1 (2016-07) [mpf] - Initial revision; MemCellNet tested.
        v0.2 (2016-10) [mpf] - Examples through FullAdderNet built & work.


    Work to do/in progress:
    -----------------------

        [/] Implement and test larger networks. (>1 node)
        [ ] Create and test alternative implementations of some functions.
                                                                             """
#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#| End of module documentation string for exampleNetworks.py.
#|------------------------------------------------------------------------------

    #|==========================================================================
    #|   1. Module imports.                                [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #------------------------------------------
        # Imports from our parent module (package).

from . import _logger       # Our component logger.


        #-----------------------------------------------------------
        # Imports some names we'll reference from custom modules in
        # this package and other, lower-level packages within the
        # Dynamic system.

from    logmaster   import  doDebug, doNorm   # Whether to show debug/normal output.
from    fixed       import  Fixed     # Our custom class for fixed-point numbers.

from    network.dynamicNetwork      import  DynamicNetwork, netName     # Dynamic networks.
from    .dynamicMemCell             import  DynamicMemCell              # Memory-cell component.
from    boolean.dynamicNOTGate      import  DynamicNOTGate              # Inverter component.
from    boolean.dynamicANDGate      import  DynamicANDGate              # AND gate component.
from    boolean.dynamicORGate       import  DynamicORGate               # OR gate component.
from    boolean.dynamicXORGate      import  DynamicXORGate              # XOR gate component.
from    simulator.simulationContext import  SimulationContext           # Context for simulation.


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

global __all__          # List of public symbols exported by this module.

__all__ = [
    'MemCellNet',       # A single memory cell, one output node.
    'NotGateNet',       # A memory cell feeding a NOT gate.  Two nodes.
    'AndGateNet',       # Two memory cells feeding an AND gate.  Three nodes.
    'HalfAdderNet',     # A half-adder.  Four nodes.  Two inputs, two outputs.
    'FullAdderNet',     # A full-adder.  Six nodes.  Three inputs, two outputs, one internal node.
    ]
    

    #|==========================================================================
    #|  3.  Class definitions.                             [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|   3.1.  Normal public classes.               [module code subsection]
        #|
        #|      In this code section, we define our public classes
        #|      (other than exception classes).
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
    
    """
        This specialized subclass of DynamicNetwork creates a very
        simple dynamic network, pretty much the simplest possible
        non-empty network.  It includes just a single dynamic memory
        cell with a single output node.  This is mainly only useful
        for testing during initial development.

            Network diagram:
            ----------------       
                 _________        
                |         |    inst._outNode
                | memcell |-->@
                |_________|      
       

            Basic class usage:
            ------------------

                from simulator.simulationContext import SimulationContext
                from examples.exampleNetworks import MemCellNet
            
                sc = SimulationContext()
                net = MemCellNet(sc)
                sc.test()
                                                                             """

    #|--------------------------------------------------------------------------
    #|(in class MemCellNet)
    #|
    #|      Private instance attributes.              [class code documentation]
    #|      ----------------------------
    #|
    #|          inst._memCell : DynamicMemCell          [private object attrib.]
    #|
    #|              This private attribute allows remembering and
    #|              easily accessing the DynamicMemCell object
    #|              that is the single component within this
    #|              network.
    #|
    #|          inst._outNode : DynamicNode             [private object attrib.]
    #|
    #|              The node that is the output of the memory cell.
    #|
    #|--------------------------------------------------------------------------
    
        #|----------------------------------------------------------------------
        #|
        #|  inst.__init__()                            [special instance method]
        #|
        #|      This initializer takes one optional argument, a
        #|      simulation context, and it creates a new dynamic
        #|      memory cell "network" (consisting of a single cell
        #|      with a single output node) in that context.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def __init__(inst, context:SimulationContext=None):
        
        """This initializer takes one optional argument, a simulation
           context, and it creates a new dynamic memory cell "network"
           (consisting of a single cell with a single output node) in
           that context."""

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

            #---------------------------------------------------------
            # Next, go ahead and create our single dynamic memory cell
            # and add it to the network.

        if doDebug:     # Maybe do diagnostics.
            
            netname = netName(inst)     # Should retrieve name set above.

            _logger.debug("Creating a new DynamicMemCell in network "
                          "'%s'..." % netname)
            
        #__/ End if doDebug.
        
        inst._memCell = memCell = DynamicMemCell('memcell', network=inst)

        inst._outNode = memCell.outputNode

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

    """
        This specialized subclass of DynamicNetwork creates a simple
        dynamic network which contains just a single dynamic memory
        cell feeding a single dynamic NOT gate.  This is mainly only
        useful for testing during initial development.

            Network diagram:
            ----------------       
                 _________         _________
                |         |   X   |         |   Y
                | memcell |-->@-->| notgate |-->@-->
                |_________|       |_________|
       
                                                                      """

    #|--------------------------------------------------------------------------
    #|[In class InverterNet]
    #|
    #|  Private instance attributes:
    #|  ----------------------------
    #|
    #|  Maybe later we will make some of these public.
    #|
    #|      inst._memCell : DynamicMemCell            [private object attribute]
    #|
    #|          The memory cell component that feeds the inverter input.
    #|
    #|      inst._notGate : DynamicNOTGate            [private object attribute]
    #|
    #|          The inverter component.
    #|
    #|      inst._inNode : DynamicNode                [private object attribute]
    #|
    #|          The input node to the inverter.
    #|
    #|      inst._outNode : DynamicNode               [private object attribute]
    #|
    #|          The output node from the inverter.
    #|
    #|--------------------------------------------------------------------------
    
    def __init__(inst, context:SimulationContext=None):
        
        """This initializer takes one optional argument, a simulation
           context, and it creates a new dynamic inverter "network"
           (consisting of a memory cell feeding an inverter) in that
           context."""

            #--------------------------------------------------------
            # First, do generic initialization for dynamic networks.
            # This sets a default short name and long title for the
            # network, and initializes internal data structures.

        DynamicNetwork.__init__(inst, name='exampleNet_inverter',
                                title="Example network: Inverter",
                                context=context)

            #---------------------------------------------------------
            # Create and remember the dynamic memory cell component.
            # Also remember its output node.
        
        inst._memCell = memCell = DynamicMemCell('memcell', network=inst)

        inst._inNode = inNode = memCell.outputNode     # Output node of memcell = input to inverter.

            #----------------------------
            # Maybe do some diagnostics.

        if doDebug:
            _logger.debug("Before creating NOT gate, input node details are:")
            inNode.printInfo()  # Temporary diagnostic for debugging.
        #__/ End if doDebug.

            #------------------------------
            # Rename the input node to "X".

        inNode.renameTo('X')    # Call the inverter's input node 'X'.

        if doDebug:
            _logger.debug("Renamed input node from q to X; now its details are:")
            inNode.printInfo()
        #__/ End if doDebug.

            #----------------------------------------------------
            # Create the NOT gate, without output node named "Y".
            # Remember the gate and its output node.

        inst._notGate = notGate = DynamicNOTGate(inNode, 'notgate',
                                                 network=inst, outNodeName='Y')
        
        inst._outNode = outNode = notGate.outputNode

            # Set the initial position of the output node
            # appropriately (assuming an input of 0).
        
        outNode.coord.position.value = Fixed(1)

            #---------------------------
            # Maybe do some diagnostics.

        if doDebug:
            
            netname = netName(inst)     # Should get network name set above.

            _logger.debug("Finished creating %s.  Now input node details are:" % netname)        
            inNode.printInfo()  # Temporary diagnostic for debugging.

            _logger.debug("Meanwhile, output node details are:")    
            outNode.printInfo()  # Temporary diagnostic for debugging.

        #__/ End if doNorm.

    #__/ End method InverterNet.__init__().


        #|----------------------------------------------------------------------
        #| inst.printDiagnostics()                      [public instance method]
        #|
        #|      Displays some network diagnostics to standard output
        #|      as a CSV format row.  Column order is
        #|
        #|          Xqt,Xq,Xpt,Xp,Yqt,Yq,Ypt,Yp
        #|
        #|      where
        #|
        #|          X = input node, Y = output node;
        #|          q = position, p = momentum;
        #|          t = timestep number.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def printDiagnostics(me):
        
        """Output network diagnostics as a CSV row. Timestep and
           value of position and momentum coordinates of X and Y
           (input and output) nodes."""

        inCoords  = me._inNode.coord    # Generalized coordinates of input.
        outCoords = me._outNode.coord   # Generalized coordinates of output.
        
        if doNorm:
            _logger.normal("%d, %.9f, %d, %.9f, %d, %.9f, %d, %.9f" %
                           (inCoords.position.time,  inCoords.position(),
                            inCoords.momentum.time,  inCoords.momentum(),
                            outCoords.position.time, outCoords.position(),
                            outCoords.momentum.time, outCoords.momentum()))
            
        #__/ End if doNorm.
        
    #__/ End method printDiagnostics().

#__/ End class InverterNet.


            #|------------------------------------------------------------------
            #|
            #|  AndGateNet(DynamicNetwork)                        [public class]
            #|                                                  
            #|      This specialized subclass of DynamicNetwork
            #|      creates a simple dynamic network which contains
            #|      two dynamic memory cells feeding the inputs of
            #|      a two-input AND gate.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class AndGateNet(DynamicNetwork):

    """
        This specialized subclass of DynamicNetwork creates a simple
        dynamic network which contains two dynamic memory cells
        feeding the inputs of a two-input AND gate.

            Network diagram:
            ----------------       
                 __________         
                |          |   A   
                | memcellA |-->@--+    _________
                |__________|      +-->|         |   Q
                 __________           | andgate |-->@-->
                |          |   B  +-->|_________|       
                | memcellB |-->@--+
                |__________|       
                                                                      """

    #|--------------------------------------------------------------------------
    #|[In class AndGateNet]
    #|
    #|  Private instance attributes:
    #|  ----------------------------
    #|
    #|      Maybe later we will make some of these public.
    #|
    #|          inst.{_memCellA,_memCellB}:DynamicMemCell  [priv. inst. attrib.]
    #|
    #|              The memory cells that feed the AND gate inputs.
    #|
    #|          inst.{_nodeA,_nodeB,_nodeQ}:DynamicNode    [priv. inst. attrib.]
    #|
    #|              The two input nodes and the output node.
    #|
    #|          inst._andGate:DynamicANDGate               [priv. inst. attrib.]
    #|
    #|              The AND gate.
    #|
    #|--------------------------------------------------------------------------
    
    def __init__(me, context:SimulationContext=None):

        """This initializer takes one optional argument, a simulation
           context, and it creates a new dynamic AND gate "network"
           (consisting of 2 memory cells feeding an AND gate) in that
           context."""

            #--------------------------------------------------------
            # First, do generic initialization for dynamic networks.
            
        DynamicNetwork.__init__(me, name='exampleNet_andGate',
                                title="Example network: AND gate",
                                context=context)

            #-----------------------------------------------------------
            # Create the two dynamic memory cells feeding the AND gate.

        me._memCellA = memCellA = DynamicMemCell('memcellA', network=me,
                                                 biasval=0, outNodeName='A')
        me._nodeA = nodeA = memCellA.outputNode
        
        me._memCellB = memCellB = DynamicMemCell('memcellB', network=me,
                                                 biasval=1, outNodeName='B')
        me._nodeB = nodeB = memCellB.outputNode

            #-----------------------------
            # Create the AND gate itself.

        me._andGate = andGate = DynamicANDGate(nodeA, nodeB, 'andgate',
                                               network=me, outNodeName='Q')
        me._nodeQ = nodeQ = andGate.nodeC

    #__/ End AndGateNet.__init__().

        #|----------------------------------------------------------------------
        #| inst.printDiagnostics()                      [public instance method]
        #|
        #|      Displays some network diagnostics to standard output
        #|      as a CSV format row.  Column order is
        #|
        #|          Aqt,Aq,Apt,Ap,Bqt,Bq,Bpt,Bp,Qqt,Qq,Qpt,Qp
        #|
        #|      where
        #|
        #|          A,B = input nodes, Q = output node;
        #|          q = position, p = momentum;
        #|          t = timestep number.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def printDiagnostics(me):
        
        """Output network diagnostics as a CSV row. Timestep and value
           of position and momentum coordinates of the three nodes A,
           B (inputs) and Q (output)."""

        Acoords = me._nodeA.coord
        Bcoords = me._nodeB.coord
        Qcoords = me._nodeQ.coord

        if doNorm:
            _logger.normal("%d, %.9f, %d, %.9f, "
                           "%d, %.9f, %d, %.9f, "
                           "%d, %.9f, %d, %.9f" %
                           
                           (Acoords.position.time, Acoords.position(),
                            Acoords.momentum.time, Acoords.momentum(),
                            
                            Bcoords.position.time, Bcoords.position(),
                            Bcoords.momentum.time, Bcoords.momentum(),
                            
                            Qcoords.position.time, Qcoords.position(),
                            Qcoords.momentum.time, Qcoords.momentum()))
            #______________/ End _logger.normal() call.
            
        #__/ End if doNorm.
            
    #__/ End AndGateNet.printDiagnostics()


        #|----------------------------------------------------------------------
        #|  inst.initStats()                            [public instance method]
        #|
        #|      Initialize statistics accumulators for this instance
        #|      of class AndGateNet.  Initializes position integration
        #|      accumulators for the three nodes A,B,Q.  These will be
        #|      used later to compute their average position values. A
        #|      sample counter is also initialized.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def initStats(me):

        """ Initializes statistics accumulators for this instance of
            class AndGateNet.  Initializes position integration accum-
            ulators for the three nodes A,B,Q.  These will be used
            later to compute their average position values. A sample
            counter is also initialized.
                                                                      """
        
        me.nSamples = 0
        me.totalA = Fixed(0)    # These are fixed-point to ensure exactness.
        me.totalB = Fixed(0)
        me.totalQ = Fixed(0)
        
    #__/ End AndGateNet.initStats().

    
        #|----------------------------------------------------------------------
        #|  inst.gatherStats()                          [public instance method]
        #|
        #|      Gathers one sample's worth of data for statistics
        #|      collection purposes.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def gatherStats(me):
        
        """ Gathers one sample's worth of data for statistics
            calculation purposes.  Updates accumulators.              """
        
        me.nSamples += 1
        me.totalA += me._nodeA.coord.position()
        me.totalB += me._nodeB.coord.position()
        me.totalQ += me._nodeQ.coord.position()

    #__/ End AndGateNet.gatherStats().
        

        #|----------------------------------------------------------------------
        #|  inst.printCsvHeader()                       [public instance method]
        #|
        #|      Prints to standard output one CSV row, which is the
        #|      header row for the data rows that are generated by
        #|      the printDiagnostics() method.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def printCsvHeader(me):

        """ Prints to standard output one CSV row, which is the
            header row for the data rows that are generated by
            the printDiagnostics() method.                            """
        
        if doNorm:
            _logger.normal("A.qt, A.q, A.pt, A.p, "
                           "B.qt, B.q, B.pt, B.p, "
                           "Q.qt, Q.q, Q.pt, Q.p")

    #__/ End AndGateNet.printCsvHeader().
            

        #|----------------------------------------------------------------------
        #|  inst.printStats()                           [public instance method]
        #|
        #|      Calculate and print to standard output the statistics
        #|      (average position) of the three nodes in the network.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def printStats(me):

        """Calculate and print to standard output the statistics
           (average position) of the three nodes in the network.       """
        
        if doNorm:
            _logger.normal("Average positions:  A = %f, B = %f, Q = %f" %
                           ((me.totalA / me.nSamples),
                            (me.totalB / me.nSamples),
                            (me.totalQ / me.nSamples)))

    #__/ End AndGateNet.printStats().

#__/ End class AndGateNet.


            #|------------------------------------------------------------------
            #|
            #|  HalfAdderNet(DynamicNetwork)                      [public class]
            #|                                                  
            #|      This specialized subclass of DynamicNetwork
            #|      instantiates as a simple dynamic network which
            #|      contains two dynamic memory cells feeding the
            #|      inputs of a half-adder network (consisting of
            #|      an AND gate and an XOR gate).
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class HalfAdderNet(DynamicNetwork):

    """
        This specialized subclass of DynamicNetwork creates a 
        dynamic network which contains two dynamic memory cells
        feeding the inputs of a half adder network, comprised of
        a two-input XOR gate and a two-input AND gate.

            Network diagram:
            ----------------       
                 __________             _____
                |          |      +--->|     |   S1
                | memcellA |----->A    | and |-->@-->
                |__________|   +---)-->|_____|        
                 __________    |  |     _____
                |          |   |  +--->|     |   S0
                | memcellB |-->B       | xor |-->@-->
                |__________|   +------>|_____|        
                                                                      """

    #|--------------------------------------------------------------------------
    #|[In class HalfAdderNet]
    #|
    #|  Private instance attributes:               [class documentation section]
    #|  ----------------------------
    #|
    #|      Maybe later we will make some of these public.
    #|
    #|          inst.{_memCellA,_memCellB}:DynamicMemCell  [priv. inst. attrib.]
    #|
    #|              The memory cells that feed the half adder inputs.
    #|
    #|          inst.{_nodeA,_nodeB}:DynamicNode           [priv. inst. attrib.]
    #|
    #|              The nodes representing the two bits to be added.
    #|
    #|          inst._AND:DynamicANDGate                   [priv. inst. attrib.]
    #|
    #|              The AND gate.
    #|
    #|          inst._XOR:DynamicANDGate                   [priv. inst. attrib.]
    #|
    #|              The XOR gate.
    #|
    #|          inst.{_nodeS1,_nodeS0}:DynamicNode         [priv. inst. attrib.]
    #|
    #|              The output nodes representing the most-significant
    #|              and least significant bits of the sum, respectively.
    #|
    #|--------------------------------------------------------------------------

        #|----------------------------------------------------------------------
        #|[In class HalfAdderNet.]
        #|
        #|  inst.__init__()                            [special instance method]
        #|
        #|      This initializer takes one optional argument, a
        #|      simulation context, and it creates a new half-adder
        #|      network (consisting of 2 memory cells feeding an AND
        #|      gate and an XOR gate) in that context.
        #|
        #|      Note that this works by explicitly constructing the
        #|      individual gates making up the half-adder.  Later we
        #|      want to abstract it by creating a half-adder module
        |#      that will do that for us, and instantiating it.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
    def __init__(me, context:SimulationContext=None):

        """This initializer takes one optional argument, a simulation
           context, and it creates a new half-adder network (consist-
           ing of 2 memory cells feeding an AND gate and an XOR gate)
           in that context."""

            # First, do generic initialization for dynamic networks.
            
        DynamicNetwork.__init__(me, name='exampleNet_halfAdder',
                                title="Example network: half adder",
                                context=context)

            #--------------------------------------------------------
            # Construct the half-adder network.  Note that in the
            #   below, the input bits are A, B.  The output bits are
            #   S0 (ones place) and S1 (twos place).

                # Create & remember the memory cells and their output nodes.

        me._memCellA = memCellA = DynamicMemCell('memcellA', network=me,
                                                 biasval=1.0, outNodeName='A')
        me._nodeA = nodeA = memCellA.outputNode
        
        me._memCellB = memCellB = DynamicMemCell('memcellB', network=me,
                                                 biasval=1.0, outNodeName='B')
        me._nodeB = nodeB = memCellB.outputNode

                # Create & remember the XOR gate and the AND gate & outputs.

        me._XOR = XOR = DynamicXORGate(nodeA, nodeB, 'xor', network=me,
                                       outNodeName='S0')
        
        me._nodeS0 = nodeS0 = XOR.nodeC     # Node C is the output node.

        me._AND = AND = DynamicANDGate(nodeA, nodeB, 'and', network=me,
                                       outNodeName='S1')
        
        me._nodeS1 = nodeS1 = AND.nodeC

    #__/ End HalfAdderNet.__init__().
        

    def printDiagnostics(me):
        if doNorm:
            
            nodes = me.nodes
            
            nodeA_c = nodes['A'].coord
            nodeB_c = nodes['B'].coord
            nodeS0_c = nodes['S0'].coord
            nodeS1_c = nodes['S1'].coord
            
            _logger.normal(("%d, %.9f, "*7 + "%d, %.9f") %
                           (nodeA_c.position.time, nodeA_c.position(),
                            nodeA_c.momentum.time, nodeA_c.momentum(),
                            nodeB_c.position.time, nodeB_c.position(),
                            nodeB_c.momentum.time, nodeB_c.momentum(),
                            nodeS1_c.position.time, nodeS1_c.position(),
                            nodeS1_c.momentum.time, nodeS1_c.momentum(),
                            nodeS0_c.position.time, nodeS0_c.position(),
                            nodeS0_c.momentum.time, nodeS0_c.momentum()
                            ))

    def initStats(me):
        me.nSamples = 0
        me.totalA = Fixed(0)
        me.totalB = Fixed(0)
        me.totalS0 = Fixed(0)
        me.totalS1 = Fixed(0)

    def gatherStats(me):
        me.nSamples += 1
        me.totalA += me.nodes['A'].coord.position()
        me.totalB += me.nodes['B'].coord.position()
        me.totalS0 += me.nodes['S0'].coord.position()
        me.totalS1 += me.nodes['S1'].coord.position()

    def printCsvHeader(me):
        if doNorm:
            #_logger.normal("in.qt, in.q, in.pt, in.p, out.qt, out.q, out.pt, out.p")
            _logger.normal("A.qt, A.q, A.pt, A.p, B.qt, B.q, B.pt, B.p, "
                           "S1.qt, S1.q, S1.pt, S1.p, S0.qt, S0.q, S0.pt, S0.p")


    def printStats(me):
        if doNorm:
            _logger.normal("Average positions:  A = %f, B = %f, S1 = %f, S0 = %f" %
                           ((me.totalA / me.nSamples),
                            (me.totalB / me.nSamples),
                            (me.totalS1 / me.nSamples),
                            (me.totalS0 / me.nSamples)
                            ))



class FullAdderNet(DynamicNetwork):

    def __init__(me, context:SimulationContext=None):

        DynamicNetwork.__init__(me, name='exampleNet_fullAdder',
                                title="Example network: full adder",
                                context=context)

        netname = netName(me)   # Should retrieve name set above.

            #|========================================================
            #|  In the below, input bits are A, B, C.  Output bits are
            #|  S0 and S1.  Intermediate nodes are X, A1, A2.
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            # First we pick logical values for the input bits.

        logicA = False;  logicB = True;  logicC = True

            # Calculate what the logic values of the computed bits should be.

        logicA1 = logicA and logicB
        logicX  = (logicA or logicB) and not logicA1
        logicA2 = logicX and logicC
        logicS0 = (logicX or logicC) and not logicA2
        logicS1 = logicA1 or logicA2

            # Convert logic values to real-valued generalized-position
            # coordinates.  (Note this is just to avoid injecting excess
            # energy on initialization.)

        Aval = float(logicA);  Bval = float(logicB);  Cval = float(logicC)

        A1val = float(logicA1);  Xval  = float(logicX);  A2val = float(logicA2)
        S0val = float(logicS0);  S1val = float(logicS1)

            # Now we create the network.  First, the input cells.

        me._memCellA = memCellA = DynamicMemCell('memcellA', network=me,
                                                 biasval=Aval, outNodeName='A')
        me._nodeA = nodeA = memCellA.outputNode
        
        me._memCellB = memCellB = DynamicMemCell('memcellB', network=me,
                                                 biasval=Bval, outNodeName='B')
        me._nodeB = nodeB = memCellB.outputNode

        me._memCellC = memCellC = DynamicMemCell('memcellC', network=me,
                                                 biasval=Cval, outNodeName='C')
        me._nodeC = nodeC = memCellC.outputNode

            # Circuit for the first half-adder.  Really, we should abstract
            # this out to a half-adder sub-network...

        me._XOR1 = XOR1 = DynamicXORGate(nodeA, nodeB, 'xor1', network=me, outNodeName='X', initOutPos=Xval)
        me._nodeX = nodeX = XOR1.nodeC

        me._AND1 = AND1 = DynamicANDGate(nodeA, nodeB, 'and1', network=me, outNodeName='A1', initOutPos=A1val)
        me._nodeA1 = nodeA1 = AND1.nodeC

            # Circuit for the second half-adder.

        me._XOR2 = XOR2 = DynamicXORGate(nodeX, nodeC, 'xor2', network=me, outNodeName='S0', initOutPos=S0val)
        me._nodeS0 = nodeS0 = XOR2.nodeC

        me._AND2 = AND2 = DynamicANDGate(nodeX, nodeC, 'and2', network=me, outNodeName='A2', initOutPos=A2val)
        me._nodeA2 = nodeA2 = AND2.nodeC

            # Circuit to compute carry-out bit (S1).

        me._OR = OR = DynamicORGate(nodeA1, nodeA2, 'or', network=me, outNodeName='S1', initOutPos=S1val)
        me._nodeS1 = nodeS1 = OR.nodeC

    def printDiagnostics(me):
        if doNorm:
            
            nodes = me.nodes
            
            nodeA_c = nodes['A'].coord
            nodeB_c = nodes['B'].coord
            nodeC_c = nodes['C'].coord
            nodeS0_c = nodes['S0'].coord
            nodeS1_c = nodes['S1'].coord
            
            _logger.normal(("%d, %.9f, "*9 + "%d, %.9f") %
                           (nodeA_c.position.time, nodeA_c.position(),
                            nodeA_c.momentum.time, nodeA_c.momentum(),
                            nodeB_c.position.time, nodeB_c.position(),
                            nodeB_c.momentum.time, nodeB_c.momentum(),
                            nodeC_c.position.time, nodeC_c.position(),
                            nodeC_c.momentum.time, nodeC_c.momentum(),
                            nodeS1_c.position.time, nodeS1_c.position(),
                            nodeS1_c.momentum.time, nodeS1_c.momentum(),
                            nodeS0_c.position.time, nodeS0_c.position(),
                            nodeS0_c.momentum.time, nodeS0_c.momentum()
                            ))

    def initStats(me):
        me.nSamples = 0
        me.totalA = Fixed(0)
        me.totalB = Fixed(0)
        me.totalC = Fixed(0)
        me.totalS0 = Fixed(0)
        me.totalS1 = Fixed(0)

    def gatherStats(me):
        me.nSamples += 1
        me.totalA += me.nodes['A'].coord.position()
        me.totalB += me.nodes['B'].coord.position()
        me.totalC += me.nodes['C'].coord.position()
        me.totalS0 += me.nodes['S0'].coord.position()
        me.totalS1 += me.nodes['S1'].coord.position()

    def printCsvHeader(me):
        if doNorm:
            #_logger.normal("in.qt, in.q, in.pt, in.p, out.qt, out.q, out.pt, out.p")
            _logger.normal("A.qt, A.q, A.pt, A.p, B.qt, B.q, B.pt, B.p, C.qt, C.q, C.pt, C.p, "
                           "S1.qt, S1.q, S1.pt, S1.p, S0.qt, S0.q, S0.pt, S0.p")


    def printStats(me):
        if doNorm:
            _logger.normal("Average positions:  A = %f, B = %f, C = %f, S1 = %f, S0 = %f" %
                           ((me.totalA / me.nSamples),
                            (me.totalB / me.nSamples),
                            (me.totalC / me.nSamples),
                            (me.totalS1 / me.nSamples),
                            (me.totalS0 / me.nSamples)
                            ))


#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#|                  BOTTOM OF FILE:    exampleNetworks.py
#|==============================================================================
