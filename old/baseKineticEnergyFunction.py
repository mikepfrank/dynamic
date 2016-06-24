#|==============================================================================
#|                                  TOP OF FILE
#|
#|      File name:  BaseKineticEnergyFunction.py    [Python module source file]
#|
#|      Description:
#|
#|          This module defines an abstract base class from which to
#|          derive kinetic energy function classes.  It should not
#|          itself be instantiated.
#|

__all__ = ['BaseKineticEnergyFunction']

class BaseKineticEnergyFunction(BaseDifferentiableFunction):

        # Special methods.

    def __init__(inst):     pass                # Does nothing - subclass should override.

        # Public member function placeholders.

        # evaluate - This evaluates the given kinetic energy function
        #   with the given argument list and returns the value of the
        #   function when applied to those arguments.

    def evaluate(this, arglist):    pass        # Does nothing - subclass should override.

        # evalPartialDeriv - This evaluates the partial derivative of
        #   the given kinetic energy function with the given argument
        #   list, with respect to the specified argument (specified with
        #   an integer from 1 to the number of arguments).

    def evalPartialDeriv(this, whicharg, arglist):  pass        # Does nothing - subclass should override.
