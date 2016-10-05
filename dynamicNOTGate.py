
from numbers import Real

from binaryDifferentiableFunction   import *    # Class BinaryDifferentiableFunction.
from dynamicNode                    import *    # We reference class DynamicNode.
from dynamicTwoTerminalGate         import *
from dynamicNetwork                 import *    # We reference class DynamicNetwork.

class DynamicNOTFunction(BinaryDifferentiableFunction):

    def __init__(inst, stiffness:Real):

            # Set up some names

        name = 'N'      # For "NOT function"
        argName1 = 'x'  # Input coordinate
        argName2 = 'y'  # Output coordinate

            # Set up our function.

        inst.stiffness = stiffness
        function = lambda x,y:  0.5 * inst.stiffness * (x + y - 1)**2

            # Set up our partial derivatives with respect to x and y.

        partial = lambda x,y:  inst.stiffness * (x + y - 1)   # partial wrt x or y

        deriv1 = partial    # The two partials are the same
        deriv2 = partial

            # Do generic initialization for binary differentiable functions.

        BinaryDifferentiableFunction.__init__(inst, name=name, argName1=argName1,
                                              argName2=argName2, function=function,
                                              deriv1=deriv1, deriv2=deriv2)

    #__/ End method DynamicNOTFunction.__init__().

#__/ End class DynamicNOTFunction.


class DynamicNOTGate(DynamicTwoTerminalGate):

    #-- This creator DynamicNotGate(inputNode) creates a dynamic
    #   NOT gate with the given input node; the output node is
    #   created.

    def __init__(inst, inputNode:DynamicNode, name:str=None, 
                 network:DynamicNetwork=None, stiffness:Real = 1.0,
                 outNodeName:str=None):

        netname = netName(network)

        logger.debug("Initializing a new DynamicNOTGate named '%s' in network '%s'" %
                     (str(name), netname))

            # Do generic initialization for dynamic two-terminal gates.
            # (Create ports & output node, link it to our output port.)

        DynamicTwoTerminalGate.__init__(inst, inputNode, name=name,
                                        network=network, outNodeName=outNodeName)

            # Create the potential energy function relating the input
            # and output nodes.

        notFunc = DynamicNOTFunction(stiffness)

            # Set the interaction function of this DynamicTwoTerminalGate
            # to that function.

        inst.interaction = notFunc
        
    #__/

#__/
        
