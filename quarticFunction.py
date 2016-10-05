from unaryDifferentiableFunction import UnaryDifferentiableFunction

#-- A class for general univariate quartic functions, of the form:
#
#       f(x) = c4*x^4 + x3*x^3 + c2*x^2 + c1*x + c0

class QuarticFunction(UnaryDifferentiableFunction):

    # Initializer.  Given coefficients (c4, c3, c2, c1, c0), creates a new
    #   quartic function with those coefficients.  The default
    #   coefficient values are just (1,0,0,0,0), which gives f(x)=x**4.

    def __init__(inst,
                 name:str=None, argName:str=None,
                 c4=None, c3=None, c2=None, c1=None, c0=None):

            # Apply default values for coefficients if needed.

        if c4 == None:  c4 = 1
        if c3 == None:  c3 = 1
        if c2 == None:  c2 = 1
        if c1 == None:  c1 = 0
        if c0 == None:  c0 = 0

            # Construct our function.

        function = lambda x:  (c4 * x**4) + (c3 * x**3) + (c2 * x**2) + (c1 * x) + c0

            # Construct our derivative.

        derivative = lambda x:  (4*c4 * x**3) + (3*c3 * x**2) + 2*c2*x + c1

            # Do generic initialization for unary differentiable
            # functions.

        UnaryDifferentiableFunction.__init__(inst, name=name,
                                             argName=argName,
                                             function=function,
                                             derivative=derivative)

            # Remember coefficients of our terms for later reference.

        inst._c4 = c4    # Coefficient of 4th-order (quartic) term.
        inst._c3 = c3    # Coefficient of 3rd-order (cubic) term.
        inst._c2 = c2    # Coefficient of 2nd-order (quadratic) term.
        inst._c1 = c1    # Coefficient of 1st-order (linear) term.
        inst._c0 = c0    # Coefficient of 0th-order (constant) term.

        
