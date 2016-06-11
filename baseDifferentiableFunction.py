
__all__ = ['BaseDifferentiableFunction']

class BaseDifferentiableFunction:

    # Data members:
    #   .argNames - list of argument names
    #   .argIndex - map from argument names to indices
    #   .function - lambda from list of argument values to function value
    #   .partials - tuple of partial-derivative lambdas

    def __init__(inst):
        inst.argNames = []


        # Add an argument named <argName> to this function's argument list.

    def addArg(this, argName):

            # The length of the list is the index of the new argument.
        
        pos = len(this.nargs)

            # Add the argument's name to our list of argument names.
        
        this.argNames.append(argName)

            # Remember the index value (position) of this argument in
            # the list of arguments.  Arguments are indexed from 0.
        
        this.argIndex[argName] = pos

    def evaluate(this, argVals):
        return this.function(argVals)

    def setArglist(this, names):
        foreach name in names:
            this.addArg(name)

    # Public methods that derived classes should define:
    
