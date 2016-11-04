#|==============================================================================
#|                      TOP OF FILE:    dynamicANDGate.py
#|------------------------------------------------------------------------------
#|   The below module documentation string will be displayed by pydoc3.
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""
    FILE NAME:      dynamicANDGate.py                [Python module source code]

    FILE PATH:      $GIT_ROOT/dynamic/src/boolean/dynamicANDGate.py

    MODULE NAME:    boolean.dynamicANDGate

    IN COMPONENT:   Dynamic.boolean     (Boolean gate implementations)


    MODULE DESCRIPTION:
    -------------------

        The dynamicANDGate module provides a simple implementation of
        a Boolean logical AND gate as a Dynamic gate.  The potential
        energy function used here is

                             1            2
                            --- k (z - xy),
                             2

        where k is a "stiffness" constant, z is the (generalized
        position) coordinate of the output node, and x and y are
        the coordinates of the two input nodes.

            Note that the energy is minimized when z = xy.


    BASIC MODULE USAGE:
    -------------------

        from boolean.dynamicANDGate import DynamicANDGate

        ...     // Create nodes nodeX and nodeY and network myNet

        myAndGate = DynamicANDGate(nodeX, nodeY, 'myAND', network=myNet,
                                   outNodeName='Z')


    PUBLIC CLASSES:
    ---------------

        See the class's docstring for details.

            DynamicANDFunction                             [module public class]

                The class of potential energy functions used to
                implement the AND gate.

            DynamicANDGate                                 [module public class]    

                The class of AND gates defined in this module.
                
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

from functions.ternaryDifferentiableFunction import (
    TernaryDifferentiableFunction
        # A class for three-argument differentiable functions.
        # (Our potential energy function is a subclass of this.)
    )

from network.dynamicNode                import  DynamicNode
from network.dynamicThreeTerminalGate   import  DynamicThreeTerminalGate
from network.dynamicNetwork             import  DynamicNetwork


    #|==========================================================================
    #|  2.  Global constants, variables, and objects.      [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|  2.1.  Special globals.                      [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global __all__              # List of public symbols exported by this module.

