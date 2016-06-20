from baseDifferentiableFunction import BaseDifferentiableFunction

__all__ = ['UnaryDifferentiableFunction']

class UnaryDifferentiableFunction(BaseDifferentiableFunction):
    
    def __init__(inst):
        
        inst.BaseDifferentiableFunction.__init__(inst)
        
        inst.setArgs('x')   # Our single argument is called 'x'.
        
