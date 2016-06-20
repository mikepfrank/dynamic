#|==============================================================================
#|                                  TOP OF FILE
#|------------------------------------------------------------------------------
#|
#|      File name:  QuadraticKineticEnergyFunction.py
#|
#|      File type:                                  [Python module source file]
#|

from BaseKineticEnergyFunction import *

__all__ = ['QuadraticKineticEnergyFunction']

class QuadraticKineticEnergyFunction(BaseKineticEnergyFunction):

    def __init__(inst, mass):
        inst.mass = mass

    def evaluate(this, arglist):
        x = arglist[0]
        return 0.5 * this.mass * x * x

    def evalPartialDeriv(this, whicharg, arglist):
        x = arglist[0]
        return this.mass * x

