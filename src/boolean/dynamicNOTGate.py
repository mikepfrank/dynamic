#|==============================================================================
#|                      TOP OF FILE:    dynamicNOTGate.py
#|------------------------------------------------------------------------------
#|   The below module documentation string will be displayed by pydoc3.
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""
    FILE NAME:      dynamicNOTGate.py                [Python module source code]

    FILE PATH:      $GIT_ROOT/dynamic/src/boolean/dynamicNOTGate.py

    MODULE NAME:    boolean.dynamicNOTGate

    IN COMPONENT:   Dynamic.boolean     (Boolean gate implementations)


    MODULE DESCRIPTION:
    -------------------

        The dynamicNOTGate module provides a simple implementation of
        a Boolean NOT gate (logical inverter) as a Dynamic gate.  The
        potential energy function used here is

                             1               2
                            --- k (x + y - 1),
                             2

        where k is a "stiffness" constant, x is the (generalized
        position) coordinate of the input node, and y is the
        the coordinate of the output node.


    BASIC MODULE USAGE:
    -------------------

        from boolean.dynamicNOTGate import DynamicNOTGate

        ...     // Create node nodeX and network myNet

        myNotGate = DynamicNOTGate(nodeX, 'myNOT', network=myNet,
                                   outNodeName='Y')


    PUBLIC CLASSES:
    ---------------

        See the class's docstring for details.

            DynamicNOTFunction                             [module public class]

                The class of potential energy functions used to
                implement the NOT gate.

            DynamicNOTGate                                 [module public class]    

                The class of NOT gates defined in this module.
                
                                                                             """
#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#| End of module documentation string.
#|------------------------------------------------------------------------------

    #|==========================================================================
    #|   1. Module imports.                                [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #------------------------------------------
        # Imports from our parent module (package).

from . import _logger       # Our component logger.


        #--------------------------------------
        # Imports from standard Python modules.

from numbers import Real    # Used only for type declarations.


        #-----------------------------------------------------------
        # Imports from custom modules in lower-level packages within
        # the Dynamic system.

from logmaster import doDebug   # Whether to show debug output.

from functions.binaryDifferentiableFunction import BinaryDifferentiableFunction
    # A class for two-argument differentiable functions, which we subclass.

from network.dynamicNode                    import  DynamicNode
from network.dynamicTwoTerminalGate         import  DynamicTwoTerminalGate
from network.dynamicNetwork                 import  DynamicNetwork


    #|==========================================================================
    #|  2.  Global constants, variables, and objects.      [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|  2.1.  Special globals.                      [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global __all__              # List of public symbols exported by this module.

__all__ = [
    'DynamicNOTFunction',   # Class of interaction functions for NOT gates.
    'DynamicNOTGate'        # Class of Dynamic implementations of NOT gates.
    ]


    #|==========================================================================
    #|  3.  Class definitions.                             [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|   3.1.  Public classes.                      [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
            #|------------------------------------------------------------------
            #|
            #|      DynamicANDFunction                     [module public class]
            #|
            #|          This class, a subclass of the class of binary
            #|          differentiable functions, represents
            #|          interaction functions of the form used to
            #|          represent Boolean NOT gates in our current
            #|          implementation, which is:
            #|
            #|                       1               2
            #|                      --- k (x + y - 1),
            #|                       2
            #|
            #|          where k is any real-valued constant (normally
            #|          positive) representing the overall energy scale
            #|          or "stiffness" of the interaction.  When the
            #|          input coordinates x,y are at consistent logic
            #|          values, the interaction energy is 0, and when
            #|          they are at inconsistent logic values, the
            #|          interaction energy is k/2.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class DynamicNOTFunction(BinaryDifferentiableFunction):

    """This class, a subclass of the class of binary differentiable
       functions, represents interaction functions of the form that we
       currently use to implement Boolean NOT gates, which is:

                           1               2
                          --- k (x + y - 1),
                           2

       where k is any real-valued constant (normally positive)
       representing the overall energy scale or "stiffness" of the
       interaction.  When the input coordinates x,y are at
       consistent logic values (with y being the output), the
       interaction energy is 0, and when they are at inconsistent
       logic values, the interaction energy is k/2.                   """

        #|----------------------------------------------------------------------
        #|
        #|  inst.__init__()                            [special instance method]
        #|
        #|      This instance initializer (constructor) for the
        #|      DynamicNOTFunction class takes one optional
        #|      argument, a real number representing the
        #|      stiffness parameter of the instance of the NOT
        #|      interaction function that is to be created.  If no
        #|      argument is provided or the value None is provided,
        #|      the stiffness value defaults to 1.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def __init__(inst, stiffness:Real=None):

        """This instance initializer (constructor) for the
           DynamicANDFunction class takes one optional argument, a
           real number representing the stiffness parameter of the
           instance of the AND interaction function that is to be
           created.  If no argument is provided or the value None is
           provided, the stiffness value defaults to 1.               """

        if stiffness is None:   stiffness = 1       # Fill in default value.

            # Set up some names, for the function and its formal arguments.

        name = 'N'      # For "NOT function."
        argName1 = 'x'  # Input coordinate.
        argName2 = 'y'  # Output coordinate.

            # Set up our function.  At minimum energy, y=1-x.

        inst.stiffness = stiffness    # Remember my stiffness value
        
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


            #|------------------------------------------------------------------
            #|
            #|      DynamicNOTGate                         [module public class]
            #|
            #|          This class, a subclass of the class of three-
            #|          terminal Dynamic gates, represents NOT gates
            #|          implemented using the interaction function
            #|
            #|                       1               2
            #|                      --- k (x + y - 1),
            #|                       2
            #|
            #|          where k is any real-valued constant (normally
            #|          positive) representing the overall energy scale
            #|          or "stiffness" of the interaction.  When the
            #|          input coordinates x,y are at consistent logic
            #|          values, the interaction energy is 0, and when
            #|          they are at inconsistent logic values, the
            #|          interaction energy is k/2.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class DynamicNOTGate(DynamicTwoTerminalGate):
    
    """This class, a subclass of the class of two-terminal Dynamic
       gates, represents NOT gates implemented using the interaction
       function
       
                             1               2
                            --- k (x + y - 1),
                             2
       
       where k is any real-valued constant (normally positive)
       representing the overall energy scale or "stiffness" of the
       interaction.  When the input coordinates x,y (with y being
       the "output") are at consistent logic values, the interaction
       energy is 0, and when they are at inconsistent logic values,
       the interaction energy is k/2.
                                                                      """
        #|----------------------------------------------------------------------
        #|
        #|  inst.__init__()                            [special instance method]
        #|
        #|      This instance initializer (constructor) for the
        #|      DynamicNOTGate class takes the following arguments:
        #|
        #|          Required arguments:
        #|          -------------------
        #|
        #|              inputNode : DynamicNode
        #|
        #|                  The NOT gate's input node, which must have
        #|                  been previously created.
        #|
        #|
        #|          Optional keyword arguments:
        #|          ---------------------------
        #|
        #|              name : str = None
        #|
        #|                  The name of this gate, if any.  (If not
        #|                  provided or None, no name is assigned.)
        #|
        #|              network : DynamicNetwork = None
        #|
        #|                  The Dynamic network that this gate will be
        #|                  a part of.  If not provided or None, the
        #|                  gate will not be added to a network.
        #|
        #|              stiffness : Real = 1
        #|
        #|                  The stiffness value for this gate's
        #|                  interaction function.  If not provided or
        #|                  None, defaults to the value 1.
        #|
        #|              outNodeName : str = None
        #|
        #|                  The name that should be given to this
        #|                  gate's output node, which will be newly
        #|                  created.  If not provided or None, defaults
        #|                  to 'nodeC'.  The name will be uniqified.
        #|
        #|              initOutPos : Real = None
        #|
        #|                  The initial value that the output node's
        #|                  generalized-position coordinate should be
        #|                  set to.  If not provided or None, defaults
        #|                  to 0.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv


    #-- This creator DynamicNotGate(inputNode) creates a dynamic
    #   NOT gate with the given input node; the output node is
    #   created.

    def __init__(inst, inputNode:DynamicNode, name:str=None, 
                 network:DynamicNetwork=None, stiffness:Real = 1,
                 outNodeName:str=None, initOutPos:Real=None):

        """This instance initializer (constructor) for the
           DynamicNOTGate class takes the following arguments:
        
                Required arguments:
                -------------------
        
                    inputNode : DynamicNode
        
                        The NOT gate's input nodes, which must have
                        been previously created.
        
        
                Optional keyword arguments:
                ---------------------------
        
                    name : str = None
        
                        The name of this gate, if any.  (If not
                        provided or None, no name is assigned.)
        
                    network : DynamicNetwork = None
        
                        The Dynamic network that this gate will be
                        a part of.  If not provided or None, the
                        gate will not be added to a network.
        
                    stiffness : Real = 1
        
                        The stiffness value for this gate's
                        interaction function.  If not provided or
                        None, defaults to the value 1.
        
                    outNodeName : str = None
        
                        The name that should be given to this
                        gate's output node, which will be newly
                        created.  If not provided or None, defaults
                        to 'nodeC'.  The name will be uniqified
                        when the node is added to the network.
        
                    initOutPos : Real = None
        
                        The initial value that the output node's
                        generalized-position coordinate should be
                        set to.  If not provided or None, defaults
                        to 0.
                                                                      """

            #----------------------------------------
            # Maybe do some debug-level diagnostics.
        
        if doDebug:
            
                # Retrieve string name of network.  Does some error-handling.
            netname = netName(network)

            _logger.debug("Initializing a new DynamicNOTGate named "
                          "'%s' in network '%s'" % (str(name), netname))

        #__/ End if doDebug


            #-----------------------------------------------------------
            # Do generic initialization for dynamic 3-terminal gates.
            # (Create ports & output node, link it to our output port.)

        DynamicTwoTerminalGate.__init__(inst, inputNode, name=name,
                                        network=network,
                                        outNodeName=outNodeName,
                                        initOutPos=initOutPos)

            #---------------------------------------------------------
            # Create the potential energy function relating the input
            # and output nodes.

        notFunc = DynamicNOTFunction(stiffness)

            #-------------------------------------------------------------
            # Set the interaction function of this DynamicTwoTerminalGate
            # to that function.

        inst.interaction = notFunc
        
    #__/ End DynamicNOTGate.__init__().

#__/ End class DynamicNOTGate.


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                   BOTTOM OF FILE:    dynamicNOTGate.py
#===============================================================================
