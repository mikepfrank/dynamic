
from numbers import Real

from functions.ternaryDifferentiableFunction  import *    # Class TernaryDifferentiableFunction
from network.dynamicNode                    import *    # Class DynamicNode
from network.dynamicThreeTerminalGate       import *    # Class DynamicThreeTerminalGate
from network.dynamicNetwork                 import *    # Class DynamicNetwork

class DynamicORFunction(TernaryDifferentiableFunction):

    def __init__(me, stiffness:Real):

            # Set up some names

        name = 'Io'      # For "Inclusive OR function"
        argName1 = 'x'  # First input coordinate.
        argName2 = 'y'  # Second input coordinate.
        argName3 = 'z'  # Output coordinate.

            # Set up our function.  At minimum energy, z=x+y-xy.

        me.stiffness = stiffness
        function = lambda x, y, z:  0.5 * me.stiffness * (z - x - y + x*y)**2

            # Set up our partial derivatives w.r.t. x, y, and z.

        partial_x = lambda x,y,z: me.stiffness * (y - 1) * (z - x - y + x*y)  # partial wrt x
        partial_y = lambda x,y,z: me.stiffness * (x - 1) * (z - x - y + x*y)  # partial wrt y
        partial_z = lambda x,y,z: me.stiffness *           (z - x - y + x*y)  # partial wrt z

        TernaryDifferentiableFunction.__init__(me, name=name,
                                               argName1=argName1,
                                               argName2=argName2,
                                               argName3=argName3,
                                               function=function,
                                               deriv1=partial_x,
                                               deriv2=partial_y,
                                               deriv3=partial_z)


class DynamicORGate(DynamicThreeTerminalGate):

    def __init__(me, inputNodeA:DynamicNode, inputNodeB:DynamicNode, name:str=None,
                 network:DynamicNetwork=None, stiffness:Real = 1.0, outNodeName:str=None,
                 initOutPos:Real=None):

        netname = netName(network)

        DynamicThreeTerminalGate.__init__(me, inputNodeA, inputNodeB, name=name,
                                          network=network, outNodeName=outNodeName,
                                          initOutPos=initOutPos)

        andFunc = DynamicORFunction(stiffness)

        me.interaction = andFunc
