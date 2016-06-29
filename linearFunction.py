from unaryDifferentiableFunction import UnaryDifferentiableFunction

class LinearFunction(UnaryDifferentiableFunction):

    def __init__(inst, name:str=None, argName:str=None,
                 c1=None, c0=None):

        if c1 == None: c1 = 1
        if c0 == None: c0 = 0

        function = lambda x: (c1*x) + c0

        derivative = lambda x:  c1

        UnaryDifferentiableFunction.__init__(inst, name=name,
                                             argName=argName,
                                             function=function,
                                             derivative=derivative)

        inst._c1 = c1
        inst._c0 = c0

class ProportionalFunction(LinearFunction):

    def __init__(inst, name:str=None, argName:str=None, c=None):

        LinearFunction.__init__(inst, name, argName, c)

        
