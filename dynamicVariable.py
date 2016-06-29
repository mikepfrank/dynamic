from fixed  import Fixed     # Fixed-precision math class.
from typing import Callable,Iterable

import logmaster

from differentiableFunction import BaseDifferentiableFunction
from partialEvalFunc        import PartiallyEvaluatableFunction
from dynamicFunction        import BaseDynamicFunction,MultiplierDynamicFunction

__all__ = ['SimulationException',
           'TimestepException',
           'TimestepParityException',
           'UnsetTimeDerivativeException',
           'UnindexedVariableException',

           'DynamicVariable',
           'DerivedDynamicFunction',
           'DifferentiableDynamicFunction']

logger = logmaster.getLogger(logmaster.sysName + '.simulator')
    # The dynamicVariable module is part of our core simulation component.

class SimulationException(Exception): pass

class TimestepException(SimulationException): pass

class TimestepParityException(TimestepException): pass

class UnsetTimeDerivativeException(TimestepException): pass

class UnindexedVariableException(SimulationException): pass

class NoIntermediateVariableException(SimulationException): pass

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

    def __init__(inst, name:str=None, value:Fixed=None, time:int=0,
                 timeDeriv:BaseDynamicFunction=None):

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
##            raise TimestepParityException(errStr)

        # Proceed either forward or backward as needed till we get there.

        while timestep > this.time:
            this.stepForward()

        while timestep < this.time:
            this.stepBackward()

    # Steps forwards in time by one minimal time increment (+2 units).

    def stepForward(this):

        logger.info("Stepping variable %s forward from time step %d..." %
                    (this.name, this.time))

        # print("value=%s, timeDeriv=%s" % (str(this.value), str(this.timeDeriv)))

            # If this dynamic variable's time-derivative function has not yet
            # been defined, then of course we can't step it forwards in time yet.
            # Severe bug in program logic!  Log an error an raise an exception.

        if this.timeDeriv == None:
            errStr = "Variable %s's time derivative is not yet defined!" % this.name
            logger.error("DynamicVariable.stepForward: " + errStr)
            raise UnsetTimeDerivativeException(errStr)

        logger.debug(("DynamicVariable.stepForward():  " +
                      "Attempt to evaluate time derivative function %s at time step %d...")
                     % (str(this.timeDeriv), (this.time + 1)))

        derivVal = this.timeDeriv(this.time + 1)

        logger.info(("DynamicVariable.stepForward():  " +
                     "Got the time derivative value %f...")
                     % float(derivVal))

        logger.normal("Stepping variable %s from %f @ time %d to %f @ time %d (delta = %f)" %
                      (this.name, this.value, this.time,
                       this.value + derivVal, this.time + 2,
                       derivVal))

        this.value = this.value + derivVal
        this.time  = this.time + 2

        logger.info("Stepped variable %s forward to value %f at time %d..." %
                    (this.name, float(this.value), this.time))

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

    def __init__(self, name:str=None, varList:Iterable[DynamicVariable]=[], function:Callable=None):

        self._varList = list(varList)

        BaseDynamicFunction.__init__(self, name, function)

    @property
    def varList(self): return self._varList

    @property
    def function(self): return self._function

##    def evaluator(inst, *args, **kwargs):
##
##        logger.debug("DerivedDynamicFunction.evaluator(): Evaluating derived dynamic function %s..." % str(inst))
##        
####        if len(args) == 0 and len(kwargs) == 0:
####            return inst         # No arguments provided: Leave the function unevaluated.
####        else:
##            
##        return inst.evaluateWith(*args, **kwargs)     # Needs further processing.

    def evolveTo(inst, timestep:int):

        logger.debug("DerivedDynamicFunction.evolveTo():  Evolving internal variables to timestep %d..." % timestep)
        
        for var in inst._varList:
            var.evolveTo(timestep)

    def evaluateWith(inst, *args, **kwargs):

        logger.normal("DerivedDynamicFunction.evaluateWith():  Evaluating function %s (%s) with arguments: %s %s" %
                     (str(inst), str(inst._function), str(args), str(kwargs)))

            # What argList to give here in the case of a Hamiltonian
            # whose function doesn't have an explicit argument list?
            # (In fact this will be the default.)  Does it even make
            # sense to partially evaluate such a Hamiltonian?
        
        pef = PartiallyEvaluatableFunction(function=inst._function)

            # Prepend the values of our variables to the list of actual arguments provided.

        logger.info("DerivedDynamicFunction.evaluateWith(): Extending argument list with values of variables: %s"
                    % str(inst._varList))
        
        args = list(map(lambda v: v(), inst._varList)) + list(args)

        logger.info("DerivedDynamicFunction.evaluateWith(): Evaluating %s with extended argument list: %s %s" %
                    (str(inst), str(args), str(kwargs)))

        value = pef(*args, **kwargs)
        logger.normal("DerivedDynamicFunction.evaluateWith():  Got value %s = %s." % (str(inst), str(value)))
        
        return value

