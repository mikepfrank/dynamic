from baseDifferentiableFunction import BaseDifferentiableFunction

__all__ = ['UnaryDifferentiableFunction']

class UnaryDifferentiableFunction(BaseDifferentiableFunction):
    
    def __init__(inst):
        
        BaseDifferentiableFunction.__init__(inst)
        
        inst._setArgs('x')   # Our single argument is called 'x' by default.
        
