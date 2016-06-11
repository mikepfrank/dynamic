class DynamicXORFunction(BaseDifferentiableFunction):

    def __init__(inst, stiffness):

        BaseDifferentiableFunction.__init__(inst)

        inst.setArglist(('x', 'y', 'z'))    # z is output

        inst.stiffness = stiffness

        inst.function = lambda (x, y, z):
            0.5 * inst.stiffness * (x + y - z)**2

        inst.partials = [
            lambda (x,y,z): inst.stiffness*(x + y - z),  # partial wrt x
            lambda (x,y,z): inst.stiffness*(x + y - z),  # partial wrt y
            lambda (x,y,z): -inst.stiffness*(x + y - z)  # partial wrt z
        ]

class DynamicXORGate(DynamicThreeTerminalGate):

    def __init__(inst, inputNodeA, inputNodeB, stiffness = 1.0):

        DynamicThreeTerminalGate.__init__(inst, inputNodeA, inputNodeB)

        xorFunc = DynamicXORFunction(stiffness)

        inst.interaction = xorFunc
        
