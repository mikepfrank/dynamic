import math         # Defines ceil, floor, etc.
import numbers      # Defines the Rational abstract class.
import operator     # Module defining standard arithmetic operators
import fractions    # Includes the Fraction class.

__all__ = ['Fixed']

#-- Class for fixed-point numbers with a specific fractional quantum.
#   NOTE: To simplify code, all instances of Fixed have the same quantum!

class Fixed(numbers.Rational):

    #-- Class data members.
    #       Fixed.denominator - The denominator D of the quantum 1/D.

    _denominator = int(1e9)      # Define numbers to 1 billionth of a unit.

    #-- Instance data members.
    #       inst._numerator - The numerator N of the fixed value N/D.

    def __init__(inst, value=0, denom=None):

        #-- If no denominator is specified, then take the value to be
        #   the full numeric value.  Else, take the value to be a numerator.

        if denom==None:     # No denomiator provided; just copy the value.

            #-- Special case if the value we're copying is already a Fixed:
            #   Just copy its numerator.  This is needed to prevent infinite
            #   recursion...
            if isinstance(value, Fixed):
                inst._numerator = value._numerator    
            else:
                #-- Calculate the fixed-point number's numerator.
                inst._numerator = round(value * Fixed._denominator)

        else:   # Denominator provided, treat pair as a fraction.
            frac = fractions.Fraction(value, denom)
            inst.__init__(frac, None)

    def __repr__(self):     # return faithful string representation
        return('Fixed(%d,%d)'%(self._numerator, Fixed._denominator))

    def __str__(self):      # return simple string representation
        frac = fractions.Fraction(self._numerator, Fixed._denominator)
        return str(frac)

    def __format__(self, fmtSpec):
        frac = fractions.Fraction(self._numerator, Fixed._denominator)
        return frac.__format__(fmtSpec)

    #-- Subclasses of numbers.Rational have to define the methods:
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
    
