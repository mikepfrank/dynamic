from unaryDifferentiableFunction import UnaryDifferentiableFunction

#-- A class for general univariate quadratic functions, of the form:
#
#       f(x) = c2*x^2 + c1*x + c0

class QuadraticFunction(UnaryDifferentiableFunction):

    # Initializer.  Given coefficients (c2, c1, c0), creates a new
    #   quadratic function with those coefficients.

    def __init__(inst, c2, c1, c0):

        UnaryDifferentiableFunction.__init__(inst)

        #-- Remember coefficients of our terms.

        inst.c2 = c2    # Coefficient of 2nd-order (quadratic) term.
        inst.c1 = c1    # Coefficient of 1st-order (linear) term.
        inst.c0 = c0    # Coefficient of 0th-order (constant) term.

        #-- Construct and remember our function.

        inst.function = lambda x:  (c2 * x**2) + (c1 * x) + c0

        #-- Construct and remember our derivative.

        inst.partials = [lambda x:  2*c2*x + c1]
        