# A DifferentiableDynamicFunction is a DerivedDynamicFunction
# (derived from a set of DynamicVariables) that also sports the
# feature of being able to return, for any one of those variables,
# another DerivedDynamicFunction which represents the partial
# derivative of the original function with respect to the variables.

class DifferentiableDynamicFunction(DerivedDynamicFunction):

    # Instance public data members:
    #
    #       inst.name:str  -  A human-readable name of this function, as a string.
    #
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

    def __init__(inst, name:str=None, varList:Iterable[DynamicVariable]=[],
                 function:BaseDifferentiableFunction=None):

            # First do generic initialization for DerivedDynamicFunction instances.
            # This remembers our variable list and our associated evaluation function.

        DerivedDynamicFunction.__init__(inst, name, varList, function)

        inst.initializeVarIndex()

            # Add all the given variables to our list of variables we can
            # be differentiated by.  NOTE: If one of those "variables" is iself
            # actually a DifferentiableDynamicFunction of some other varibles,
            # we can go on and add the variables that it depends on as well!

        for var in varList:
            inst.addVariable(var)

            # The following is kind of clumsy; it won't work if there is more
            # than one level of nested sub-variables.  Fix this at some point.

        for var in varList:
            if isinstance(var, DifferentiableDynamicFunction):
                logger.debug(("DifferentiableDynamicFunction.__init__(): " +
                              "Variable %s of %s is itself a DifferentiableDynamicFunction " +
                              "so let's also add the variables it depends on.") %
                             (str(var), str(inst)))
                for subvar in var.varList:
                    inst.addVariable(subvar)

        logger.debug(("DifferentiableDynamicFunction.__init__(): "
                      "Setting ._function attribute of DDF %s to %s")
                     % (str(inst), str(function)))

        if function != None:
            inst._function = function       # Remember the function, if provided.

        inst._partials = dict()         # Initially empty cache of partials.

    def initializeVarIndex(inst):
        inst._varIndex = dict()
        if hasattr(inst, '_varList'):
            for var in inst._varList:
                index = inst._varList.index(var)
                inst._varIndex[var] = index

    # Adds a variable to the list of variables we can be differentiated by.
    # Doesn't attempt to figure out what our partial is WRT the new variable yet.

    def addVariable(inst, var:DynamicVariable):

        logger.info(("DifferentiableDynamicFunction.addVariable():  " +
                      "Adding variable %s to the list of variables that " +
                      "function %s can be differentiated by...") % (str(var), str(inst)))

            # Create our variable list if it doesn't exist yet.

        if not hasattr(inst, '_varList'):
            inst._varList = []

            # Create our variable index if it doesn't exist yet.

        if not hasattr(inst, '_varIndex'):
            inst._varIndex = dict()

            # If the variable isn't already in the variable list, add it.

        if var not in inst._varIndex:

            logger.debug(("DifferentiableDynamicFunction.addVariable():  " +
                          "Previously %s's variable list was %s.") % (str(var), str(inst._varList)))
            logger.debug(("DifferentiableDynamicFunction.addVariable():  " +
                          "Previously %s's variable index was %s.") % (str(var), str(inst._varIndex)))
            
                # Figure out what this new variable's index is in the last.

            index = len(inst._varList)

                # Add the new variable to the list.

            inst._varList.append(var)

                # Add the new variable's index to the index.

            inst._varIndex[var] = index

            logger.debug(("DifferentiableDynamicFunction.addVariable():  " +
                          "Added variable %s to %s's variable list in the " +
                          "%d'th position.") % (str(var), str(inst), index))

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

        if v not in self._varIndex:

            # If we can't do df/dv directly, search for another variable v' such
            # that we can compute df/dv = df/dv' * dv'/dv.  NOTE: This is presently
            # limited to only one level of chaining.
            
            dynPartial = self.chainRuleSearch(v)

            if dynPartial == None:        
                errmsg = ("Could not find any intermediate variable for chain rule when " +
                          "attempting to differentiate %s with respect to %s.")%(str(self),str(v))

                logger.critical("DifferentiableDynamicFunction.chainRuleSearch: " + errmsg)
        
                raise NoIntermediateVariableException(errmsg)