__all__ = [
    'DynamicANDFunction',   # Class of interaction functions for AND gates.
    'DynamicANDGate'        # Class of Dynamic implementations of AND gates.
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
            #|          This class, a subclass of the class of ternary
            #|          differentiable functions, represents
            #|          interaction functions of the form used to
            #|          represent Boolean AND gates in our current
            #|          implementation, which is:
            #|
            #|                       1            2
            #|                      --- k (z - xy),
            #|                       2
            #|
            #|          where k is any real-valued constant (normally
            #|          positive) representing the overall energy scale
            #|          or "stiffness" of the interaction.  When the
            #|          input coordinates x,y,z are at consistent logic
            #|          values, the interaction energy is 0, and when
            #|          they are at inconsistent logic values, the
            #|          interaction energy is k/2.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class DynamicANDFunction(TernaryDifferentiableFunction):

    """This class, a subclass of the class of ternary differentiable
       functions, represents interaction functions of the form that we
       currently use to implement Boolean AND gates, which is:

                           1            2
                          --- k (z - xy),
                           2

       where k is any real-valued constant (normally positive)
       representing the overall energy scale or "stiffness" of the
       interaction.  When the input coordinates x,y,z are at
       consistent logic values (with z being the output), the
       interaction energy is 0, and when they are at inconsistent
       logic values, the interaction energy is k/2.                   """

        #|----------------------------------------------------------------------
        #|
        #|  inst.__init__()                            [special instance method]
        #|
        #|      This instance initializer (constructor) for the
        #|      DynamicANDFunction class takes one optional
        #|      argument, a real number representing the
        #|      stiffness parameter of the instance of the AND
        #|      interaction function that is to be created.  If no
        #|      argument is provided or the value None is provided,
        #|      the stiffness value defaults to 1.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def __init__(me, stiffness:Real=None):

        """This instance initializer (constructor) for the
           DynamicANDFunction class takes one optional argument, a
           real number representing the stiffness parameter of the
           instance of the AND interaction function that is to be
           created.  If no argument is provided or the value None is
           provided, the stiffness value defaults to 1.               """

        if stiffness is None:   stiffness = 1       # Fill in default value.

            # Set up some names, for the function and its formal arguments.

        name = 'A'      # For "AND function"
        argName1 = 'x'  # First input coordinate.
        argName2 = 'y'  # Second input coordinate.
        argName3 = 'z'  # Output coordinate.

            # Set up our function.  At minimum energy, z=xy.

        me.stiffness = stiffness    # Remember my stiffness value
        
        function = lambda x, y, z:  0.5 * me.stiffness * (z - x*y)**2

            # Set up our partial derivatives w.r.t. x, y, and z.

        partial_x = lambda x,y,z: -y * me.stiffness * (z - x*y)  # partial wrt x
        partial_y = lambda x,y,z: -x * me.stiffness * (z - x*y)  # partial wrt y
        partial_z = lambda x,y,z:      me.stiffness * (z - x*y)  # partial wrt z

            # Do generic initialization for ternary differentiable functions.

        TernaryDifferentiableFunction.__init__(me, name=name,
                                               argName1=argName1,
                                               argName2=argName2,
                                               argName3=argName3,
                                               function=function,
                                               deriv1=partial_x,
                                               deriv2=partial_y,
                                               deriv3=partial_z)

    #__/ End DynamicANDFunction.__init__()

#__/ End class DynamicANDFunction.


            #|------------------------------------------------------------------
            #|
            #|      DynamicANDGate                         [module public class]
            #|
            #|          This class, a subclass of the class of three-
            #|          terminal Dynamic gates, represents AND gates
            #|          implemented using the interaction function
            #|
            #|                       1            2
            #|                      --- k (z - xy),
            #|                       2
            #|
            #|          where k is any real-valued constant (normally
            #|          positive) representing the overall energy scale
            #|          or "stiffness" of the interaction.  When the
            #|          input coordinates x,y,z are at consistent logic
            #|          values, the interaction energy is 0, and when
            #|          they are at inconsistent logic values, the
            #|          interaction energy is k/2.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class DynamicANDGate(DynamicThreeTerminalGate):

    """This class, a subclass of the class of three-terminal Dynamic
       gates, represents AND gates implemented using the interaction
       function
       
                                1            2
                               --- k (z - xy),
                                2
       
       where k is any real-valued constant (normally positive)
       representing the overall energy scale or "stiffness" of the
       interaction.  When the input coordinates x,y,z are at
       consistent logic values, the interaction energy is 0, and when
       they are at inconsistent logic values, the interaction energy
       is k/2.
                                                                      """

        #|----------------------------------------------------------------------
        #|
        #|  inst.__init__()                            [special instance method]
        #|
        #|      This instance initializer (constructor) for the
        #|      DynamicANDGate class takes the following arguments:
        #|
        #|          Required arguments:
        #|          -------------------
        #|
        #|              inputNodeA, inputNodeB : DynamicNode
        #|
        #|                  The AND gate's input nodes, which must have
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

    def __init__(me, inputNodeA:DynamicNode, inputNodeB:DynamicNode,
                 name:str=None, network:DynamicNetwork=None,
                 stiffness:Real = 1, outNodeName:str=None,
                 initOutPos:Real=None):

        """This instance initializer (constructor) for the
           DynamicANDGate class takes the following arguments:
        
                Required arguments:
                -------------------
        
                    inputNodeA, inputNodeB : DynamicNode
        
                        The AND gate's input nodes, which must have
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

            _logger.debug("Initializing a new DynamicANDGate named "
                          "'%s' in network '%s'" % (str(name), netname))

        #__/ End if doDebug


            #-------------------------------------------------------
            # Do default initialization that applies to all Dynamic
            # three-terminal gates.

        DynamicThreeTerminalGate.__init__(me, inputNodeA, inputNodeB,
                                          name=name, network=network,
                                          outNodeName=outNodeName,
                                          initOutPos=initOutPos)


            #---------------------------------------------
            # Set our interaction function appropriately.

        andFunc = DynamicANDFunction(stiffness)

        me.interaction = andFunc    

    #__/ End DynamicANDGate.__init__().
#__/ End class DynamicANDGate.


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                   BOTTOM OF FILE:    dynamicANDGate.py
#===============================================================================
