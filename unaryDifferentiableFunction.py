from baseDifferentiableFunction import BaseDifferentiableFunction

__all__ = ['UnaryDifferentiableFunction']

class UnaryDifferentiableFunction(BaseDifferentiableFunction):
    
    def __init__(inst):
        
        BaseDifferentiableFunction.__init__(inst)
        
        inst._setArgs('x')   # Our single argument is called 'x' by default.
            # Users can change this using the property setter method,
            # inst.argName = <newName>, defined below.

    @property
    def argName(this):
        return this.argNames[0]

    @argName.setter(this, newName:str):
        this.argNames[0] = newName
        
        
