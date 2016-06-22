from typing import Any,Callable,Iterable

# Base class from which to derive subclasses for particular types
# of differentiable functions (of any number of variables).

__all__ = ['BaseDifferentiableFunction']

class BaseDifferentiableFunction:

    # Public properties:
    #
    #
    #
    # Private data members:
    #
    #   ._argNames - list of argument names
    #   ._argIndex - map from argument names to their indices
    #   ._function - lambda from list of argument values to function value
    #   ._partials - list of partial-derivative lambdas

    # Private methods:
    #
    #   ._addArg(<arg>) - Add an argument name <arg> to our list of arguments.
    #
    #   ._setArgs(<arg1>[, <argi>]*) - Set the argument list of this
    #       function to the given string(s).

    def __init__(inst, argNames:Iterable[str]=[],
                 function:Callable[[Iterable],Any]=None,
                 partials:Iterable[Callable[[Iterable],Any]]=[]):

        inst._setArgs(*argNames)

        if function != None:  inst.function = function

        if partials != None:  inst.partials = partials

    # Function application operator.
    #   For applying a BaseDifferentiableFunction instance to a
    #   list of arguments.

    def __call__(this, *argVals):
        return this.function(*argVals)

    # ._addArg(argName) - Adds an argument named <argName> to this
    #   function's argument list.

    def _addArg(this, argName):

            # The length of the existing list of arguments
            # is the index of the new argument (0-based).
        
        pos = len(this._argNames)

            # Add the argument's name to our list of argument names.
        
        this._argNames.append(argName)

            # Remember the index value (position) of this argument in
            # the list of arguments.  Arguments are indexed from 0.
        
        this._argIndex[argName] = pos

    # ._setArgs(<arg1>[, <argi>]*) - Set the argument list of this
    #       function to the given string(s).

    def _setArgs(this, *names):
        this._argNames = []
        this._argIndex = dict()
        for name in names:
            this._addArg(name)    


    # Public methods that derived classes should define:
    
