#|==============================================================================
#|                          TOP OF FILE:    fixed.py
#|------------------------------------------------------------------------------
#|   The below module documentation string will be displayed by pydoc3.
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""
    FILE NAME:              fixed.py            [Python 3 module source file]

    MODULE NAME:            fixed

    SOFTWARE SYSTEM:        Dynamic         (simulator for dynamic networks)

    SOFTWARE COMPONENT:     Dynamic.fixed   (fixed-precision arithmetic package)


    MODULE DESCRIPTION:
    -------------------

        The fixed module provides a new numeric type defined by the
        class Fixed, a subclass of numbers.Rational.  Instances of
        Fixed represent fixed-point numbers; that is, they are all
        integer multiples of the same (fractional) quantum.
        Currently, the quantum must be of the form 1/D (where D is
        an integer), to ensure that 1.0 can be exactly represented.
        At present, the value of D is 1,000,000,000 (one billion);
        thus, elements of Fixed have a precision of 0.000,000,001
        (9 decimal places).

        The purpose of Fixed, within the Dynamic system, is to ensure
        that addition is bit-level reversible.  (Addition of floating-
        point numbers is not reversible, due to the fact that the sum
        may be rounded if the binary exponent increased.)


    BASIC MODULE USAGE:
    -------------------

        import fixed; from fixed import *

        a = Fixed(1/3)      # Rounded down to 0.333,333,333
        
        b = Fixed(2/3)      # Rounded up to 0.666,666,667

        c = a + b           # Adding Fixeds makes a Fixed.

        print(str(c))       # Outputs '1'


    PUBLIC CLASSES:
    ---------------

            See the individual classes' docstrings for additional details.


        Regular classes:
        ----------------

            Fixed                                       [module public class]

                A simple class for fixed-point numbers.
                

        Exception classes:
        ------------------

            FixedError                          [module public exception class]

                Base class for error exceptions in the fixed module.
                These errors are automatically logged upon creation.

            InitialValueError                   [module public exception class]

                An error exception indicating that something was wrong
                with an initial-value argument passed to an initializ-
                er of a class in the fixed module.

            NoInitialValueError                 [module public exception class]

                An error exception indicating that no initial value
                argument was passed to an initializer of a class in
                the fixed module, and one was expected.
        
                                                                             """
#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#| End of module documentation string.
#|------------------------------------------------------------------------------


    #|==========================================================================
    #|   1. Module imports.                                [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|  1.1. Imports of standard python modules.    [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

import math         # Defines ceil, floor, etc.
import numbers      # Defines the Rational abstract base class.
import operator     # Module defining standard arithmetic operators
import fractions    # Includes the Fraction class.

        #|======================================================================
        #|  1.2. Imports of custom application modules. [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

import logmaster                        # Provides logging capabilities.
from logmaster import ErrorException    # We use this name a couple of times.


    #|==========================================================================
    #|  2.  Global constants, variables, and objects.      [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|  2.1.  Special globals.                      [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

__all__ = [                 # List of all explicitly-exported public names.
    'Fixed',
    'FixedError',           # Exception classes.
    'InitialValueError',
    'NoInitialValueError'
    ]

        #|======================================================================
        #|  2.3.  Private globals.                      [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

_logger = logmaster.getLogger(logmaster.sysName + '.fixed')     # Module logger.


    #|==========================================================================
    #|  3.  Class definitions.                             [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|  3.1.  Exception classes.                    [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            #|------------------------------------------------------------------
            #|  FixedError                              [public exception class]
            #|
            #|      Base class for error exceptions in the fixed
            #|      module.  These errors are automatically logged
            #|      upon creation.
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    # Alternatively to the below, we could subclass logmaster.LoggedException
    # to create FixedException, and then mixin ErrorException with that to get
    # FixedError.  This would allow us to do module-specific logged exceptions
    # at other levels as well (info, warning, critical, etc.)  So far we
    # haven't needed that capability, though.

class FixedError(ErrorException):       # Error in this fixed-point module.
    """This base class is for errors detected in 'fixed', the fixed-point
       arithmetic module."""
    def __init__(inst, msg:str=None):
        ErrorException.__init__(inst, msg=msg, logger=_logger)


            #|------------------------------------------------------------------
            #|  InitialValueError                       [public exception class]
            #|
            #|      An error exception indicating that something was
            #|      wrong with an initial-value argument passed to an
            #|      initializer of a class in the fixed module.
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class InitialValueError(FixedError):
    """An initial value that was passed as an argument to a
       constructor in this module ('fixed') was unacceptable."""
    pass

            #|------------------------------------------------------------------
            #|  NoInitialValueError                     [public exception class]
            #|
            #|      An error exception indicating that no initial
            #|      value argument was passed to an initializer of a
            #|      class in the fixed module, and one was expected.
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class NoInitialValueError(InitialValueError):
    """No initial value or an initial value of None was provided to a
        constructor, but a value other than None was required."""
    pass


        #|======================================================================
        #|   3.2.  Normal public classes.               [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            #|------------------------------------------------------------------
            #|  Fixed                                           [public class]
            #|
            #|      Class for fixed-point numbers with a specific
            #|      fractional quantum (currently 1e-9).
            #|
            #|      NOTE: To simplify user code, all instances of
            #|      Fixed within the system are required to have the
            #|      same quantum! This way the user does not have to
            #|      specify the quantum when creating fixed-point
            #|      number instances.
            #|
            #|      It may be worth considering whether it would be
            #|      useful to have a base Fixed class that is abstract
            #|      (leaves the denominator unspecified, as an ab-
            #|      stract property), and then have various subclas-
            #|      ses of it that give different values to the quan-
            #|      tum, or even allow the user to specify the quantum
            #|      dynamically during some class-initialization step.
            #|      This way, fixed-point numbers of different precis-
            #|      ion could be used within one application.  We're
            #|      not yet exploring this option, though.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class Fixed(numbers.Rational):
    
    """Fixed is a rational-number class (an implementation of the
       abstract base class numbers.Rational) in which all number
       instances have a fixed precision, in that they are all
       integer multiples of a fixed quantum 1/D, where D could be
       any fixed positive integer.  Currently D=1e9 (1 billion),
       so all Fixed numbers are defined to a precision of 1e-9
       (0.000000001), or nine decimal places."""

        #|======================== Within class: Fixed =========================
        #|  Private class attributes.                       [class code section]
        #|
        #|      These are similar to static data members in C++.
        #|,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

            #|------------------------------------------------------------------
            #|  Fixed._denominator:Integer             [private class attribute]
            #|
            #|      The denominator D of the quantum 1/D.  (Please
            #|      don't change this after instances have been
            #|      created, or insanity will ensue.)
            #|,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

    _denominator = int(1e9)      # Define all numbers to 1 billionth of a unit.

        #|======================== Within class: Fixed =========================
        #|  Private instance attributes.                   [class documentation]
        #|
        #|      These are similar to data members in C++.
        #|
        #|          inst._numerator:Integer         [private instance attribute]
        #|
        #|              The numerator N of this fixed-precision value
        #|              N/D.
        #|
        #|======================================================================
    
        #|======================== Within class: Fixed =========================
        #|  Special methods.                                [class code section]
        #|,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

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

    def __repr__(self):     # return faithful string representation

        """The faithful string representation of a Fixed looks like
           Fixed(<N>/<D>), where <N>/<D> is the fractional represen-
           tation of the value of the Fixed in lowest terms."""

        return 'Fixed(%d/%d)'%(self.numerator, self.denominator)

# The following is no longer used, since the above is usually more readable.

##        """The faithful string representation of a Fixed, which looks
##           like "Fixed(<N>,<D>)", includes both the numerator <N> and
##           the (supposedly fixed) denominator <D>.  This provides for
##           the ability to parse this output into a future version of
##           the Fixed class that supports alternate denominators.  It
##           also is more human-readable than if the denominator were
##           not provided.  Note that the Fixed initializer explicitly
##           supports the notation used here."""
##        
##        return 'Fixed(%d,%d)'%(self._numerator, Fixed._denominator)

    def __str__(self):      # return simple string representation
        
        """The simple string representation of a Fixed is whatever
           the fractions.Fraction class returns."""

        frac = fractions.Fraction(self._numerator, Fixed._denominator)
        return str(frac)

    def __format__(self, fmtSpec):
        frac = fractions.Fraction(self._numerator, Fixed._denominator)
        return frac.__format__(fmtSpec)

    #-- NOTE: Subclasses of numbers.Rational have to define all these methods:
    #
    #       __abs__, __add__, __ceil__, __eq__, __floor__, __floordiv__,
    #       __le__, __lt__, __mod__, __mul__, __neg__, __pos__, __pow__,
    #       __radd__, __rfloordiv__, __rmod__, __rmul__, __round__,
    #       __rpow__, __rtruediv__, __truediv__, __trunc__

        # ***** CONTINUE CLEANING UP BELOW HERE *****

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
        result = Fixed(pow(y, xfrac, mod))
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

#__/ End class Fixed.
    
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                   BOTTOM OF FILE:    fixed.py
#===============================================================================
