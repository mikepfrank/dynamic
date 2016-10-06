#|==============================================================================
#|                                  TOP OF FILE
#|
#|      File name:  kineticEnergyFunction.py    [Python module source file]
#|
#|      Description:
#|
#|          This module defines an abstract base class from which to
#|          derive kinetic energy function classes, which should not
#|          itself be instantiated.
#|
#|          It also defines a simple default quadratic kinetic energy
#|          function subclass.
#|

from .differentiableFunction import BaseDifferentiableFunction
from .quadraticFunction      import SimpleQuadraticFunction

__all__ = ['BaseKineticEnergyFunction']

class BaseKineticEnergyFunction(BaseDifferentiableFunction):  pass

# A simple quadratic kinetic energy function is of the form
#
#       K(x) = (1/2) m (v**2)
#
# where m is a generalized mass and v a generalized velocity.

class SimpleQuadraticKineticEnergyFunction(BaseKineticEnergyFunction,
                                           SimpleQuadraticFunction):

        # 

    def __init__(inst, name:str='K', argName:str='v', m=None):

        #print("SQKEF name=%s argName=%s m=%s" % (name, argName, str(m)))

            # If mass was not provided, default to unit mass.

        if m == None:  m=1

            # Do generic initialization for simple quadratic functions.
        
        SimpleQuadraticFunction.__init__(inst, name, argName, m/2)

