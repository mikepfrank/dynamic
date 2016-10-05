from numbers import Real

import logmaster; from logmaster import *

from quarticFunction import QuarticFunction

_logger = getLogger(sysName + '.functions')

class DoubleWellFunction(QuarticFunction):

    def __init__(inst, bottom1:Real, bottom2:Real, stiffness:Real):

        # Set coefficients of quartic function terms accordingly per
        #           0.5k(x-b1)^2(x-b2)^2  

        c4  =    0.5 * stiffness
        c3  =  -       stiffness * (bottom1 + bottom2)
        c2  =          stiffness * (0.5 * ((bottom1 ** 2) + (bottom2 ** 2))
                                    + 2 * (bottom1 * bottom2))
        c1  =  -       stiffness * (bottom1 * (bottom2 ** 2) + (bottom1 ** 2) * bottom2)
        c0  =    0.5 * stiffness * (bottom1**2 + bottom2**2)

        QuarticFunction.__init__(inst, name='D', c4=c4, c3=c3, c2=c2, c1=c1, c0=c0)

        # Remember the bottom values and stiffness for future reference.

        inst.bottom1 = bottom1
        inst.bottom2 = bottom2
        inst.stiffness = stiffness

