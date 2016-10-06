# ternaryDifferentiableFunction.py

from typing import Callable

from .differentiableFunction import BaseDifferentiableFunction

__all__ = ['TernaryDifferentiableFunction']

class TernaryDifferentiableFunction(BaseDifferentiableFunction):

    def __init__(me, name:str=None,
                 argName1:str=None, argName2:str=None, argName3:str=None,
                 function:Callable=None,
                 deriv1:Callable=None, deriv2:Callable=None, deriv3:Callable=None):

        if function is None:
            
            if name is None:        name = 'f'
            if argName1 is None:    argName1 = 'x'
            if argName2 is None:    argName2 = 'y'
            if argName3 is None:    argName3 = 'z'

        argNames = [argName1, argName2, argName3] if argName1 is not None and argName2 is not None and argName3 is not None else None
        partials = [deriv1, deriv2, deriv3] if deriv1 is not None and deriv2 is not None and deriv3 is not None else None

        BaseDifferentiableFunction.__init__(me, name, argNames, function, partials)

    @property
    def argName1(me): return me.argNames[0]

    @argName1.setter
    def argName1(me, newName:str): me.argNames[0] = newName

    @property
    def argName2(me): return me.argNames[1]

    @argName2.setter
    def argName2(me, newName:str): me.argNames[1] = newName

    @property
    def argName3(me): return me.argNames[2]

    @argName3.setter
    def argName3(me, newName:str): me.argNames[2] = newName

    @property
    def deriv1(me): return me.partials[0]

    @property
    def deriv2(me): return me.partials[1]

    @property
    def deriv3(me): return me.partials[2]
    
