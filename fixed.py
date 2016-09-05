
    # ***** THIS IS THE NEXT FILE TO CLEAN UP *****

import math         # Defines ceil, floor, etc.
import numbers      # Defines the Rational abstract class.
import operator     # Module defining standard arithmetic operators
import fractions    # Includes the Fraction class.

import logmaster
from logmaster import ErrorException

_logger = logmaster.getLogger(logmaster.sysName + '.fixed')

__all__ = [
    'Fixed',
    'FixedError',           # Exception classes.
    'InitialValueError',
    'NoInitialValueError'
    ]

# Exception classes.

    # Alternatively to the below, we could subclass logmaster.LoggedException
    # and then mixin ErrorException.  This would allow us to do module-specific
    # logged exceptions at other levels as well (info, warning, critical, etc.)
    # So far we haven't needed that capability, though.

class FixedError(ErrorException):       # Error in this fixed-point module.
    """This class is for errors detected in 'fixed', the fixed-point
       arithmetic module."""
    def __init__(inst, msg:str=None):
        ErrorException.__init__(msg=msg, logger=_logger)

class InitialValueError(FixedError):
    """An initial value that was passed as an argument to a
       constructor in this module ('fixed') was unacceptable."""
    pass

class NoInitialValueError(InitialValueError):
    """No initial value or an initial value of None was provided to a
        constructor, but a value other than None was required."""
    pass

#-- Class for fixed-point numbers with a specific fractional quantum.
#
#       NOTE: To simplify user code, all instances of Fixed are required
#   to have the same quantum! This way the user does not have to specify
#   the quantum when creating fixed-point number instances.
#
#       It may be worth considering whether it would be useful to
#   have a base class that is abstract (leaves the denominator
#   unspecified), and then have various subclasses of it that give
#   different default values to the quantum, or even allow the user
#   to specify the quantum during some class-initialization step.
#   This way, fixed-point numbers of different precision could be
#   used within one application.  We're not yet exploring this,
#   though.

