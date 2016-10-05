import logmaster; from logmaster import *

from quadraticFunction import QuadraticFunction

_logger = getLogger(sysName + '.functions')

class DynamicBiasFunction(QuadraticFunction):

    def __init__(inst, biasval, stiffness):

        # Set coefficients of quadratic function terms accordingly per
        #           0.5k(x-b)^2  =  0.5kx^2 -kbx + 0.5kb^2.

        c2  =    0.5 * stiffness
        c1  =  -       stiffness * biasval
        c0  =    0.5 * stiffness * biasval**2

        QuadraticFunction.__init__(inst, name='B', c2=c2, c1=c1, c0=c0)

        # Remember the bias value and stiffness for future reference.

        inst.biasval   = biasval
        inst.stiffness = stiffness

