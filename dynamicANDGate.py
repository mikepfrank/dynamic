
class DynamicANDFunction(BaseDifferentiableFunction):

    def __init__(inst, stiffness):

        BaseDifferentiableFunction.__init__(inst)

        inst.setArglist(('x', 'y', 'z'))      # z is output

        inst.stiffness = stiffness

        inst.function = lambda (x, y, z):
            0.5 * inst.stiffness * (z - x*y)**2

        inst.partials = [
            lambda (x,y,z): -y*inst.stiffness * (z - x*y),  # partial wrt x
            lambda (x,y,z): -x*inst.stiffness * (z - x*y),  # partial wrt y
            lambda (x,y,z): inst.stiffness * (z - x*y)      # partial wrt z
        ]

class DynamicANDGate(DynamicThreeTerminalGate):

    def __init__(inst, inputNodeA, inputNodeB, stiffness = 1.0):

        DynamicThreeTerminalGate.__init__(inst, inputNodeA, inputNodeB)

        andFunc = DynamicANDFunction(stiffness)

        inst.interaction = andFunc

