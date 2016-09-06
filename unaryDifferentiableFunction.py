from typing import Callable

from differentiableFunction import BaseDifferentiableFunction

__all__ = ['UnaryDifferentiableFunction']

class UnaryDifferentiableFunction(BaseDifferentiableFunction):
    
    def __init__(inst, name:str=None, argName:str=None,
                 function:Callable=None, derivative:Callable=None):

        if name == None and function == None:    name = 'f'

            # If no argument name or function was provided, then
            # just use default name 'x' for the function argument.
            # This can also be changed later, if desired, using
            # the inst.argName property setter (defined below).

        if argName == None and function == None:    argName = 'x'

            # Turn the argument name and derivative, if known,
            # into a singleton argument name list and partial
            # derivative list, respectively.

        argNames = [argName] if argName != None else None
        partials = [derivative] if derivative != None else None

            # Do generic initialization for differentiable functions.
        
        BaseDifferentiableFunction.__init__(inst, name, argNames,
                                            function, partials)
        
    @property
    def argName(this):
        return this.argNames[0]

    @argName.setter
    def argName(this, newName:str):
        this.argNames[0] = newName
        
    @property
    def derivative(this):
        return this.partials[0]
