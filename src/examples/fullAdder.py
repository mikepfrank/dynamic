class FullAdder(DynamicNetwork):

    #---- This creator FullAdder(a,b,c) takes three nodes a,b,c that
    #       are three bits to be added together in the full adder.

    def __init__(inst, a, b, c):

        #-- Add the three input nodes to the set of nodes associated
        #   with the current full-adder network.
            
        inst.addNodes([a, b, c])

        #-- Create the first half-adder.  This adds the bits a,b
        #   together to produce a two-bit partial sum s1,s0.

        HA1 = HalfAdder(a, b)
        inst.s0 = HA1.s0
        inst.s1 = HA1.s1

        #-- Add the output nodes of that half-adder to our network.
        inst.addNodes([inst.s0, inst.s1])

        #-- Create the second half-adder.  This adds the low-order
        #   bit of the output of the first half-adder to the third
        #   input.

        HA2 = HalfAdder(inst.s0, c)
        inst.t0 = HA2.s0
        inst.t1 = HA2.s1

        #-- Add the output nodes the the second half-adder to our network.
        inst.addNodes([inst.t0, inst.t1])

        #-- Finally, create an OR gate to combine the carry bits
        #   of the two constituent half-adders.

        OR = DynamicORGate(inst.s1, inst.t1)

        inst.addNode(OR.outputNode)
        
        inst.sum = inst.t0
        inst.carry = OR.outputNode

        
        