class Fixed(numbers.Rational):
    
    """Fixed is a rational-number class (an implementation of the
       abstract base class numbers.Rational) in which all number
       instances have a fixed precision, in that they are all
       integer multiples of a fixed quantum 1/D, where D could be
       any fixed positive integer.  Currently D=1e9 (1 billion),
       so all Fixed numbers are defined to a precision of 1e-9
       (0.000000001), or nine decimal places."""

    #-- Private class attributes (static data members).
    #
    #       Fixed._denominator:Integer - The denominator D of the quantum 1/D.
    #           (Please don't change this after the class is initialized.)

    _denominator = int(1e9)      # Define all numbers to 1 billionth of a unit.

    #-- Private instance data members.
    #       inst._numerator:Integer - The numerator N of the fixed value N/D.

    def __init__(inst, value=None, denom=None):
        
        """This initializer for instances of class Fixed may be used
           in any of several ways:

                newFixed = Fixed(value=<oldFixed>:Fixed)

                    If given one argument which is itself also an
                    instance of Fixed, the initializer simply copies
                    the value of the old object into the new one.

                newFixed = Fixed(value=<number>:Number)

                    Any other numeric argument, by itself, will be
                    used as the initial value of the new fixed-point
                    number, but rounding may occur here, if the
                    argument is not an exact integer multiple of our
                    quantum 1/D (D=1e9).

                newFixed = Fixed(value=<numerator>:Rational,
                                 denom=<denominator>:Rational)

                    If two numbers are provided, Fixed(N,D), both
                    rational, then they are treated as the numerator
                    and denominator of a fraction, and the value of
                    this fraction (rounded as needed), is taken as
                    the initial value of the new Fixed number.  So,
                    for example, Fixed(2,3) = 0.666666667 (exactly).
                                                                             """

            #------------------------------------------------------
            # Error checking: If a non-None value is not provided,
            # throw an ErrorException. (What is the user thinking?)

        if value is None:
            raise NoInitialValueError("Fixed.__init__(): Creating a Fixed "
                                      "with no initial value is not supported.")

            #------------------------------------------------------
            # If no denominator is specified, then take the value
            # to be the full numeric value of the new fixed-point
            # number. Else, take the value to be a numerator of a
            # fraction. (Numerator & denominator must be rational.)

        if denom==None:     # No denominator provided; just copy the value.

                #---------------------------------------------------
                # Here, we handle a special case which arises if the
                # value we're copying is already a Fixed:  We just
                # copy its numerator.  This is needed to prevent an
                # infinite recursion which would otherwise occur...

            if isinstance(value, Fixed):
                inst._numerator = value._numerator      # Copy numerator.

                #----------------------------------------------------
                # For arbitrary numeric arguments, find our numerator
                # by multiplying by the fixed denominator integer D
                # and then rounding to the nearest integer value. So,
                # for example, 5/3 ends up getting represented as the
                # fraction 1,666,666,667 / 1,000,000,000.
                
            else:
                # Possible error-checking we could do here: Make sure
                # that the value provided is a numeric type.
                inst._numerator = round(value * Fixed._denominator)
                
            #__/ End if isinstance(value, Fixed) ... else ...

            #------------------------------------------------------
            # In this case, a non-None value of the denom argument
            # was provided, so interpret value/denom as a fraction.

        else:
            
            # First, find the implied initial value as a fraction.
            # Possible error-checking we could do here: Check to make
            # sure that value and denom are both rationals.
            
            frac = fractions.Fraction(value, denom)

            # Next, initialize our value to that of the fraction that
            # just put together.
            
            inst.__init__(frac)   # Recursively call this initializer.

        #__/ End if denom==None ... else ...

        # ***** CONTINUE CLEANING UP BELOW HERE *****

    def __repr__(self):     # return faithful string representation
        return('Fixed(%d,%d)'%(self._numerator, Fixed._denominator))

    def __str__(self):      # return simple string representation
        frac = fractions.Fraction(self._numerator, Fixed._denominator)
        return str(frac)

    def __format__(self, fmtSpec):
        frac = fractions.Fraction(self._numerator, Fixed._denominator)
        return frac.__format__(fmtSpec)

    #-- Subclasses of numbers.Rational have to define all these methods:
    #
    #       __abs__, __add__, __ceil__, __eq__, __floor__, __floordiv__,
    #       __le__, __lt__, __mod__, __mul__, __neg__, __pos__, __pow__,
    #       __radd__, __rfloordiv__, __rmod__, __rmul__, __round__,
    #       __rpow__, __rtruediv__, __truediv__, __trunc__

    def __abs__(self):
        result = Fixed(self)    # Make a copy of this fixed-point number.
        result._numerator = abs(result._numerator)      # Absolute-value it.
        return result

    def __add__(x,y):
        result = Fixed(x)
        _logger.debug("Fixed.__add__(): Attempting to convert addend %s to Fixed..." % y)
        yfixed = Fixed(y)
        result._numerator = result._numerator + yfixed._numerator
        return result

    def __ceil__(self):
        frac = fractions.Fraction(self._numerator, Fixed._denominator)
        result = Fixed(math.ceil(frac))
        return result

    def __eq__(x, y):
        xfixed = Fixed(x)
        yfixed = Fixed(y)
        return xfixed._numerator == yfixed._numerator        

    def __floor__(self):
        frac = fractions.Fraction(self._numerator, Fixed._denominator)
        result = Fixed(math.floor(frac))
        return result

    def __floordiv__(x, y):
        xfrac = fractions.Fraction(x._numerator, Fixed._denominator)
        result = Fixed(xfrac // y)
        return result

    def __le__(x, y):
        xfixed = Fixed(x)
        yfixed = Fixed(y)
        return xfixed._numerator <= yfixed._numerator        

    def __lt__(x, y):
        xfixed = Fixed(x)
        yfixed = Fixed(y)
        return xfixed._numerator < yfixed._numerator                

    def __mod__(x, y):
        xfrac = fractions.Fraction(x._numerator, Fixed._denominator)
        result = Fixed(xfrac % y)
        return result

    def __mul__(x, y):
        xfrac = fractions.Fraction(x._numerator, Fixed._denominator)
        result = Fixed(xfrac * y)
        return result

    def __neg__(self):
        result = Fixed(self)
        result._numerator = -result._numerator
        return result

    def __pos__(self):
        result = Fixed(self)
        return result

    def __pow__(x, y):
        xfrac = fractions.Fraction(x._numerator, Fixed._denominator)
        result = Fixed(xfrac ** y)
        return result

    def __radd__(x, y):
        xfrac = fractions.Fraction(x._numerator, Fixed._denominator)
        result = Fixed(xfrac + y)
        return result

    def __rfloordiv__(x, y):
        xfrac = fractions.Fraction(x._numerator, Fixed._denominator)
        result = Fixed(y // xfrac)
        return result

    def __rmod__(x, y):
        xfrac = fractions.Fraction(x._numerator, Fixed._denominator)
        result = Fixed(y % xfrac)
        return result

    def __rmul__(x, y):
        xfrac = fractions.Fraction(x._numerator, Fixed._denominator)
        result = Fixed(xfrac * y)
        return result

    def __round__(self, precision=None):
        frac = fractions.Fraction(self._numerator, Fixed._denominator)
        return Fixed(round(frac, precision))

    def __rpow__(x, y, mod=None):
        xfrac = fractions.Fraction(x._numerator, Fixed._denominator)
        result = Fixed(y ** xfrac)
        return result

    def __rtruediv__(x, y):
        xfrac = fractions.Fraction(x._numerator, Fixed._denominator)
        result = Fixed(y / xfrac)
        return result

    def __truediv__(x, y):
        xfrac = fractions.Fraction(x._numerator, Fixed._denominator)
        result = Fixed(xfrac / y)
        return result

    def __trunc__(self):
        frac = fractions.Fraction(self._numerator, Fixed._denominator)
        return Fixed(math.trunc(frac))
    
    #-- Subclasses of numbers.Rational have to define the properties:
    #       numerator, denominator

    @property
    def numerator(self):
        #-- Go through Fraction to reduce to lowest terms.
        frac = fractions.Fraction(self._numerator, Fixed._denominator)
        return frac.numerator

    @property
    def denominator(self):
        #-- Go through Fraction to reduce to lowest terms.
        frac = fractions.Fraction(self._numerator, Fixed._denominator)
        return frac.denominator

    #-- New public properties:
    #       .quantum - The quantum of the fixed number system, as a Fraction.

    @property
    def quantum(self):
        return fractions.Fraction(1, Fixed._denominator)
    
