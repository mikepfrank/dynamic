#/==============================================================================
#|                          TOP OF FILE - fixedpoint.py
#|------------------------------------------------------------------------------
#|
#|      File name:      FixedPoint.py               [Python module source code]
#|
#|
#|      Description:
#|      ------------
#|
#|          This file defines a class called "FixedPoint" that provides
#|          a fixed-point arithmetic data type.  At present, all instances
#|          (objects of class FixedPoint) within a given application are
#|          created with the same precision by default.
#|
#|          FixedPoint is defined as a subclass of the standard library
#|          type fraction.Fraction.
#|
#|          Internally, FixedPoint is implemented using instances of the
#|          standard library class decimal.Decimal.  The difference from
#|          Decimal is that FixedPoint objects are always fixed-point
#|          (never floating-point) and they are mutable.
#|
#|
#|      Python language versions:
#|      -------------------------
#|
#|          * (To be) tested with Python 3.5.1 (Windows 64-bit)
#|
#|
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

"""A fixed-point arithmetic data type."""

#..../--------------------------------------------------------------------------
    #|
    #|      Imports.                                            [code section]
    #|
    #|          In this section, we import other modules that are used
    #|          by this module.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

#......../----------------------------------------------------------------------
        #|
        #|      Standard imports.                           [code subsection]
        #|
        #|          In this subsection, we import standard python
        #|          library modules.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

#..................../------------------------------------------|
                    #| Used by entity   | Names used from       |
                    #| in cur. module:  | imported module:      |
                    #|------------------+-----------------------|
import numbers      #|  FixedPoint      |   Rational, Integral  |
import fractions    #|  FixedPoint      |   Fraction            |
import decimal      #|  FixedPoint      |   
                    #|------------------------------------------/

#..../--------------------------------------------------------------------------
    #|
    #|      Globals.                                             [code section]
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

#......../----------------------------------------------------------------------
        #|
        #|      Global constant parameters.                 [code subsection]
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

#............/------------------------------------------------------------------
            #|
            #|      DEFAULT_PRECISION               [global constant parameter]
            #|
            #|          Non-negative integer specifying the number of
            #|          (decimal) digits of precision for all new objects
            #|          of class FixedPoint.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global  DEFAULT_PRECISION

DEFAULT_PRECISION   =   9               # Nine digits after decimal point =
                                        # precise to 1 part in a billion.

#..../ Define this little utility function before the functions section
    #| so that we can use it to initialize later constants.

def quantum(precision:numbers.Integral=DEFAULT_PRECISION):
    return decimal.Decimal(10) ** -precision

#............/------------------------------------------------------------------
            #|
            #|      DEFAULT_QUANTUM                 [global constant parameter]
            #|
            #|          A decimal.Decimal value giving the smallest
            #|          quantum for the default number representation.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global  DEFAULT_QUANTUM

DEFAULT_QUANTUM = quantum()


#............/------------------------------------------------------------------
            #|
            #|      DEFAULT_DIVISOR                 [global constant parameter]
            #|
            #|          All new instances of class FixedPoint will be
            #|          assigned this value for their divisor parameter
            #|          if not otherwise specified.  (This determines the
            #|          precision with which that fixed-point number is
            #|          defined.)
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global  DEFAULT_DIVISOR

DEFAULT_DIVISOR     =   pow(10, DEFAULT_PRECISION)      # One billion (10^9).


#............|/-----------------------------------------------------------------
            #|
            #|      DEFAULT_CONTEXT                 [global constant object]
            #|
            #|          All new instances of class FixedPoint will use
            #|          the given decimal arithmetic context (see the
            #|          documentation for the decimal module) internally
            #|          for their decimal number representations if not
            #|          otherwise specified.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global  DEFAULT_CONTEXT

#.... Temporarily modify the current decimal context to configure the default
    # context for use in this module.

with decimal.localContext(decimal.getContext()):

    if DEFAULT_PRECISION == 9:
        decimal.setContext(decimal.BasicContext)    # This is a standard 9-digit context.
    else:
        decimal.getContext().prec = DEFAULT_PRECISION
        #   \__ Creates a context with the requested precision and
        #       other settings.  (Note these may be different from
        #       the settings in the case for precision 9.)

    DEFAULT_CONTEXT = decimal.getContext()      # Remember this context.


#..../--------------------------------------------------------------------------
    #|
    #|      Class definitions.                                  [code section]
    #|
    #|          In this section we define the classes that are provided
    #|          by this module.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

