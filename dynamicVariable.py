from fixed  import Fixed     # Fixed-precision math class.
from typing import Callable,Iterable

import logmaster; from logmaster import *
logger = getLogger(logmaster.sysName + '.simulator')
    # The dynamicVariable module is part of our core simulation component.

from differentiableFunction import BaseDifferentiableFunction
from dynamicFunction        import BaseDynamicFunction,MultiplierDynamicFunction
#from simulationContext      import SimulationContext
# Introduces circularity!

class SimulationContext: pass

__all__ = ['SimulationError',
           'TimestepError',
           'TimestepParityError',
           'UnsetTimeDerivativeError',
           'UnindexedVariableError',

           'DynamicVariable',
           'DerivedDynamicFunction',
           'DifferentiableDynamicFunction']

class SimulationError(Exception): pass

class TimestepError(SimulationError): pass

class TimestepParityError(TimestepError): pass

class UnsetTimeDerivativeError(TimestepError): pass

class UnindexedVariableError(SimulationError): pass

class NoIntermediateVariableError(SimulationError): pass

class NoSimulationContextError(SimulationError): pass

#   A dynamic variable (a.k.a., generalized coordinate, degree of freedom)
#   could in general correspond to either a generalized position, or to a
#   corresponding generalized velocity.
#
#   In Dynamic, a variable has the following general features:
#
#       * (Optional) a name, which is usually derived from
#           the name of the corresponding simulation node.
#
#       * A present value, which is a fixed-point number;
#
#       * A time-step number, which is the index of the present
#           point in time at which the variable has that value.
#
#       * A function giving the value of the time-derivative
#           of the variable at any given time step.
#
#   And, a variable supports the following operations:
#
#       * Evolve it to the given point in time (integer).
#
#       * Evolve forwards or backwards in time by a minimal amount.
#           (This is usually two time steps, for reasons given below.)
#
#   To ensure reversibility, the time-derivative function may not depend
#   directly on the present value of the variable at the same time step.
#
#   During simulation, variables will typically get updated in leapfrog
#   (centered-difference) fashion, so that, for example:
#
#               v(t) + 2Dv(t+1) = v(t+2).
#
#   where Dv = (dv/dt)*Dt is the delta of v extrapolated from the
#   derivative and the time delta Dt.
#
#   Since the arithmetic is fixed-point, addition is reversible, and so
#   this kind of leapfrog-style update can be exactly reversed.  This
#   ensures that the simulation is thermodynamically sound.
#
#   Normally in Dynamic, a position variable gets updated based on
#   velocity variables at adjacent time steps, and vice-versa.  It
#   would be possible to have update schemes involving cycles with
#   more than two phases (triple-leapfrog, etc.), but we do not plan
#   to explore that possibility at present.
#

class DynamicVariable(BaseDynamicFunction):

    # Public data members:
    #
    #   .name [str]
    #
    #           The name of this variable, a string.  No default.
    #           Variable names should be unique within a given simulation.
    #
    #   .value [Fixed]
    #
    #           The current value of this variable, a fixed-point
    #           number.  Initially defaults to 0.
    #
    #   .time [int]
    #
    #           The integer index of the current time step.
    #           Initially defaults to 0.
    #
    # Public properties:
    #
    #   .timeDeriv [Callable[[int],Fixed]]
    #
    #           A function that takes an integer time-step
    #           number, and returns what the time derivative
    #           of this variable would be at that time step.
    #           This should be prescaled by 2Dt (two time units).
    #
    #           We can expect that this function will work by
    #           internally causing other state variables to
    #           evolve to the requested point in time as needed.
    #
    #   .context:SimulationContext
    #
    #           The global simulation context under which this dynamic
    #           variable's time-evolution will be simulated.
    #
    # Private data members:
    #
    #   ._timeDeriv [Callable[[int],Fixed]]
    #
    #           A function that takes an integer time-step
    #           number, and returns what the time derivative
    #           of this variable would be at that time step.
    #           This should be prescaled by 2Dt (two time units).
    #
    #           We can expect that this function will work by
    #           internally causing other state variables to
    #           evolve to the requested point in time as needed.
    #
    #           Accessed through the .timeDeriv public @property.
    #
    #   ._context:SimulationContext
    #
    #           The global simulation context under which this dynamic
    #           variable's time-evolution will be simulated.
    #
    #   

    def __init__(inst, name:str=None, value:Fixed=None, time:int=0,
                 timeDeriv:BaseDynamicFunction=None,
                 context:SimulationContext=None):

        if doDebug:
            logger.debug("Initializing the DynamicVariable named %s..." % name)

            # Do default initialization for BaseDynamicFunctions.
            # We don't specify an underlying function here, since
            # our job as a dynamic variable is to track our current
            # value via dynamical simulation instead.

        BaseDynamicFunction.__init__(inst, name)

            # If no initial value was specified for this dynamic
            # variable, just default its initial value to (fixed-point)
            # zero.

        if value is None:
            value = Fixed(0)

        if name != None:  inst.name = name

        if timeDeriv != None:  inst._timeDeriv = timeDeriv

        inst.value = value
        inst.time = time

        inst.context = context

