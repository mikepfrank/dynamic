
#-- This example network includes a full adder whose
#   input nodes are output by memory cells.

class ExampleNetwork_FullAdder(Network):

    def __init__(inst):

        #-- Create 3 dynamic memory cells to hold the network's input.
        Ma = DynamicMemCell(0)
        Mb = DynamicMemCell(0)
        Mc = DynamicMemCell(0)

        #-- Get our 3 input nodes (which are output nodes of those cells).
        a = Ma.outputNode
        b = Mb.outputNode
        c = Mc.outputNode

        #-- Create a full-adder operating on those nodes.        
        FA = FullAdder(a,b,c)
        
        
