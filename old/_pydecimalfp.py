# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        _pydecimalfp
## Purpose:     Decimal fixed-point arithmetic (Python implementation)
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) 2001 ff. Michael Amrhein
##              Portions adopted from FixedPoint.py written by Tim Peters
## License:     This program is free software. You can redistribute it, use it
##              and/or modify it under the terms of the 2-clause BSD license.
##              For license details please read the file LICENSE.TXT provided
##              together with the source code.
##----------------------------------------------------------------------------
## $Source: _pydecimalfp.py $
## $Revision: 57be6576e3c7 2015-03-27 13:28 +0100 mamrhein $


"""Decimal fixed-point arithmetic."""


from __future__ import absolute_import, division
import sys
import locale
import math
import numbers
import operator
from decimalfp import _get_limit_prec, get_rounding
from decimal import Decimal as _StdLibDecimal
from fractions import gcd, Fraction
from functools import reduce
# rounding modes
from decimal import ROUND_DOWN, ROUND_UP, ROUND_HALF_DOWN, ROUND_HALF_UP,\
    ROUND_HALF_EVEN, ROUND_CEILING, ROUND_FLOOR, ROUND_05UP


__version__ = 0, 9, 11


# Python 2 / Python 3
if sys.version_info[0] < 3:
    # rounding mode of builtin round function
    DFLT_ROUNDING = ROUND_HALF_UP
else:
    # In 3.0 round changed from half-up to half-even !
    DFLT_ROUNDING = ROUND_HALF_EVEN

# Compatible testing for strings
str = type(u'')
bytes = type(b'')
str_types = (bytes, str)


