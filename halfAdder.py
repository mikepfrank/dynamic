class HalfAdder(DynamicNetwork):

    #-- This creator HalfAdder(a,b) takes two nodes a,b that
    #   are inputs to the half-adder.

    def __init__(inst, a, b):

        #-- Add the two input nodes to the set of nodes associated
        #   with the current full-adder network.
            
        inst.addNodes(a, b)

        #-- First, create an XOR gate operating on the two input nodes.
        #   The output node of the XOR is the low-order bit of the
        #   2-bit sum of the two input bits.

        XOR = DynamicXORGate(a,b)
        inst.s0 = XOR.out

        #-- Next, create an AND gate operating on the two input nodes.
        #   The output node of the AND is the high-order bit of the
        #   2-bit sum of the two input bits.

        AND = DynamicANDGate(a,b)
        inst.s1 = AND.out

        #-- Add the output nodes of the XOR and AND gates to the set of
        #   nodes associated with the current half-adder network.

        inst.addNodes(inst.s0, inst.s1)
        
        
        
