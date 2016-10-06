from .unaryDifferentiableFunction import UnaryDifferentiableFunction

#-- A class for general univariate quadratic functions, of the form:
#
#       f(x) = c2*x^2 + c1*x + c0

class QuadraticFunction(UnaryDifferentiableFunction):

    # Initializer.  Given coefficients (c2, c1, c0), creates a new
    #   quadratic function with those coefficients.  The default
    #   coefficient values are just (1,0,0), which gives f(x)=x**2.

    def __init__(inst,
                 name:str=None, argName:str=None,
                 c2=None, c1=None, c0=None):

            # Apply default values for coefficients if needed.

        if c2 == None:  c2 = 1
        if c1 == None:  c1 = 0
        if c0 == None:  c0 = 0

            # Construct our function.

        function = lambda x:  (c2 * x**2) + (c1 * x) + c0

            # Construct our derivative.

        derivative = lambda x:  2*c2*x + c1

            # Do generic initialization for unary differentiable
            # functions.

        UnaryDifferentiableFunction.__init__(inst, name=name,
                                             argName=argName,
                                             function=function,
                                             derivative=derivative)

            # Remember coefficients of our terms for later reference.

        inst._c2 = c2    # Coefficient of 2nd-order (quadratic) term.
        inst._c1 = c1    # Coefficient of 1st-order (linear) term.
        inst._c0 = c0    # Coefficient of 0th-order (constant) term.

        
# A SimpleQuadraticFunction is a special case of a QuadraticFunction
# where the first-order and zeroth-order terms are zero.  It is thus
# of the form:
#
#       f(x) = c * (x ** 2)
#
# where c is a constant.

class SimpleQuadraticFunction(QuadraticFunction):

    def __init__(inst, name:str=None, argName:str=None, c=None):

        #print("SQF name=%s argName=%s c=%s" % (name, argName, str(c)))
        
        QuadraticFunction.__init__(inst, name, argName, c)
            # We could optimize this implementation here
            # replacing ._function and ._partials with
            # simpler versions of them.
