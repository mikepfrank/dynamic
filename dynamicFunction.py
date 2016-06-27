from abc    import *
from typing import Any,Callable,Iterable

from fixed import Fixed

import logmaster

logger = logmaster.getLogger(logmaster.sysName + '.simulator')

__all__ = ['BaseDynamicFunction',
           'NullDynamicFunction',
           'NegatorDynamicFunction',
           'AdderDynamicFunction'
           'SummerDynamicFunction']

# dynamicFunction.py

class NullDynamicFunction:      pass
class NegatorDynamicFunction:   pass
class AdderDynamicFunction:     pass
class SummerDynamicFunction:    pass

# A DynamicFunction is a function of time (specified by an integer time-step
# number) that works by first updating some internal simulation state
# information as necessary to move the simulation forwards or backwards in
# time as needed, in order to be able to evaluate the function.  This base
# class is an abstract class, and cannot itself be instantiated directly.

class BaseDynamicFunction(metaclass=ABCMeta):

        # When initializing, can optionally provide an actual function
        # that will be called to implement our evaluateWith() method.

    def __init__(inst, function:Callable=None):
        inst._function = function

    def __call__(inst, timestep:int=None, *args, **kwargs):

        logger.debug("BaseDynamicFunction.__call__(): Evaluating dynamic function %s at timestep %s..."
                     % (str(inst), str(timestep)))
        
        if timestep != None:
            inst.evolveTo(timestep)
            
        return inst.evaluator(*args, **kwargs)

    def evaluator(inst, *args, **kwargs):

        logger.debug("BaseDynamicFunction.evaluator(): Evaluating dynamic function %s with arguments %s %s..." % (str(inst), str(args), str(kwargs)))
        
##        if len(args) == 0 and len(kwargs) == 0:
##            return inst         # No arguments provided: Leave the function unevaluated.
##        else:
        return inst.evaluateWith(*args, **kwargs)     # Needs further processing.

    def __neg__(inst):
        return NegatorDynamicFunction(inst)

    def __add__(inst, other:Callable[[int],Any]):
        return AdderDynamicFunction(inst,other)

    # Subclasses must define the evolveTo() method to define
    # how they accomplish evolving their state to the given
    # time point.  This base class does not define this
    # method, so it cannot be directly instantiated.

    @abstractmethod
    def evolveTo(inst, timestep:int): pass

    # Subclasses can override the evaluateWith() method to define
    # how they will evaluate the function if some arguments are
    # provided. At least one of args and kwargs must be non-empty.

    def evaluateWith(inst, *args, **kwargs):
        if inst._function != Null:
            inst._function(*args, **kwargs)

# A special DynamicFunction that just always returns Fixed(0).

class NullDynamicFunction(BaseDynamicFunction):
    def evolveTo(inst, timestep:int): pass
    def evaluateWith(inst, *args, **kwargs):
        return Fixed(0)

nullDynamicFunction = NullDynamicFunction()

# Given a DynamicFunction, constructs another one whose value is the
# unary negation of it.
            
class NegatorDynamicFunction(BaseDynamicFunction):

    def __init__(inst, f:BaseDynamicFunction):
        inst._internalFunction = f

    def evolveTo(inst, timestep:int):

        logger.debug("NegatorDynamicFunction.evolveTo(): Evolving internal dynamic function %s to timestep %d..." %
                     (str(inst._internalFunction), timestep))
        
        inst._internalFunction.evolveTo(timestep)

    def evaluateWith(inst, *args, **kwargs):
        
        logger.debug("NegatorDynamicFunction.evaluateWith(): Evaluating negator on internal function %s with arguments: %s %s" %
                     (str(inst._internalFunction), str(args), str(kwargs)))
        
        return -inst._internalFunction(*args, **kwargs)

# Given two DynamicFunctions, constructs another one whose value is
# the sum of those two.

class AdderDynamicFunction(BaseDynamicFunction):

    def __init__(inst, f1:BaseDynamicFunction, f2:BaseDynamicFunction):
        inst._augend = f1
        inst._addend = f2

    def evolveTo(inst, timestep:int):
        inst._augend.evolveTo(timestep)
        inst._addend.evolveTo(timestep)

    def evaluateWith(inst, *args, **kwargs):
        augend = inst._augend.evaluateWith(*args, **kwargs)
        addend = inst._addend.evaluateWith(*args, **kwargs)
        return augend + addend

# Given a list of DynamicFunction objects, constructs a new one whose
# value is the sum of the values of those objects.

class SummerDynamicFunction(BaseDynamicFunction):

    def __init__(inst, terms:Iterable[BaseDynamicFunction]):
        inst._terms = terms

    def evolveTo(inst, timestep:int):
        
        logger.debug("SummerDynamicFunction.evolveTo(): Evolving terms to timestep %d..." % timestep)
        
        for term in inst._terms:
            term.evolveTo(timestep)

    def evaluateWith(inst, *args, **kwargs):

        logger.debug("SummerDynamicFunction.evaluateWith(): Evaluating summer with arguments: %s %s" %
                     (str(args), str(kwargs)))
        
        if len(inst._terms) == 0:
            return Fixed(0)
        cumSum = inst._terms[0].evaluateWith(*args, **kwargs)
        for term in inst._terms[1:]:
            cumSum = cumSum + term.evaluateWith(*args, **kwargs)
        return cumSum

