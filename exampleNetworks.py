
#-- This example network includes just a single dynamic memory cell.

class ExampleNetwork_MemCell(DynamicNetwork):

    def __init__(inst):

        #-- Create the single dynamic memory cell.
        m = DynamicMemCell()

        #-- Get our single node (the output node of that cell).
        n = m.outputNode

#-- This example network includes a full adder whose
#   input nodes are output by memory cells.

class ExampleNetwork_FullAdder(DynamicNetwork):

    def __init__(inst):

        #-- Create 3 dynamic memory cells to hold the network's input.
        Ma = DynamicMemCell()
        Mb = DynamicMemCell()
        Mc = DynamicMemCell()

        #-- Get our 3 input nodes (which are output nodes of those cells).
        a = Ma.outputNode
        b = Mb.outputNode
        c = Mc.outputNode

        #-- Create a full-adder operating on those nodes.        
        FA = FullAdder(a,b,c)
        
        
