from typing     import Any,Callable,Iterable
from functools  import partial
from inspect    import getargspec

__all__ = ['FunctionNotDefinedException',
           'TooManyArgumentsException',
           'UnknownArgumentsException',
           'PartiallyEvaluatableFunction']

class FunctionNotDefinedException(Exception): pass
    # At final-evaluation time, the actual function was still not defined.

class TooManyArgumentsException(Exception): pass
    # Too many actual arguments were supplied to a partially-evaluatable function.

class UnknownArgumentsException(Exception): pass
    # A keyword argument with an unexpected name was supplied to a partially-evaluatable function.

class PartiallyEvaluatableFunction():   # Is callable().

    # PartiallyEvaluatableFunction(<name>, <func>)
    #
    #       Create a new partially-evaluatable function.  You may
    #       optionally supply a name, a list of formal argument
    #       names, and an underlying function to base this
    #       entity on.  If the list of formal argument names is
    #       not supplied, it is inferred from the function's
    #       parameter list, but ignoring *varargs or **kwargs
    #       parameters or any default value specifiers.
    
    def __init__(inst, name:str='f', argList:Iterable[str]=None, function:Callable=None):

        inst._name = name

        if argList == None:
            argList = getargspec(function).args
            
        inst._argList = list(argList)

        inst._origArgList = inst._argList           # Original argument list to this function.
        inst._argDefs = dict()                      # Dictionary of argument values defined so far (none initially).

        inst._internalFunc = function

    @property
    def argList(inst):
        return inst._argList

    @property
    def function(inst):
        return inst._internalFunc

    @function.setter
    def function(inst, newFunc:Callable=None):
        inst._internalFunc = newFunc

    # If you call a partially-evaluatable function while only supplying
    # some of its arguments, then you get back a new partially-evaluatable
    # function object representing the partial evaluation of the original
    # function with only those arguments specified.  If you supply all of
    # its arguments, you get back its value.

    def __call__(inst, *args, **kwargs) -> Any:

        if inst._internalFunc == None:
            raise FunctionNotDefinedException("Can't call a PartiallyEvaluatableFunction before defining its function!")

        totArgs = len(args) + len(kwargs)

            # Make sure user didn't supply us with too many actual arguments.

        if len(args) + len(kwargs) > len(inst._argList):
            raise TooManyArgumentsException("Tried to call %s with too many (%d) arguments!" % (str(inst), totArgs))

        argDefs = dict(inst._argDefs)   # List of pairs (arg, val) giving initial argument values.

            # Remember the actual argument values supplied for future reference.

        argIndex = 0
        for argVal in args:
            argName = inst._argList[argIndex]
            argDefs[argName] = argVal
            argIndex = argIndex + 1

            # OK, let's get our remaining list of formal argument names.
            
        nArgs = len(args)
        remArgs = inst._argList[nArgs:]

            # Final argument list consists of remaining arguments
            # that don't appear in the supplied keyword arguments.
            # Shouln't there be an easier way to do this???

        finArgs = []
        remkwargs = dict(kwargs)
        for arg in remArgs:
            if not arg in remkwargs:
                finArgs.append(arg)
            else:
                argDefs[arg] = remkwargs[arg]
                del remkwargs[arg]             # We used that keyword already; delete it!

            # If there are any extra keyword arguments left, they don't belong!

        if len(remkwargs) > 0:
            raise UnknownArgumentsException("Unknown keyword arguments %s were supplied to PartiallyEvaluatableFunction %s" %
                                            (str(kwargs), str(inst)))

        if len(finArgs) == 0:   # All arguments were supplied!!
            
                # Go ahead and evaluate our internal function.
            return inst._internalFunc(*args, **kwargs)
            
        # Not all arguments were supplied - create a new partially
        # evaluatable function.

        result = PartiallyEvaluatableFunction(inst._name, finArgs,
                                              partial(inst._internalFunc,
                                                      *args, **kwargs))

            # For documentation purposes, annotate the result with
            # the original argument list, and the argument values
            # that have been defined so far.

        result._origArgList = inst._origArgList
        result._argDefs     = argDefs

        return result
    
    def __str__(inst) -> str:
        string = inst._name + '('
        if len(inst._argList) > 0:
            string += inst._argList[0]
            for arg in inst._argList[1:]:
                string += ',' + arg
        string += ')'
        if len(inst._origArgList) > len(inst._argList):
            string += ' = '+ inst._name + '(' + inst._origArgList[0]
            if inst._origArgList[0] in inst._argDefs:
                string += '=' + str(inst._argDefs[inst._origArgList[0]])
            for arg in inst._origArgList[1:]:
                string += ', ' + arg
                if arg in inst._argDefs:
                    string += '=' + str(inst._argDefs[arg])
            string += ')'
            
        return string

