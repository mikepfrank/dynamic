from typing     import Callable,Iterable
from inspect    import getargspec

# Base class from which to derive subclasses for particular types
# of differentiable functions (of any number of variables).

__all__ = ['BaseDifferentiableFunction']

class BaseDifferentiableFunction:

    # Instance public properties:
    #
    #   .argNames:list - Read-only property that is a list of
    #           formal argument names.
    #
    # Instance private data members:
    #
    #   ._argNames:list - list of argument names
    #   ._argIndex:dict - map from argument names to their indices
    #   ._function:Callable - lambda from argument values to function value
    #   ._partials:Iterable[Callable] - list of partial-derivative lambdas

    # Instance private methods:
    #
    #   ._addArg(<arg>) - Add an argument name <arg> to our list of arguments.
    #
    #   ._setArgs(<arg1>[, <argi>]*) - Set the argument list of this
    #       function to the given string(s).

    # Instance special methods:
    #
    #   inst.__init__(<argnames>, [<function>,] [<partials>]) -
    #
    #       Instance initializer.

    def __init__(inst, argNames:Iterable[str]=None,
                 function:Callable=None,
                 partials:Iterable[Callable]=[]):

        if function != None:
            inst.function = function
            if argNames == None
                argNames = getargspec(function).args

        inst._setArgs(*argNames)

        if partials != None:  inst.partials = partials

    # Function application operator.
    #   For applying a BaseDifferentiableFunction instance to a
    #   list of arguments.

    def __call__(this, *argVals):
        return this.function(*argVals)

    # Returns the partial derivative of this differentiable
    # function with respect to its <argumentIndex>th argument.
    # Our return type is Callable.  The arguments to this
    # callable should be the values of the function's arguments,
    # and the return value is the value of the partial derivative
    # evaluated at that point.

    def partialDerivWRT(argumentIndex:int):
        return this._partials[argumentIndex]

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

    #|==========================================================================
    #|
    #|      Instance public property defintions.    [class definition section]
    #|
    #|--------------------------------------------------------------------------

    @property
    def argNames(this):
        return this._argNames

    # Public methods that derived classes should define:
    
