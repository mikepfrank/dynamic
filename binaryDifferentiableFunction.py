from typing import Callable

from differentiableFunction import BaseDifferentiableFunction

__all__ = ['BinaryDifferentiableFunction']

class BinaryDifferentiableFunction(BaseDifferentiableFunction):

    def __init__(inst, name:str=None, argName1:str=None, argName2:str=None,
                 function:Callable=None,
                 deriv1:Callable=None, deriv2:Callable=None):

        if function == None:
            
            if name == None:        name = 'f'
            if argName1 == None:    argName1 = 'x'
            if argName2 == None:    argName2 = 'y'

        argNames = [argName1, argName2] if argName1 != None and argName2 != None else None
        partials = [deriv1, deriv2] if deriv1 != None and deriv2 != None else None

        BaseDifferentiableFunction.__init__(inst, name, argNames, function, partials)

    @property
    def argName1(this):
        return this.argNames[0]

    @argName1.setter
    def argName1(this, newName:str):
        this.argNames[0] = newName
        
    @property
    def argName2(this):
        return this.argNames[1]

    @argName2.setter
    def argName2(this, newName:str):
        this.argNames[1] = newName

    @property
    def deriv1(this):
        return this.partials[0]

    @property
    def deriv2(this):
        return this.partials[1]