# Now this is in BaseDynamicFunction
##    def renameTo(me, name:str):
##        me.name = name

    @property
    def value(me):
        if hasattr(me, '_value'):
            return me._value
        else:
            return None

    @value.setter
    def value(me,value):
        me._value = value

    @property
    def timeDeriv(self):
        if hasattr(self,'_timeDeriv'):
            return self._timeDeriv
        else:
            return None

    @property
    def context(self):
        if hasattr(self,'_context'):
            return self._context
        else:
            return None

    @context.setter
    def context(self, sc:SimulationContext):
        if sc is not None:
            self._context = sc
        else:
            del self.context

    @context.deleter
    def context(self):
        if hasattr(self,'_context'):
            del self._context

##    @timeDeriv.setter
##    def timeDeriv(self, timeDeriv:BaseDynamicFunction):
##        if timeDeriv != None:
##            self._timeDeriv = timeDeriv

    def evaluateWith(self, **args):
        return self.value               # Ignore any arguments provided.

    # Cause the variable to update itself to the given point
    # in time (specified as an integer time-step number).  If
    # the parities of current and requested time-step numbers
    # do not match, throws a TimestepParity exception.

    def evolveTo(this, timestep:int):

        # First, make sure that the time parities match.  If they don't, then
        # we can't actually get to the time requested.  In that case, just get
        # as close as we can instead (without going over).

        if (timestep - this.time)%2 != 0:

                # Nudge timestep one unit closer to the current time.

            if timestep > this.time:
                timestep -= 1
            else:
                timestep += 1
            
##            errStr = ("Can't evolve dynamic variable %s from time step %d to %d " +
##                      "because parities don't match")%(str(this), this.time, timestep)
##            logger.error("DynamicVariable.evolveTo: "+errStr)
##            raise TimestepParityError(errStr)

        # Proceed either forward or backward as needed till we get there.

        while timestep > this.time:
            this.stepForward()

        while timestep < this.time:
            this.stepBackward()

    # Steps forwards in time by one minimal time increment (+2 units).

    def stepForward(this, nSteps:int=2):

        # Special case: If we are asked to step forward by some specific amount
        # other than the minimal 2 steps, instead calculate the destination time
        # step value, and then call the more general evolveTo() method.  Then that
        # will call back to this method the appropriate number of times.

        if nSteps != 2:
            this.evolveTo(this.time + nSteps)
            return

        if doDebug:
            logger.debug("Stepping variable %s forward from time step %d..." %
                        (this.name, this.time))

        # print("value=%s, timeDeriv=%s" % (str(this.value), str(this.timeDeriv)))

            # If this dynamic variable's time-derivative function has not yet
            # been defined, then of course we can't step it forwards in time yet.
            # Severe bug in program logic!  Log an error an raise an exception.

        if this.timeDeriv == None:
            errStr = "Variable %s's time derivative is not yet defined!" % this.name
            logger.error("DynamicVariable.stepForward: " + errStr)
            raise UnsetTimeDerivativeError(errStr)

        if doDebug:
            logger.debug(("DynamicVariable.stepForward():  For variable %s:  " +
                          "Attempt to evaluate time derivative function %s at time step %d...")
                         % (str(this), str(this.timeDeriv), (this.time + 1)))

        derivVal = this.timeDeriv(this.time + 1)

        if doDebug:
            logger.debug(("DynamicVariable.stepForward():  For variable %s at time %d:  " +
                          "Got the time derivative value %f...")
                         % (str(this), this.time + 1, float(derivVal)))

##        logger.normal("Stepping variable %s from %f @ time %d to %f @ time %d (delta = %f)" %
##                      (this.name, this.value, this.time,
##                       this.value + derivVal, this.time + 2,
##                       derivVal))

        context = this.context
        if context is None:
            errmsg = ("Can't step variable %s forward because it doesn't have a "
                      "simulation context!") % str(this)
            logger.exception("DynamicVariable.stepForward(): " + errmsg)
            raise NoSimulationContextError(errmsg)

        this.value = this.value + 2* derivVal * context.timedelta
        this.time  = this.time + 2

        if doDebug:
            logger.debug("Stepped variable %s forward to value %f at time %d..." %
                        (this.name, float(this.value), this.time))

    # Steps backwards in time by one minimal time increment (-2 units).

    def stepBackward(this, nSteps:int=2):

        # Special case: If we are asked to step backward by some specific amount
        # other than the minimal 2 steps, instead calculate the destination time
        # step value, and then call the more general evolveTo() method.  Then that
        # will call back to this method the appropriate number of times.

        if nSteps != 2:
            this.evolveTo(this.time - nSteps)
            return

        context = this.context
        if context is None:
            errmsg = ("Can't step variable %s backward because it doesn't have a "
                      "simulation context!") % str(this)
            logger.exception("DynamicVariable.stepBackward(): " + errmsg)
            raise NoSimulationContextError(errmsg)

        this.value = this.value - 2 * this.timeDeriv(this.time - 1) * context.timedelta
        this.time  = this.time - 2

    def __str__(me):
        
        name = me.name if me.name != None else '_' # placeholder

        if me.value is None:
            return name
        else:
            return "%s=%f@%d" % (str(me.name), float(me.value), int(me.time))
    