class Decimal(numbers.Rational):

    """Decimal number with a given number of fractional digits.

    Args:
        value (see below): numerical value (default: 0)
        precision (int): number of fractional digits (default: None)

    If `value` is given, it must either be a string (type `str` or `unicode`
    in Python 2.x, `bytes` or `str` in Python 3.x), an instance of
    `number.Integral` (for example `int` or `long` in Python 2.x, `int` in
    Python 3.x), `number.Rational` (for example `fractions.Fraction`),
    `decimal.Decimal` or `float` or be convertable to a `float` or an `int`.

    If a string is given as value, it must be a string in one of two formats:

    * [+|-]<int>[.<frac>][<e|E>[+|-]<exp>] or

    * [+|-].<frac>[<e|E>[+|-]<exp>].

    Returns:
        :class:`Decimal` instance derived from `value` according
            to `precision`

    The value is always adjusted to the given precision or the precision is
    calculated from the given value, if no precision is given. For performance
    reasons, in the latter case the conversion of a `numbers.Rational` (like
    `fractions.Fraction`) or a `float` tries to give an exact result as a
    :class:`Decimal` only up to a fixed limit of fractional digits. This limit
    defaults to 32 and is accessible as `decimalfp.LIMIT_PREC`.

    Raises:
        TypeError: `precision` is given, but not of type `int`.
        TypeError: `value` is not an instance of the types listed above and
            not convertable to `float` or `int`.
        ValueError: `precision` is given, but not >= 0.
        ValueError: `value` can not be converted to a `Decimal` (with a number
            of fractional digits <= `LIMIT_PREC` if no `precision` is given).

    :class:`Decimal` instances are immutable.
    """

    __slots__ = ('_value', '_precision',
                 # used for caching values only:
                 '_hash', '_numerator', '_denominator'
                 )

    def __init__(self, value=None, precision=None):

        if precision is None:
            if value is None:
                self._value = 0
                self._precision = 0
                return
        else:
            if not isinstance(precision, int):
                raise TypeError("Precision must be of <type 'int'>.")
            if precision < 0:
                raise ValueError("Precision must be >= 0.")
            if value is None:
                self._value = 0
                self._precision = precision
                return

        # Decimal
        if isinstance(value, Decimal):
            self._precision = prec = value._precision
            self._value = value._value
            if precision is not None and precision != prec:
                _adjust(self, precision)
            return

        # String
        if isinstance(value, str_types):
            prec = -1 if precision is None else precision
            try:
                s = value.encode()
            except AttributeError:
                s = value
            try:
                _dec_from_str(self, s, prec)
            except ValueError:
                raise ValueError("Can't convert %s to Decimal." % repr(value))
            return

        # Integral
        if isinstance(value, numbers.Integral):
            lValue = int(value)
            if precision is None:
                self._precision = 0
                self._value = lValue
            else:
                self._precision = precision
                self._value = lValue * 10 ** precision
            return

        # Decimal (from standard library)
        if isinstance(value, _StdLibDecimal):
            if value.is_finite():
                sign, digits, exp = value.as_tuple()
                coeff = (-1) ** sign * reduce(lambda x, y: x * 10 + y, digits)
                prec = -1 if precision is None else precision
                _dec_from_coeff_exp(self, coeff, exp, prec)
                return
            else:
                raise ValueError("Can't convert %s to Decimal." % repr(value))

        # Rational
        if isinstance(value, numbers.Rational):
            prec = -1 if precision is None else precision
            num, den = value.numerator, value.denominator
            try:
                _dec_from_rational(self, num, den, prec)
            except ValueError:
                    raise ValueError("Can't convert %s exactly to Decimal."
                                     % repr(value))
            return

        # Float
        if isinstance(value, float):
            try:
                num, den = value.as_integer_ratio()
            except (ValueError, OverflowError):
                raise ValueError("Can't convert %s to Decimal." % repr(value))
            prec = -1 if precision is None else precision
            try:
                _dec_from_rational(self, num, den, prec)
            except ValueError:
                    raise ValueError("Can't convert %s exactly to Decimal."
                                     % repr(value))
            return

        # Others
        # If there's a float or int equivalent to value, use it
        ev = None
        try:
            ev = float(value)
        except:
            try:
                ev = int(value)
            except:
                pass
        if ev == value:     # do we really have the same value?
            dec = Decimal(ev, precision)
            self._value = dec._value
            self._precision = dec._precision
            return

        # unable to create Decimal
        raise TypeError("Can't convert %s to Decimal." % repr(value))

    # to be compatible to fractions.Fraction
    @classmethod
    def from_float(cls, f):
        """Convert a finite float (or int) to a :class:`Decimal`.

        Args:
            f (float or int): number to be converted to a `Decimal`

        Returns:
            :class:`Decimal` instance derived from `f`

        Raises:
            TypeError: `f` is neither a `float` nor an `int`.
            ValueError: `f` can not be converted to a :class:`Decimal` with
                a precision <= `LIMIT_PREC`.

        Beware that Decimal.from_float(0.3) != Decimal('0.3').
        """
        if not isinstance(f, (float, numbers.Integral)):
            raise TypeError("%s is not a float." % repr(f))
        return cls(f)

    # to be compatible to fractions.Fraction
    @classmethod
    def from_decimal(cls, d):
        """Convert a finite decimal number to a :class:`Decimal`.

        Args:
            d (see below): decimal number to be converted to a
                :class:`Decimal`

        `d` can be of type :class:`Decimal`, `numbers.Integral` or
        `decimal.Decimal`.

        Returns:
            :class:`Decimal` instance derived from `d`

        Raises:
            TypeError: `d` is not an instance of the types listed above.
            ValueError: `d` can not be converted to a :class:`Decimal`.
        """
        if not isinstance(d, (Decimal, numbers.Integral, _StdLibDecimal)):
            raise TypeError("%s is not a Decimal." % repr(d))
        return cls(d)

    @classmethod
    def from_real(cls, r, exact=True):
        """Convert a Real number to a :class:`Decimal`.

        Args:
            r (`numbers.Real`): number to be converted to a :class:`Decimal`
            exact (`bool`): `True` if `r` shall exactly be represented by
                the resulting :class:`Decimal`

        Returns:
            :class:`Decimal` instance derived from `r`

        Raises:
            TypeError: `r` is not an instance of `numbers.Real`.
            ValueError: `exact` is `True` and `r` can not exactly be converted
                to a :class:`Decimal` with a precision <= `LIMIT_PREC`.

        If `exact` is `False` and `r` can not exactly be represented by a
        `Decimal` with a precision <= `LIMIT_PREC`, the result is rounded to a
        precision = `LIMIT_PREC`.
        """
        if not isinstance(r, numbers.Real):
            raise TypeError("%s is not a Real." % repr(r))
        try:
            return cls(r)
        except ValueError:
            if exact:
                raise
            else:
                return cls(r, _get_limit_prec())

    @property
    def precision(self):
        """Return precision of `self`."""
        return self._precision

    @property
    def magnitude(self):
        """Return magnitude of `self` in terms of power to 10, i.e. the
        largest integer exp so that 10 ** exp <= self."""
        return int(math.floor(math.log10(abs(self._value)))) - self._precision

    @property
    def numerator(self):
        """Return the numerator from the pair of integers with the smallest
        positive denominator, whose ratio is equal to `self`."""
        try:
            return self._numerator
        except AttributeError:
            self._numerator, self._denominator = self.as_integer_ratio()
            return self._numerator

    @property
    def denominator(self):
        """Return the smallest positive denominator from the pairs of
        integers, whose ratio is equal to `self`."""
        try:
            return self._denominator
        except AttributeError:
            self._numerator, self._denominator = self.as_integer_ratio()
            return self._denominator

    @property
    def real(self):
        """The real part of `self`.

        Returns `self` (Real numbers are their real component)."""
        return self

    @property
    def imag(self):
        """The imaginary part of `self`.

        Returns 0 (Real numbers have no imaginary component)."""
        return 0

    def adjusted(self, precision=None, rounding=None):
        """Return copy of `self`, adjusted to the given `precision`, using the
        given `rounding` mode.

        Args:
            precision (int): number of fractional digits (default: None)
            rounding (str): rounding mode (default: None)

        Returns:
            :class:`Decimal` instance derived from `self`, adjusted
                to the given `precision`, using the given `rounding` mode

        If no `precision` is given, the result is adjusted to the minimum
        precision preserving x == x.adjusted().

        If no `rounding` mode is given, the default mode from the current
        context (from module `decimal`) is used.

        If the given `precision` is less than the precision of `self`, the
        result is rounded and thus information may be lost.
        """
        if precision is None:
            v, p = _reduce(self)
            result = Decimal()
            result._value = v
            result._precision = p
        else:
            if not isinstance(precision, int):
                raise TypeError("Precision must be of <type 'int'>.")
            result = Decimal(self)
            _adjust(result, precision, rounding)
        return result

    def quantize(self, quant, rounding=None):
        """Return integer multiple of `quant` closest to `self`.

        Args:
            quant (Rational): quantum to get a multiple from
            rounding (str): rounding mode (default: None)

        A string can be given for `quant` as long as it is convertable to a
        :class:`Decimal`.

        If no `rounding` mode is given, the default mode from the current
        context (from module `decimal`) is used.

        Returns:
            :class:`Decimal` instance that is the integer multiple of `quant`
                closest to `self` (according to `rounding` mode); if result
                can not be represented as :class:`Decimal`, an instance of
                `Fraction` is returned

        Raises:
            TypeError: `quant` is not a Rational number or can not be
                converted to a :class:`Decimal`
        """
        try:
            num, den = quant.numerator, quant.denominator
        except AttributeError:
            try:
                num, den = quant.as_integer_ratio()
            except AttributeError:
                try:
                    quant = Decimal(quant)
                except (TypeError, ValueError):
                    raise TypeError("Can't quantize to a '%s': %s."
                                    % (quant.__class__.__name__, quant))
                num, den = quant.as_integer_ratio()
        mult = _div_rounded(self._value * den, 10 ** self._precision * num,
                            rounding)
        return Decimal(mult) * quant

    def as_tuple(self):
        """Return a tuple (sign, coeff, exp) so that
        self == (-1) ** sign * coeff * 10 ** exp."""
        v = self._value
        sign = int(v < 0)
        coeff = abs(v)
        exp = -self._precision
        return sign, coeff, exp

    # return lowest fraction equal to self
    def as_integer_ratio(self):
        """Return the pair of numerator and denominator with the smallest
        positive denominator, whose ratio is equal to self."""
        n, d = self._value, 10 ** self._precision
        g = gcd(n, d)
        return n // g, d // g

    def __copy__(self):
        """Return self (Decimal instances are immutable)."""
        return self

    def __deepcopy__(self, memo):
        return self.__copy__()

    def __reduce__(self):
        return (Decimal, (), (self._value, self._precision))

    def __setstate__(self, state):
        self._value, self._precision = state

    # string representation
    def __repr__(self):
        """repr(self)"""
        sp = self._precision
        rv, rp = _reduce(self)
        if rp == 0:
            s = str(rv)
        else:
            s = str(abs(rv))
            n = len(s)
            if n > rp:
                s = "'%s%s.%s'" % ((rv < 0) * '-', s[0:-rp], s[-rp:])
            else:
                s = "'%s0.%s%s'" % ((rv < 0) * '-', (rp - n) * '0', s)
        if sp == rp:
            return "Decimal(%s)" % (s)
        else:
            return "Decimal(%s, %s)" % (s, sp)

    def __str__(self):
        """str(self)"""
        sp = self._precision
        if sp == 0:
            return "%i" % self._value
        else:
            sv = self._value
            i = _int(sv, sp)
            f = sv - i * 10 ** sp
            s = (i == 0 and f < 0) * '-'  # -1 < self < 0 => i = 0 and f < 0 !
            return '%s%i.%0*i' % (s, i, sp, abs(f))

    def __format__(self, fmtSpec):
        """Return `self` converted to a string according to given format
        specifier.

        Args:
            fmtSpec (str): a standard format specifier for a number

        Returns:
            str: `self` converted to a string according to `fmtSpec`
        """
        (fmtFill, fmtAlign, fmtSign, fmtMinWidth, fmtThousandsSep,
            fmtGrouping, fmtDecimalPoint, fmtPrecision,
            fmtType) = _getFormatParams(fmtSpec)
        nToFill = fmtMinWidth
        prec = self._precision
        if fmtPrecision is None:
            fmtPrecision = prec
        if fmtType == '%':
            percentSign = '%'
            nToFill -= 1
            xtraShift = 2
        else:
            percentSign = ''
            xtraShift = 0
        val = _get_adjusted_value(self, fmtPrecision + xtraShift)
        if val < 0:
            sign = '-'
            nToFill -= 1
            val = abs(val)
        elif fmtSign == '-':
            sign = ''
        else:
            sign = fmtSign
            nToFill -= 1
        rawDigits = format(val, '>0%i' % (fmtPrecision + 1))
        if fmtPrecision:
            decimalPoint = fmtDecimalPoint
            rawDigits, fracPart = (rawDigits[:-fmtPrecision],
                                   rawDigits[-fmtPrecision:])
            nToFill -= fmtPrecision + 1
        else:
            decimalPoint = ''
            fracPart = ''
        if fmtAlign == '=':
            intPart = _padDigits(rawDigits, max(0, nToFill), fmtFill,
                                 fmtThousandsSep, fmtGrouping)
            return sign + intPart + decimalPoint + fracPart + percentSign
        else:
            intPart = _padDigits(rawDigits, 0, fmtFill,
                                 fmtThousandsSep, fmtGrouping)
            raw = sign + intPart + decimalPoint + fracPart + percentSign
            if nToFill > len(intPart):
                fmt = "%s%s%i" % (fmtFill, fmtAlign, fmtMinWidth)
                return format(raw, fmt)
            else:
                return raw

    # compare to Decimal or any type that can be converted to a Decimal
    def _make_comparable(self, other):
        if isinstance(other, Decimal):
            selfPrec, otherPrec = self._precision, other._precision
            if selfPrec == otherPrec:
                return self._value, other._value
            elif selfPrec < otherPrec:
                return (_get_adjusted_value(self, otherPrec), other._value)
            else:
                return (self._value, _get_adjusted_value(other, selfPrec))
        if isinstance(other, numbers.Integral):
            return self._value, other * 10 ** self._precision
        if isinstance(other, numbers.Rational):
            return (self.numerator * other.denominator,
                    other.numerator * self.denominator)
        if isinstance(other, float):
            num, den = other.as_integer_ratio()
            return (self.numerator * den, num * self.denominator)
        if isinstance(other, _StdLibDecimal):
            return (self, Decimal(other))
        if isinstance(other, numbers.Complex) and other.imag == 0:
            return self._make_comparable(other.real)
        else:
            raise TypeError

    def _compare(self, other, op):
        """Compare self and other using operator op."""
        try:
            selfVal, otherVal = self._make_comparable(other)
        except TypeError:
            return NotImplemented
        return op(selfVal, otherVal)

    def __eq__(self, other):
        """self == other"""
        return self._compare(other, operator.eq)

    def __lt__(self, other):
        """self < other"""
        return self._compare(other, operator.lt)

    def __le__(self, other):
        """self <= other"""
        return self._compare(other, operator.le)

    def __gt__(self, other):
        """self > other"""
        return self._compare(other, operator.gt)

    def __ge__(self, other):
        """self >= other"""
        return self._compare(other, operator.ge)

    def __hash__(self):
        """hash(self)"""
        try:
            return self._hash
        except AttributeError:
            selfVal, selfPrec = self._value, self._precision
            if selfPrec == 0:           # if self == int(self),
                return hash(selfVal)    # same hash as int
            else:               # otherwise same hash as equivalent fraction
                return hash(Fraction(selfVal, 10 ** selfPrec))

    # return 0 or 1 for truth-value testing
    def __nonzero__(self):
        """bool(self)"""
        return self._value != 0
    __bool__ = __nonzero__

    # return integer portion as int
    def __int__(self):
        """math.trunc(self)"""
        return _int(self._value, self._precision)
    __trunc__ = __int__

    # convert to float (may loose precision!)
    def __float__(self):
        """float(self)"""
        return self._value / 10 ** self._precision

    def __pos__(self):
        """+self"""
        return self

    def __neg__(self):
        """-self"""
        result = Decimal(self)
        result._value = -result._value
        return result

    def __abs__(self):
        """abs(self)"""
        result = Decimal(self)
        result._value = abs(result._value)
        return result

    def __add__(x, y):
        """x + y"""
        return add(x, y)

    # other + self
    __radd__ = __add__

    def __sub__(x, y):
        """x - y"""
        return sub(x, y)

    def __rsub__(x, y):
        """y - x"""
        return add(-x, y)

    def __mul__(x, y):
        """x * y"""
        return mul(x, y)

    # other * self
    __rmul__ = __mul__

    def __div__(x, y):
        """x / y"""
        return div1(x, y)

    def __rdiv__(x, y):
        """y / x"""
        return div2(y, x)

    # Decimal division is true division
    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __divmod__(x, y):
        """x // y, x % y"""
        return divmod1(x, y)

    def __rdivmod__(x, y):
        """y // x, y % x"""
        return divmod2(y, x)

    def __floordiv__(x, y):
        """x // y"""
        return floordiv1(x, y)

    def __rfloordiv__(x, y):
        """y // x"""
        return floordiv2(y, x)

    def __mod__(x, y):
        """x % y"""
        return mod1(x, y)

    def __rmod__(x, y):
        """y % x"""
        return mod2(y, x)

    def __pow__(x, y, mod=None):
        """x ** y

        If y is an integer (or a Rational with denominator = 1), the
        result will be a Decimal. Otherwise, the result will be a float or
        complex since roots are generally irrational.

        `mod` must always be None (otherwise a `TypeError` is raised).
        """
        if mod is not None:
            raise TypeError("3rd argument not allowed unless all arguments "
                            "are integers")
        return pow1(x, y)

    def __rpow__(x, y, mod=None):
        """y ** x

        `mod` must always be None (otherwise a `TypeError` is raised).
        """
        if mod is not None:
            raise TypeError("3rd argument not allowed unless all arguments "
                            "are integers")
        return pow2(y, x)

    def __floor__(self):
        """math.floor(self)"""
        n, d = self._value, 10 ** self._precision
        return n // d

    def __ceil__(self):
        """math.ceil(self)"""
        n, d = self._value, 10 ** self._precision
        return -(-n // d)

    def __round__(self, precision=None):
        """round(self [, ndigits])

        Round `self` to a given precision in decimal digits (default 0).
        `ndigits` may be negative.

        Note: This method is called by the built-in `round` function only in
        Python 3.x! It returns an `int` when called with one argument,
        otherwise a :class:`Decimal`.
        """
        if precision is None:
            # return integer
            return int(self.adjusted(0, DFLT_ROUNDING))
        # otherwise return Decimal
        return self.adjusted(precision, DFLT_ROUNDING)


# helper functions:


# parse string
import re
_pattern = r"""
            \s*
            (?P<sign>[+|-])?
            (
                (?P<int>\d+)(\.(?P<frac>\d*))?
                |
                \.(?P<onlyfrac>\d+)
            )
            ([eE](?P<exp>[+|-]?\d+))?
            \s*$
            """.encode()
_parseString = re.compile(_pattern, re.VERBOSE).match


def _dec_from_str(dec, s, prec):
    parsed = _parseString(s)
    if parsed is None:
        raise ValueError
    sExp = parsed.group('exp')
    if sExp:
        exp = int(sExp)
    else:
        exp = 0
    sInt = parsed.group('int')
    if sInt:
        nInt = int(sInt)
        sFrac = parsed.group('frac')
    else:
        nInt = 0
        sFrac = parsed.group('onlyfrac')
    if sFrac:
        nFrac = int(sFrac)
        shift10 = len(sFrac)
    else:
        nFrac = 0
        shift10 = 0
    coeff = nInt * 10 ** shift10 + nFrac
    exp -= shift10
    if parsed.group('sign') == b'-':
        coeff = -coeff
    _dec_from_coeff_exp(dec, coeff, exp, prec)


def _dec_from_coeff_exp(dec, coeff, exp, prec):
    """Set `dec` so that it equals coeff * 10 ** exp, rounded to precision
    `prec`."""
    if prec == -1:
        if exp > 0:
            dec._precision = 0
            dec._value = coeff * 10 ** exp
        else:
            dec._precision = abs(exp)
            dec._value = coeff
    else:
        dec._precision = prec
        shift10 = exp + prec
        if shift10 == 0:
            dec._value = coeff
        if shift10 > 0:
            dec._value = coeff * 10 ** shift10
        else:
            dec._value = _div_rounded(coeff, 10 ** -shift10)


def _dec_from_rational(dec, num, den, prec):
    if prec >= 0:
        dec._value = _div_rounded(num * 10 ** prec, den)
        dec._precision = prec
    else:
        rem = _approx_rational(dec, num, den)
        if rem:
            raise ValueError


def _approx_rational(dec, num, den, minPrec=0):
    """Approximate num / den as Decimal.

    Computes q, p, r, so that
        q * 10 ** -p + r = num / den
    and p <= max(minPrec, LIMIT_PREC) and r -> 0.
    Sets `dec` to q * 10 ** -p. Returns True if r != 0, False otherwise.
    """
    maxPrec = max(minPrec, _get_limit_prec())
    while True:
        prec = (minPrec + maxPrec) // 2
        quot, rem = divmod(num * 10 ** prec, den)
        if prec == maxPrec:
            break
        if rem == 0:
            maxPrec = prec
        elif minPrec >= maxPrec - 2:
            minPrec = maxPrec
        else:
            minPrec = prec
    dec._value = quot
    dec._precision = prec
    return (rem != 0)


# parse a format specifier
# [[fill]align][sign][0][minimumwidth][,][.precision][type]

_pattern = r"""
            \A
            (?:
                (?P<fill>.)?
                (?P<align>[<>=^])
            )?
            (?P<sign>[-+ ])?
            (?P<zeropad>0)?
            (?P<minimumwidth>(?!0)\d+)?
            (?P<thousands_sep>,)?
            (?:\.(?P<precision>0|(?!0)\d+))?
            (?P<type>[fFn%])?
            \Z
            """
_parseFormatSpec = re.compile(_pattern, re.VERBOSE).match
del re, _pattern

_dfltFormatParams = {'fill': ' ',
                     'align': '<',
                     'sign': '-',
                     #'zeropad': '',
                     'minimumwidth': 0,
                     'thousands_sep': '',
                     'grouping': [3, 0],
                     'decimal_point': '.',
                     'precision': None,
                     'type': 'f'}


def _getFormatParams(formatSpec):
    m = _parseFormatSpec(formatSpec)
    if m is None:
        raise ValueError("Invalid format specifier: " + formatSpec)
    fill = m.group('fill')
    zeropad = m.group('zeropad')
    if fill:                            # fill overrules zeropad
        fmtFill = fill
        fmtAlign = m.group('align')
    elif zeropad:                       # zeropad overrules align
        fmtFill = '0'
        fmtAlign = "="
    else:
        fmtFill = _dfltFormatParams['fill']
        fmtAlign = m.group('align') or _dfltFormatParams['align']
    fmtSign = m.group('sign') or _dfltFormatParams['sign']
    minimumwidth = m.group('minimumwidth')
    if minimumwidth:
        fmtMinWidth = int(minimumwidth)
    else:
        fmtMinWidth = _dfltFormatParams['minimumwidth']
    fmtType = m.group('type') or _dfltFormatParams['type']
    if fmtType == 'n':
        lconv = locale.localeconv()
        fmtThousandsSep = m.group('thousands_sep') and lconv['thousands_sep']
        fmtGrouping = lconv['grouping']
        fmtDecimalPoint = lconv['decimal_point']
    else:
        fmtThousandsSep = (m.group('thousands_sep') or
                           _dfltFormatParams['thousands_sep'])
        fmtGrouping = _dfltFormatParams['grouping']
        fmtDecimalPoint = _dfltFormatParams['decimal_point']
    precision = m.group('precision')
    if precision:
        fmtPrecision = int(precision)
    else:
        fmtPrecision = None
    return (fmtFill, fmtAlign, fmtSign, fmtMinWidth, fmtThousandsSep,
            fmtGrouping, fmtDecimalPoint, fmtPrecision, fmtType)


def _padDigits(digits, minWidth, fill, sep=None, grouping=None):
    nDigits = len(digits)
    if sep and grouping:
        slices = []
        i = j = 0
        limit = max(minWidth, nDigits) if fill == '0' else nDigits
        for l in _iterGrouping(grouping):
            j = min(i + l, limit)
            slices.append((i, j))
            if j >= limit:
                break
            i = j
            limit = max(limit - 1, nDigits, i + 1)
        if j < limit:
            slices.append((j, limit))
        digits = (limit - nDigits) * fill + digits
        raw = sep.join([digits[limit - j: limit - i]
                       for i, j in reversed(slices)])
        return (minWidth - len(raw)) * fill + raw
    else:
        return (minWidth - nDigits) * fill + digits


def _iterGrouping(grouping):
    l = None
    for i in grouping[:-1]:
        yield i
        l = i
    i = grouping[-1]
    if i == 0:
        while l:
            yield l
    elif i != locale.CHAR_MAX:
        yield i


# helper functions for decimal arithmetic


def _adjust(dec, prec, rounding=None):
    """Adjust Decimal `dec` to precision `prec` using given rounding mode
    (or default mode if none is given)."""
    dp = prec - dec._precision
    if dp == 0:
        return
    elif dp > 0:
        dec._value *= 10 ** dp
    elif prec >= 0:
        dec._value = _div_rounded(dec._value, 10 ** -dp, rounding)
    else:
        dec._value = (_div_rounded(dec._value, 10 ** -dp, rounding)
                      * 10 ** -prec)
    dec._precision = max(prec, 0)


def _get_adjusted_value(dec, prec, rounding=None):
    """Return rv so that rv // 10 ** rp = v // 10 ** p,
    rounded to precision rp using given rounding mode (or default mode if none
    is given)."""
    dp = prec - dec._precision
    if dp == 0:
        return dec._value
    elif dp > 0:
        return dec._value * 10 ** dp
    elif prec >= 0:
        return _div_rounded(dec._value, 10 ** -dp, rounding)
    else:
        return (_div_rounded(dec._value, 10 ** -dp, rounding)
                * 10 ** -prec)


def _reduce(dec):
    """Return rv, rp so that rv // 10 ** rp = dec and rv % 10 != 0
    """
    v, p = dec._value, dec._precision
    if v == 0:
        return 0, 0
    while p > 0 and v % 10 == 0:
        p -= 1
        v = v // 10
    return v, p


# divide x by y, return rounded result
def _div_rounded(x, y, rounding=None):
    """Return x // y, rounded using given rounding mode (or default mode
    if none is given)."""
    quot, rem = divmod(x, y)
    if rem == 0:              # no need for rounding
        return quot
    return quot + _round(quot, rem, y, rounding)


def _int(v, p):
    """Return integral part of shifted decimal"""
    if p == 0:
        return v
    if v == 0:
        return v
    if p > 0:
        if v > 0:
            return v // 10 ** p
        else:
            return -(-v // 10 ** p)
    else:
        return v * 10 ** -p


def _div(num, den, minPrec):
    """Return num / den as Decimal, if possible with precision <=
    max(minPrec, LIMIT_PREC), otherwise as Fraction"""
    dec = Decimal()
    rem = _approx_rational(dec, num, den, minPrec)
    if rem == 0:
        return dec
    else:
        return Fraction(num, den)


def add(x, y):
    """x + y

    x must be a Decimal"""
    if isinstance(y, Decimal):
        p = x._precision - y._precision
        if p == 0:
            result = Decimal(x)
            result._value += y._value
        elif p > 0:
            result = Decimal(x)
            result._value += y._value * 10 ** p
        else:
            result = Decimal(y)
            result._value += x._value * 10 ** -p
        return result
    elif isinstance(y, numbers.Integral):
        p = x._precision
        result = Decimal(x)
        result._value += y * 10 ** p
        return result
    elif isinstance(y, numbers.Rational):
        y_numerator, y_denominator = (y.numerator, y.denominator)
    elif isinstance(y, float):
        y_numerator, y_denominator = y.as_integer_ratio()
    elif isinstance(y, _StdLibDecimal):
        return add(x, Decimal(y))
    else:
        return NotImplemented
    # handle Rational and float
    x_denominator = 10 ** x._precision
    num = x._value * y_denominator + x_denominator * y_numerator
    den = y_denominator * x_denominator
    minPrec = x._precision
    # return num / den as Decimal or as Fraction
    return _div(num, den, minPrec)


def sub(x, y):
    """x - y

    x must be a Decimal"""
    if isinstance(y, Decimal):
        p = x._precision - y._precision
        if p == 0:
            result = Decimal(x)
            result._value -= y._value
        elif p > 0:
            result = Decimal(x)
            result._value -= y._value * 10 ** p
        else:
            result = Decimal(y)
            result._value = x._value * 10 ** -p - y._value
        return result
    elif isinstance(y, numbers.Integral):
        p = x._precision
        result = Decimal(x)
        result._value -= y * 10 ** p
        return result
    elif isinstance(y, numbers.Rational):
        y_numerator, y_denominator = (y.numerator, y.denominator)
    elif isinstance(y, float):
        y_numerator, y_denominator = y.as_integer_ratio()
    elif isinstance(y, _StdLibDecimal):
        return sub(x, Decimal(y))
    else:
        return NotImplemented
    # handle Rational and float
    x_denominator = 10 ** x._precision
    num = x._value * y_denominator - x_denominator * y_numerator
    den = y_denominator * x_denominator
    minPrec = x._precision
    # return num / den as Decimal or as Fraction
    return _div(num, den, minPrec)


def mul(x, y):
    """x * y

    x must be a Decimal"""
    if isinstance(y, Decimal):
        result = Decimal(x)
        result._value *= y._value
        result._precision += y._precision
        return result
    elif isinstance(y, numbers.Integral):
        result = Decimal(x)
        result._value *= y
        return result
    elif isinstance(y, numbers.Rational):
        y_numerator, y_denominator = (y.numerator, y.denominator)
    elif isinstance(y, float):
        y_numerator, y_denominator = y.as_integer_ratio()
    elif isinstance(y, _StdLibDecimal):
        return x.__mul__(Decimal(y))
    else:
        return NotImplemented
    # handle Rational and float
    num = x._value * y_numerator
    den = y_denominator * 10 ** x._precision
    minPrec = x._precision
    # return num / den as Decimal or as Fraction
    return _div(num, den, minPrec)


def div1(x, y):
    """x / y

    x must be a Decimal"""
    if isinstance(y, Decimal):
        xp, yp = x._precision, y._precision
        num = x._value * 10 ** yp
        den = y._value * 10 ** xp
        minPrec = max(0, xp - yp)
        # return num / den as Decimal or as Fraction
        return _div(num, den, minPrec)
    elif isinstance(y, numbers.Rational):       # includes Integral
        y_numerator, y_denominator = (y.numerator, y.denominator)
    elif isinstance(y, float):
        y_numerator, y_denominator = y.as_integer_ratio()
    elif isinstance(y, _StdLibDecimal):
        return div1(x, Decimal(y))
    else:
        return NotImplemented
    # handle Rational and float
    num = x._value * y_denominator
    den = y_numerator * 10 ** x._precision
    minPrec = x._precision
    # return num / den as Decimal or as Fraction
    return _div(num, den, minPrec)


def div2(x, y):
    """x / y

    y must be a Decimal"""
    if isinstance(x, Decimal):
        xp, yp = x._precision, y._precision
        num = x._value * 10 ** yp
        den = y._value * 10 ** xp
        minPrec = max(0, xp - yp)
        # return num / den as Decimal or as Fraction
        return _div(num, den, minPrec)
    if isinstance(x, numbers.Rational):
        x_numerator, x_denominator = (x.numerator, x.denominator)
    elif isinstance(x, float):
        x_numerator, x_denominator = x.as_integer_ratio()
    elif isinstance(x, _StdLibDecimal):
        return div1(Decimal(x), y)
    else:
        return NotImplemented
    # handle Rational and float
    num = x_numerator * 10 ** y._precision
    den = y._value * x_denominator
    minPrec = y._precision
    # return num / den as Decimal or as Fraction
    return _div(num, den, minPrec)


def divmod1(x, y):
    """x // y, x % y

    x must be a Decimal"""
    if isinstance(y, Decimal):
        xp, yp = x._precision, y._precision
        if xp >= yp:
            r = Decimal(x)
            xv = x._value
            yv = y._value * 10 ** (xp - yp)
        else:
            r = Decimal(y)
            xv = x._value * 10 ** (yp - xp)
            yv = y._value
        q = xv // yv
        r._value = xv - q * yv
        return Decimal(q, r._precision), r
    elif isinstance(y, numbers.Integral):
        r = Decimal(x)
        xv = x._value
        xp = x._precision
        yv = y * 10 ** xp
        q = xv // yv
        r._value = xv - q * yv
        return Decimal(q, xp), r
    elif isinstance(y, _StdLibDecimal):
        return x.__divmod__(Decimal(y))
    else:
        return x // y, x % y


def divmod2(x, y):
    """x // y, x % y

    y must be a Decimal"""
    if isinstance(x, Decimal):
        xp, yp = x._precision, y._precision
        if xp >= yp:
            r = Decimal(x)
            xv = x._value
            yv = y._value * 10 ** (xp - yp)
        else:
            r = Decimal(y)
            xv = x._value * 10 ** (yp - xp)
            yv = y._value
        q = xv // yv
        r._value = xv - q * yv
        return Decimal(q, r._precision), r
    elif isinstance(x, numbers.Integral):
        r = Decimal(y)
        yv = y._value
        yp = y._precision
        xv = x * 10 ** yp
        q = xv // yv
        r._value = xv - q * yv
        return Decimal(q, yp), r
    elif isinstance(x, _StdLibDecimal):
        return Decimal(x).__divmod__(y)
    else:
        return x // y, x % y


def floordiv1(x, y):
    """x // y

    x must be a Decimal"""
    if isinstance(y, (Decimal, numbers.Integral, _StdLibDecimal)):
        return divmod1(x, y)[0]
    else:
        return Decimal(math.floor(x / y), x._precision)


def floordiv2(x, y):
    """x // y

    y must be a Decimal"""
    if isinstance(x, (Decimal, numbers.Integral, _StdLibDecimal)):
        return divmod2(x, y)[0]
    else:
        return Decimal(math.floor(x / y), y._precision)


def mod1(x, y):
    """x % y

    x must be a Decimal"""
    if isinstance(y, (Decimal, numbers.Integral, _StdLibDecimal)):
        return divmod1(x, y)[1]
    else:
        return x - y * (x // y)


def mod2(x, y):
    """x % y

    y must be a Decimal"""
    if isinstance(x, (Decimal, numbers.Integral, _StdLibDecimal)):
        return divmod2(x, y)[1]
    else:
        return x - y * (x // y)


def pow1(x, y):
    """x ** y

    x must be a Decimal"""
    if isinstance(y, numbers.Integral):
        exp = int(y)
        if exp >= 0:
            result = Decimal()
            result._value = x._value ** exp
            result._precision = x._precision * exp
            return result
        else:
            return 1 / pow1(x, -y)
    elif isinstance(y, numbers.Rational):
        if y.denominator == 1:
            return x ** y.numerator
        else:
            return float(x) ** float(y)
    else:
        return float(x) ** y


def pow2(x, y):
    """x ** y

    y must be a Decimal"""
    if y.denominator == 1:
        return x ** y.numerator
    return x ** float(y)


# helper for different rounding modes

def _round(q, r, y, rounding=None):
    if rounding is None:
        rounding = get_rounding()
    if rounding == ROUND_HALF_UP:
        # Round 5 up (away from 0)
        # |remainder| > |divisor|/2 or
        # |remainder| = |divisor|/2 and quotient >= 0
        # => add 1
        ar, ay = abs(2 * r), abs(y)
        if ar > ay or (ar == ay and q >= 0):
            return 1
        else:
            return 0
    if rounding == ROUND_HALF_EVEN:
        # Round 5 to even, rest to nearest
        # |remainder| > |divisor|/2 or
        # |remainder| = |divisor|/2 and quotient not even
        # => add 1
        ar, ay = abs(2 * r), abs(y)
        if ar > ay or (ar == ay and q % 2 != 0):
            return 1
        else:
            return 0
    if rounding == ROUND_HALF_DOWN:
        # Round 5 down
        # |remainder| > |divisor|/2 or
        # |remainder| = |divisor|/2 and quotient < 0
        # => add 1
        ar, ay = abs(2 * r), abs(y)
        if ar > ay or (ar == ay and q < 0):
            return 1
        else:
            return 0
    if rounding == ROUND_DOWN:
        # Round towards 0 (aka truncate)
        # quotient negativ => add 1
        if q < 0:
            return 1
        else:
            return 0
    if rounding == ROUND_UP:
        # Round away from 0
        # quotient not negativ => add 1
        if q >= 0:
            return 1
        else:
            return 0
    if rounding == ROUND_CEILING:
        # Round up (not away from 0 if negative)
        # => always add 1
        return 1
    if rounding == ROUND_FLOOR:
        # Round down (not towards 0 if negative)
        # => never add 1
        return 0
    if rounding == ROUND_05UP:
        # Round down unless last digit is 0 or 5
        # quotient not negativ and quotient divisible by 5 without remainder
        # or quotient negativ and (quotient + 1) not divisible by 5 without
        # remainder => add 1
        if q >= 0 and q % 5 == 0 or q < 0 and (q + 1) % 5 != 0:
            return 1
        else:
            return 0
