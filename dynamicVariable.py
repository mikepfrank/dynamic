from fixed  import Fixed     # Fixed-precision math class.
from typing import Callable,Iterable

import logmaster

from differentiableFunction import BaseDifferentiableFunction
from partialEvalFunc        import PartiallyEvaluatableFunction
from dynamicFunction        import BaseDynamicFunction

__all__ = ['SimulationException',
           'TimestepException',
           'TimestepParity',

           'DynamicVariable',
           'DerivedDynamicFunction']

logger = logmaster.getLogger(logmaster.sysName + '.simulator')
    # The dynamicVariable module is part of our core simulation component.

class SimulationException(Exception): pass

class TimestepException(SimulationException): pass

class TimestepParityException(TimestepException): pass

class UnsetTimeDerivativeException(TimestepException): pass

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
    #   

    def __init__(inst, name:str=None, value:Fixed=Fixed(0), time:int=0,
                 timeDeriv:BaseDynamicFunction=None):

        logger.debug("Initializing the DynamicVariable named %s..." % name)

        if name != None:  inst.name = name

        if timeDeriv != None:  inst._timeDeriv = timeDeriv

        inst.value = value
        inst.time = time

    @property
    def timeDeriv(self):
        if hasattr(self,'_timeDeriv'):
            return self._timeDeriv
        else:
            return None

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

        # First, make sure that the time parities match.

        if (timestep - this.time)%2 != 0:
            errStr = ("Can't get from time step %d to %d " +
                      "because parities don't match")%(this.time,timestep)
            logger.error("DynamicVariable.evolveTo: "+errStr)
            raise TimestepParityException(errStr)

        # Proceed either forward or backward as needed till we get there.

        while timestep > this.time:
            this.stepForward()

        while timestep < this.time:
            this.stepBackward()

    # Steps forwards in time by one minimal time increment (+2 units).

    def stepForward(this):

        # print("value=%s, timeDeriv=%s" % (str(this.value), str(this.timeDeriv)))

            # If this dynamic variable's time-derivative function has not yet
            # been defined, then of course we can't step it forwards in time yet.
            # Severe bug in program logic!  Log an error an raise an exception.

        if this.timeDeriv == None:
            errStr = "Variable %s's time derivative is not yet defined!" % this.name
            logger.error("DynamicVariable.stepForward: " + errStr)
            raise UnsetTimeDerivativeException(errStr)


        this.value = this.value + this.timeDeriv(this.time + 1)
        this.time  = this.time + 2

        logger.debug("Stepped variable %s forward to time %d..." %
                     (this.name, this.time))

    # Steps backwards in time by one minimal time increment (-2 units).

    def stepBackward(this):

        this.value = this.value - this.timeDeriv(this.time - 1)
        this.time  = this.time - 2

# This is a general class for dynamic functions that are expressed as some
# arbitrary derived function of some list of underlying dynamic variables.
# NOTE: We assume the given list of N variables will supply the first N
# arguments of the given function.  The function may have other arguments.

class DerivedDynamicFunction(BaseDynamicFunction):

    # At whatever point it's provided, the <function> should take at
    # least as many arguments as there are variables in <varList>.

    def __init__(self, varList:Iterable[DynamicVariable]=[], function:Callable=None):
        self._varList = list(varList)
        self._function = function

    @property
    def varList(self): return self._varList

    @property
    def function(self): return self._function

    def evolveTo(inst, timestep:int):
        for var in inst._varList:
            var.evolveTo(timestep)

    def evaluateWith(inst, *args, **kwargs):

            # What argList to give here in the case of a Hamiltonian
            # whose function doesn't have an explicit argument list?
            # (In fact this will be the default.)  Does it even make
            # sense to partially evaluate such a Hamiltonian?
        
        pef = PartiallyEvaluatableFunction(function=self._function)

            # Prepend the values of our variables to the list of actual arguments provided.
        
        args = map(lambda v: v(), self._varList) + args
        
        return pef(*args, **kwargs)

# A DifferentiableDynamicFunction is a DerivedDynamicFunction
# (derived from a set of DynamicVariables) that also sports the
# feature of being able to return, for any one of those variables,
# another DerivedDynamicFunction which represents the partial
# derivative of the original function with respect to the variables.

class DifferentiableDynamicFunction(DerivedDynamicFunction):

    # Instance private data members:
    #
    #       inst._varList:List[DynamicVariable]
    #
    #           The list of dynamical variables that the value of this
    #           term depends on.
    #
    #       inst._varIndex:Dict[DynamicVariable,int]
    #
    #           Maps a dynamical variable to its index within our list.
    #           This facilitates fast lookups of particular variables.
    #
    #       inst._function:BaseDifferentiableFunction
    #           (Inherited from DerivedDynamicFunction.)
    #
    #           The function that computes the value of this term given
    #           values for all of its variables.
    #
    #       inst._partials:Dict[BaseDynamicFunction]
    #
    #           These dynamic functions are the partial derivatives
    #           of this term with respect to its variables.  The key
    #           to this dict is the variable index in [0..nVars-1].
    #           This is just a cache of partials computed elsewhere.

    # This initializer takes a list of the dynamic variables that this
    # term involves, and a differentiable function giving the value of
    # this term (given values of the variables).  The dynamical variables
    # in the given <varlist> must correspond (in the same order!) to the
    # arguments to the given function.

    def __init__(inst, varList:Iterable[DynamicVariable]=[],
                 function:BaseDifferentiableFunction=None):

            # First do generic initialization for DerivedDynamicFunction instances.
            # This remembers our variable list and our associated evaluation function.

        DerivedDynamicFunction.__init__(inst, varList, function)

            # Construct our map from variables to their indices.

        inst._varIndex = dict()
        for index in range(len(varList)):
            inst._varIndex[varList[index]] = index

        if function != None:
            inst._function = function       # Remember the function, if provided.

        inst._partials = dict()         # Initially empty cache of partials.

    # Instance public methods:
    #
    #   .dynPartialDerivWRT(v:DynamicVariable) - Given the identification
    #       of one of the dynamic variables that this DerivedDynamicFunction
    #       depends on, return another DerivedDynamicFunction which
    #       is a callable function that, given a point in time t, evaluates
    #       the partial derivative of the term with respect to that
    #       variable at that point in time (given the values that other
    #       variables would have at that point in time).

    def dynPartialDerivWRT(self, v:DynamicVariable) -> DerivedDynamicFunction:

        logger.debug("DifferentiableDynamicFunction.dynPartialDerivWRT(): " +
                     "Looking up the index of DynamicVariable %s..." % str(v))

        varIndex = self._varIndex[v]    # Look up this variable's index in our list.

            # We may have previously constructed the dynamic function for
            # this particular partial derivative.  If so, just look it up.

        if varIndex in self._partials:
            return self._partials[varIndex]

            # Ask our BaseDifferentialFunction for its partial derivative
            # with respect to the <varIndex>'th variable.  Note that at this
            # point, this function is still unevaluated.

        partial = self._function.partialDerivWRT(varIndex)

            # Now construct a dynamic function corresponding to this partial
            # derivative and remember it.

        dynPartial = DerivedDynamicFunction(self.varList, partial)
        self._partials[varIndex] = dynPartial

            # Return that dude.

        return dynPartial
    
