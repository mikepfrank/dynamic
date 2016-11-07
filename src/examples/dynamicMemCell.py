#|==============================================================================
#|                      TOP OF FILE:    dynamicMemCell.py
#|------------------------------------------------------------------------------
#|   The below module documentation string will be displayed by pydoc3.
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""
    FILE NAME:      dynamicMemCell.py                [Python module source file]

    FILE PATH:      $GIT_ROOT/dynamic/src/examples/dynamicMemCell.py

    MODULE NAME:    examples.dynamicMemCell

    IN COMPONENT:   Dynamic.examples    (device & network examples)


    MODULE DESCRIPTION:
    -------------------

        The dynamicMemCell module provides a simple implementation of
        a read-only memory cell implemented as a Dynamic gate with 0
        inputs, 1 output, and a simple quadratic potential energy
        function,

                                1           2
                               --- k (x - b),
                                2

        where k is a "stiffness" constant, x is the (generalized
        position) coordinate of the output node, and b is a bias value
        (normally either 0 or 1).

            Note that the energy is minimized when x = b.


    BASIC MODULE USAGE:
    -------------------

        from examples.dynamicMemCell import DynamicMemCell

        ...     // Create network myNet

        myMemCell = DynamicMemCell('myCell', network=myNet, biasval=1,
                                   outNodeName='X')


    PUBLIC CLASSES:
    ---------------

        See the class's docstring for details.

            DynamicMemCell                                 [module public class]

                The class of read-only memory cells defined in this
                module.
                            
                                                                             """
#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#| End of module documentation string for dynamicMemCell.py.
#|------------------------------------------------------------------------------

    #|==========================================================================
    #|   1. Module imports.                                [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #------------------------------------------
        # Imports from our parent module (package).

from . import _logger       # Our component logger.


        #--------------------------------------
        # Imports from standard Python modules.

from numbers import Real


        #-----------------------------------------------------------
        # Imports from custom modules in lower-level packages within
        # the Dynamic system.

from logmaster import doDebug   # Whether to show debug output.

from functions.quadraticFunction        import QuadraticFunction
from network.dynamicOneTerminalGate     import DynamicOneTerminalGate
from network.dynamicNetwork             import DynamicNetwork, netName
from functions.dynamicBiasFunction      import DynamicBiasFunction


    #|==========================================================================
    #|  2.  Global constants, variables, and objects.      [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|  2.1.  Special globals.                      [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global __all__              # List of public symbols exported by this module.

__all__ = [
    'DynamicMemCell'   # Class of Dynamic implementations of read-only memory cells.
    ]


    #|==========================================================================
    #|  3.  Class definitions.                             [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|   3.1.  Public classes.                      [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
            #|------------------------------------------------------------------
            #|
            #|      DynamicMemCell                         [module public class]
            #|
            #|          This class, a subclass of the class of one-
            #|          terminal Dynamic gates, represents read-only
            #|          memory cells implemented using the interaction
            #|          function
            #|
            #|                           1           2
            #|                          --- k (x - b),
            #|                           2
            #|
            #|          where k is any real-valued constant (normally
            #|          positive) representing the overall energy scale
            #|          or "stiffness" of the interaction.  When the
            #|          output coordinate x is equal to the bias value
            #|          b (which is normally 0 or 1), the interaction
            #|          energy is 0, and when they it is at the opposite
            #|          logic value, the interaction energy is k/2.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class DynamicMemCell(DynamicOneTerminalGate):

    """This class, a subclass of the class of one-terminal Dynamic
       gates, represents read-only memory cells implemented using the
       interaction function

                                1           2
                               --- k (x - b),
                                2

       where k is any real-valued constant (normally positive)
       representing the overall energy scale or "stiffness" of the
       interaction.  When the output coordinate x is equal to the bias
       value b (which is normally 0 or 1), the interaction energy is
       0, and when they it is at the opposite logic value, the
       interaction energy is k/2.                                     """

        #|----------------------------------------------------------------------
        #|
        #|  inst.__init__()                            [special instance method]
        #|
        #|      This instance initializer (constructor) for the
        #|      DynamicMemCell class initializes a dynamic memory
        #|      cell; the output node is also created.  By default
        #|      it has zero bias and unit "stiffness."  It takes
        #|      the following arguments:
        #|
        #|          Optional keyword arguments:
        #|          ---------------------------
        #|
        #|              name : str = None
        #|
        #|                  The name of this cell, if any.  (If not
        #|                  provided or None, no name is assigned.)
        #|
        #|              network : DynamicNetwork = None
        #|
        #|                  The Dynamic network that this cell will be
        #|                  a part of.  If not provided or None, the
        #|                  cell will not be added to a network.
        #|
        #|              stiffness : Real = 1
        #|
        #|                  The stiffness value for this cell's
        #|                  potential energy function.  If not
        #|                  provided or None, defaults to the value
        #|                  1.
        #|
        #|              outNodeName : str = None
        #|
        #|                  The name that should be given to this
        #|                  gate's output node, which will be newly
        #|                  created.  If not provided or None, defaults
        #|                  to (what?).  The name will be uniqified.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def __init__(inst, name:str=None, network:DynamicNetwork=None,
                 biasval:Real=0, stiffness:Real=1, outNodeName:str=None):

        """This instance initializer (constructor) for the
           DynamicMemCell class initializes a dynamic memory cell;
           the output node is also created.  By default the newly-
           created cell has zero bias and unit "stiffness."  The
           constructor takes the following arguments:
        
                  Optional keyword arguments:
                  ---------------------------
        
                      name : str = None
        
                          The name of this cell, if any.  (If not
                          provided or None, no name is assigned.)
        
                      network : DynamicNetwork = None
        
                          The Dynamic network that this cell will be
                          a part of.  If not provided or None, the
                          cell will not be added to a network.
        
                      stiffness : Real = 1
        
                          The stiffness value for this cell's
                          potential energy function.  If not
                          provided or None, defaults to the value
                          1.
        
                      outNodeName : str = None
        
                          The name that should be given to this
                          gate's output node, which will be newly
                          created.  If not provided or None, defaults
                          to (what?).  The name will be uniqified.    """

            #----------------------------------------
            # Maybe do some debug-level diagnostics.
        
        if doDebug:
            
                # Retrieve string name of network.  Does some error-handling.
            netname = netName(network)

            _logger.debug("Initializing a new DynamicMemCell named "
                          "'%s' in network '%s'" % (str(name), netname))

        #__/ End if doDebug

            
            #-------------------------------------------------------
            # Do default initialization that applies to all Dynamic
            # one-terminal gates. (Create port & output node, link
            # it to our output port.)

        DynamicOneTerminalGate.__init__(inst, name=name, network=network,
                                        outNodeName=outNodeName)

            #---------------------------------------------------------
            # Create the potential energy function constraining the
            # output node.

        if doDebug:
            _logger.debug("Setting up %s's dynamic bias function with bias "
                          "value %f and stiffness %f..." %
                              (str(inst), biasval, stiffness))

        biasFunc = DynamicBiasFunction(biasval, stiffness)

            # Set the potential function of this DynamicOneTerminalGate
            # to that function.

        inst.potential = biasFunc

        if doDebug:
            _logger.debug("DynamicMemCell.__init__(): Output node momentum is: %f" % 
                          inst.outputNode.coord.momentum.value)

            # Initialize position to minimum-energy value.

        if biasval != 0:
            inst.outputNode.coord.position.value = biasval

    #__/ End DynamicMemCell.__init__().

#__/ End class DynamicMemCell.

#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#|                  BOTTOM OF FILE:    dynamicMemCell.py
#|==============================================================================