#......../----------------------------------------------------------------------
        #|
        #|      FixedPoint                                      [public class]
        #|
        #|          This is the main class provided by this module.
        #|
        #|          FixedPoint is defined as a subclass of the
        #|          standard class fractions.Fraction.
        #|
        #|          A number of class FixedPoint is conceptually stored
        #|          as a pair of integers:  A variable dividend and a
        #|          constant divisor.
        #|
        #|          In practice, the implementation is to use the
        #|          Python standard library's decimal.Decimal() class
        #|          and quantize the value to the desired number of
        #|          decimal places.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class FixedPoint(Fraction):

    #..../----------------------------------------------------------------------
        #|
        #|      Class attributes.                               [class section]
        #|
        #|          In this section, we define variable or constant
        #|          parameters that are shared across all members of
        #|          the given class.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    #......../------------------------------------------------------------------
            #|
            #|      .defaultPrecision               [integer class variable]
            #|
            #|          This class variable determines the number of
            #|          decimal places of precision for all newly-created
            #|          instances of class FixedPoint.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    defaultPrecision = DEFAULT_PRECISION

    #......../------------------------------------------------------------------
            #|
            #|      .defaultQuantum                 [decimal class variable]
            #|
            #|          The decimal.Decimal() value representing the
            #|          smallest positive value representable in 
            #|          FixedPoint instances with the default precision.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    defaultQuantum = quantum(DEFAULT_PRECISION)

    #......../------------------------------------------------------------------
            #|
            #|      .defaultDivisor                 [integer class variable]
            #|
            #|          This class variable determines the default value
            #|          of the divisor attribute for newly created
            #|          instances of class FixedPoint.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    defaultDivisor = DEFAULT_DIVISOR

    #......../------------------------------------------------------------------
            #|
            #|      .defaultContext                 [class variable object]
            #|
            #|          This class variable is an object of type
            #|          decimal.Context that specifies how arithmetic
            #|          will be done on new instances of class FixedPoint.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    defaultContext = DEFAULT_CONTEXT

    #..../----------------------------------------------------------------------
        #|
        #|      Instance attributes.                            [class section]
        #|
        #|          These are attributes of individual instances of the
        #|          FixedPoint class.  In Python, these are not defined
        #|          formally as part of the class defintion, but as a
        #|          matter of style, we define them in this comment.
        #|          They are as follows:
        #|
        #|
        #|          Constant instance attributes (instance parameters):
        #|
        #|              .precision                  [integer instance parameter]
        #|
        #|                  Number of decimal digits of precision of this
        #|                  FixedPoint number.
        #|
        #|              .quantum                    [decimal instance parameter]
        #|
        #|                  The decimal.Decimal value of the smallest
        #|                  representable positive value for this
        #|                  particular FixedPoint instance.
        #|
        #|              .divisor                    [integer instance parameter]
        #|
        #|                  Implied divisor or denominator for fractional
        #|                  representation of this FixedPoint number.  (This
        #|                  is a constant based on the precision and is not
        #|                  reduced to lowest terms.)
        #|
        #|              .context            [decimal.Context instance parameter]
        #|
        #|                  The object of type decimal.Context to be used
        #|                  for working with this FixedPoint number.
        #|
        #|
        #|          Variable instance attributes (instance variables):
        #|
        #|              .value              [decimal.Decimal instance variable]
        #|
        #|                  The decimal.Decimal object representing the
        #|                  current value of this FixedPoint instance.
        #|
        #|              .dividend                   [integer instance variable]
        #|
        #|                  The implied dividend or numerator for a
        #|                  fractional representation of the current
        #|                  value of this FixedPoint number.  (This is
        #|                  not reduced to lowest terms.)
        #|
        #|----------------------------------------------------------------------

    #..../----------------------------------------------------------------------
        #|
        #|      Methods.                                        [class section]
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    #......../------------------------------------------------------------------
            #|
            #|      Special methods.                            [class section]
            #|
            #|          In this section, we define special methods that have
            #|          reserved names in Python.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    #............/--------------------------------------------------------------
                #|
                #|      .__init__()                             [special method]
                #|
                #|          The .__init__() special method is used to initalize
                #|          new instances of a given class.  The local variable
                #|          "self" is used to refer to the uninitialized object.
                #|
                #|      Arguments:
                #|
                #|          value - The value that this FixedPoint instance
                #|                  should be initialized with.  This may be
                #|                  any number.Real value, but it may end
                #|                  up getting rounded.
                #|
                #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def __init__(self, value=0, precision:Integral=defaultPrecision):

        self.precision = precision

        self.quantum = quantum(precision)

        self.divisor = pow(10,precision)
        
        if precision == defaultPrecision:
            self.context = defaultContext
        else:
            self.context = decimal.Context(precision)

        with decimal.localcontext(self.context):

            dec = decimal.Decimal(value)

            self.value = dec.quantize(self.quantum)

    