##            errmsg = ("DyanmicVariable %s not found in _varIndex{} of " +
##                      "DifferentiableDynamicFunction %s!") % (str(v), str(self))
##            logger.exception("DifferentiableDynamicFunction.dynPartialDerivWRT(): " + errmsg)
##            raise 

        else:

            logger.debug("DifferentiableDynamicFunction.dynPartialDerivWRT(): " +
                         "Looking up the index of DynamicVariable %s..." % str(v))

            logger.debug("The ._varIndex dict of %s is %s." % (str(self), str(self._varIndex)))

            varIndex = self._varIndex[v]    # Look up this variable's index in our list.

            logger.debug("DifferentiableDynamicFunction.dynPartialDerivWRT(): " +
                         "The index of DynamicVariable %s is %d..." % (str(v), varIndex))

                # We may have previously constructed the dynamic function for
                # this particular partial derivative.  If so, just look it up.

            if varIndex in self._partials:
                return self._partials[varIndex]

                # Check to see if this is a case where we can use the chain rule.

            dynPartial = self.chainRuleSearch(v)

            if dynPartial == None:

                    # Ask our BaseDifferentiableFunction for its partial derivative
                    # with respect to the <varIndex>'th variable.  Note that at this
                    # point, this function is still unevaluated.

                try:
                    try:
                        partial = self._function.partialDerivWRT(varIndex)
                    except IndexError as e:
                        logger.exception(("DifferentiableDynamicFunction.dynPartialDerivWRT(): " +
                                          "IndexError exception in %s trying to find the partial derivative of %s " +
                                          "with respect to %s!") % (str(self), str(self._function), str(v)))
                        raise e
                    
                    # Now construct a dynamic function corresponding to this partial
                    # derivative and remember it.

                    dynPartial = DerivedDynamicFunction("d%s_over_d%s"%(self.name,v.name), self.varList, partial)
                    
                except TypeError as e:
                    logger.exception(("DifferentiableDynamicFunction.dynPartialDerivWRT(): " +
                                      "TypeError exception in %s trying to find the partial derivative of %s " +
                                      "with respect to %s!") % (str(self), str(self._function), str(v)))
                    raise e

            # Cache this result so we don't have to recalculate it each time.
            
        self._partials[varIndex] = dynPartial

            # Return that dude.

        return dynPartial
    
    def chainRuleSearch(self, v:DynamicVariable) -> DerivedDynamicFunction:

        # Search all possible intermediate variables.

        for var in self._varIndex:

            if isinstance(var, DifferentiableDynamicFunction):
                
                if v in var._varIndex:

                    # First, find the partial of self with respect to var.

                    leftPartial = self.dynPartialDerivWRT(var)

                    logger.info("The partial of %s with respect to %s is %s..." %
                                (str(self), str(var), str(leftPartial)))

                    # Next, find the partial of var with respect to v.

                    rightPartial = var.dynPartialDerivWRT(v)

                    logger.info("The partial of %s with respect to %s is %s..." %
                                (str(var), str(v), str(rightPartial)))

                    # Now multiply them.

                    overallPartial = leftPartial * rightPartial

                    # Remember that, yes, we are a function of v.

                    self.addVariable(v)

                    return overallPartial

        return None


            
