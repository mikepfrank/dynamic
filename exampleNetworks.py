from dynamicNetwork import DynamicNetwork
from dynamicMemCell import DynamicMemCell

# ExampleNetwork_MemCell class.  This example network (pretty much the
# simplest possible non-empty network) includes just a single dynamic
# memory cell.

class ExampleNetwork_MemCell(DynamicNetwork):

    def __init__(inst):

        # First do generic initialization for dynamic networks.

        DynamicNetwork.__init__(inst)

        #-- Create the single dynamic memory cell and add it to the network.
        
        m = DynamicMemCell(inst)

        ##-- Get our single node (the output node of that cell).
        #n = m.outputNode

#-- This example network includes a full adder whose
#   input nodes are output by memory cells.

class ExampleNetwork_FullAdder(DynamicNetwork):

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
        
        
