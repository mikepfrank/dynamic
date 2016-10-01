from typing     import Callable,Iterable
from inspect    import getargspec

import logmaster; from logmaster import *

# Base class from which to derive subclasses for particular types
# of differentiable functions (of any number of variables).

__all__ = ['BaseDifferentiableFunction']

logger = getLogger(logmaster.sysName + '.functions')

class BaseDifferentiableFunction:

    # Instance public properties:
    #
    #   .name:str - Name of this function.  Used for display purposes.
    #                   NOTE: These names are not required or guaranteed
    #                   to be unique for different instances of a given
    #                   function.
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

    def __init__(inst, name:str=None,
                 argNames:Iterable[str]=None,
                 function:Callable=None,
                 partials:Iterable[Callable]=[]):

        inst.name = name

        # If the function was provided, remember it.
        # And if the function name and argument names
        # were not separately provided, get them by
        # inspecting the function.

        if function != None:
            
            inst.function = function

            # If the function was anonymous (a lambda), then
            # it has no true name, so don't bother using it
            # to extract a name.  Otherwise, use its name
            # if the user isn't overriding it.

            if function.__name__ != '<lambda>':
                if name == None:
                    name = function.__name__

            # Use the function's list of formal arguments
            # (other than *varargs or **kwargs arguments)
            # as our list of argument names, unless the
            # user is overriding it.

            if argNames == None:
                argNames = getargspec(function).args

        # If the name is still unset at this point,
        # default it to 'f' (for "function").

        if name == None:
            name = 'f'

        # If the list of argument names is still unset
        # at this point, default it to the empty list.
        
        if argNames == None:
            argNames = []
            
        inst._setArgs(*argNames)

        if partials != None:  inst._partials = partials

    # Function application operator.
    #   For applying a BaseDifferentiableFunction instance to a
    #   list of arguments.

    def __call__(this, *argVals):
        value = this.function(*argVals)

        if doDebug:
            logger.debug(("BaseDifferentiableFunction.__call__(): Evaluated " +
                           "%s (%s) on %s to get %s") %
                          (str(this), str(this.function), str(argVals), str(value)))

        return value

    # Returns the partial derivative of this differentiable
    # function with respect to its <argumentIndex>th argument.
    # Our return type is Callable.  The arguments to this
    # callable should be the values of the function's arguments,
    # and the return value is the value of the partial derivative
    # evaluated at that point.

    def partialDerivWRT(this, argumentIndex:int):
        try:
            return this._partials[argumentIndex]
        except IndexError as e:
            logger.exception(("BaseDifferentiableFunction.partialDerivWRT():  Attempted to " +
                              "take the partial derivative of %s with respect to its %d'th " +
                              "argument, but it only has %d arguments.") % (str(this),
                                                                            argumentIndex,
                                                                            len(this._partials)))
            raise e

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
    
