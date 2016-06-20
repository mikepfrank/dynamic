# Base class from which to derive subclasses for particular types
# of differentiable functions (of any number of variables).

__all__ = ['BaseDifferentiableFunction']

class BaseDifferentiableFunction:

    # Data members:
    #   .argNames - list of argument names
    #   .argIndex - map from argument names to their indices
    #   .function - lambda from list of argument values to function value
    #   .partials - tuple of partial-derivative lambdas

    def __init__(inst):
        inst.argNames = []

    # .addArg(argName) - Adds an argument named <argName> to this
    #   function's argument list.

    def addArg(this, argName):

            # The length of the existing list of arguments
            # is the index of the new argument (0-based).
        
        pos = len(this.argNames)

            # Add the argument's name to our list of argument names.
        
        this.argNames.append(argName)

            # Remember the index value (position) of this argument in
            # the list of arguments.  Arguments are indexed from 0.
        
        this.argIndex[argName] = pos

    # .setArgs(<arg1>[, <argi>]*) - Set the argument list of this
    #   function to the given string(s).

    def setArgs(this, *names):
        this.argNames = []
        foreach name in names:
            this.addArg(name)    

    # Function application operator.
    #   For applying a BaseDifferentiableFunction instance to a
    #   list of arguments.

    def __call__(this, *argVals):
        return this.function.__call__(*argVals)


    # Public methods that derived classes should define:
    
