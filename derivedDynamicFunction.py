from typing             import Callable,Iterable,Iterator,Set

import logmaster
logger = logmaster.getLogger(logmaster.sysName + '.simulator')
    # The dynamicVariable module is part of our core simulation component.

from partialEvalFunc    import PartiallyEvaluatableFunction
from dynamicVariable    import DynamicVariable
from dynamicFunction    import BaseDynamicFunction

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

        logger.debug("DerivedDynamicFunction.evaluateWith():  Evaluating function %s (%s) with arguments: %s %s" %
                     (str(inst), str(inst._function), str(args), str(kwargs)))

            # What argList to give here in the case of a Hamiltonian
            # whose function doesn't have an explicit argument list?
            # (In fact this will be the default.)  Does it even make
            # sense to partially evaluate such a Hamiltonian?
        
        pef = PartiallyEvaluatableFunction(function=inst._function)

            # Prepend the values of our variables to the list of actual arguments provided.

        logger.debug("DerivedDynamicFunction.evaluateWith(): Extending argument list with values of variables: %s"
                    % str(inst._varList))
        
        args = list(map(lambda v: v(), inst._varList)) + list(args)

        logger.debug("DerivedDynamicFunction.evaluateWith(): Evaluating %s with extended argument list: %s %s" %
                    (str(inst), str(args), str(kwargs)))

        value = pef(*args, **kwargs)
        logger.debug("DerivedDynamicFunction.evaluateWith():  Got value %s = %s." % (str(inst), str(value)))
        
        return value

