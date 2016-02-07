#!/usr/bin/env python
##****************************************************************************
## Name:        test_decimalfp
## Purpose:     Test driver for both implementations of decimalfp
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) Michael Amrhein
## License:     This program is free software. You can redistribute it, use it
##              and/or modify it under the terms of the 2-clause BSD license.
##              For license details please read the file LICENSE.TXT provided
##              together with the source code.
##****************************************************************************
## $Source: test/test_decimalfp.py $
## $Revision: 82898c4ba3ff 2015-11-19 19:05 +0100 mamrhein $

from __future__ import absolute_import, division
import sys
import platform
import os
import copy
import unittest
import math
import locale
from pickle import dumps, loads
from decimal import Decimal as _StdLibDecimal
from fractions import Fraction
from decimalfp import set_rounding, ROUND_DOWN, ROUND_UP, ROUND_HALF_DOWN, \
    ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_CEILING, ROUND_FLOOR, ROUND_05UP, \
    LIMIT_PREC
from _pydecimalfp import Decimal as _PyDecimal
from _cdecimalfp import Decimal as _CDecimal

Decimal = None

__version__ = 0, 9, 11

__metaclass__ = type


rounding_modes = [ROUND_DOWN, ROUND_UP, ROUND_HALF_DOWN, ROUND_HALF_UP,
                  ROUND_HALF_EVEN, ROUND_CEILING, ROUND_FLOOR, ROUND_05UP]

# set default rounding to ROUND_HALF_UP
set_rounding(ROUND_HALF_UP)


class IntWrapper():

    def __init__(self, i):
        self.i = i

    def __int__(self):
        return self.i

    def __eq__(self, i):
        return self.i == i


class DecimalTest:

    """Mix-in defining the tests."""

    def testConstructor(self):
        self.assertTrue(Decimal(Decimal(1)))
        self.assertEqual(Decimal(Decimal(1)), Decimal(1))
        self.assertTrue(Decimal(-1, 2))
        self.assertEqual(Decimal(-1, 2), -1)
        self.assertTrue(Decimal(-37, 100))
        self.assertEqual(Decimal(-37, 100), -37)
        self.assertTrue(Decimal(sys.maxsize ** 100))
        self.assertTrue(Decimal(1.111e12))
        self.assertEqual(Decimal(1.111e12), 1.111e12)
        self.assertTrue(Decimal(sys.float_info.max))
        self.assertEqual(Decimal(sys.float_info.max), sys.float_info.max)
        self.assertTrue(Decimal(sys.float_info.max, 27))
        self.assertRaises(ValueError, Decimal, sys.float_info.min)
        self.assertEqual(Decimal(sys.float_info.min, 32), 0)
        self.assertEqual(Decimal(sys.float_info.min, 320),
                         Decimal('2225073858507', 320) / 10 ** 320)
        self.assertTrue(Decimal(u'+21.4'))
        self.assertTrue(Decimal(b'+21.4'))
        self.assertNotEqual(Decimal('+21.4'), 21.4)
        self.assertTrue(Decimal('+1e2'))
        self.assertEqual(Decimal('+1e2'), 100)
        self.assertTrue(Decimal('12345678901234567890e-234'))
        self.assertTrue(Decimal('-1E2'))
        self.assertEqual(Decimal('-1E2'), -100)
        self.assertTrue(Decimal('   .23e+2 '))
        self.assertRaises(ValueError, Decimal, ' -  1.23e ')
        self.assertTrue(Decimal('+1e-2000'))
        self.assertTrue(Decimal(_StdLibDecimal('-123.4567')))
        self.assertTrue(Decimal(_StdLibDecimal('-123.4567'), 2))
        self.assertEqual(Decimal('-123.4567'),
                         Decimal(_StdLibDecimal('-123.4567')))
        self.assertEqual(Decimal('1.234e12'),
                         Decimal(_StdLibDecimal('1.234e12')))
        self.assertEqual(Decimal('1.234e-12'),
                         Decimal(_StdLibDecimal('1.234e-12')))
        self.assertRaises(TypeError, Decimal, 1, '')
        self.assertRaises(ValueError, Decimal, 1, -1)
        self.assertRaises(TypeError, Decimal, Decimal)
        self.assertRaises(ValueError, Decimal, 123.4567)
        self.assertRaises(ValueError, Decimal, float('nan'))
        self.assertRaises(ValueError, Decimal, float('inf'))
        self.assertRaises(ValueError, Decimal, _StdLibDecimal('nan'))
        self.assertRaises(ValueError, Decimal, _StdLibDecimal('inf'))
        self.assertRaises(ValueError, Decimal, Fraction(1, 3))
        self.assertEqual(Decimal(Fraction(1, 4)), Decimal('0.25'))
        self.assertEqual(Decimal('0.33'), Fraction('0.33'))
        self.assertEqual(Decimal(IntWrapper(7)), Decimal('7'))

    def testAlternateConstructors(self):
        self.assertEqual(Decimal.from_float(1.111e12), Decimal(1.111e12))
        self.assertEqual(Decimal.from_float(12), Decimal(12))
        self.assertRaises(TypeError, Decimal.from_float, '1.111e12')
        self.assertEqual(Decimal.from_decimal(_StdLibDecimal('1.23e12')),
                         Decimal('1.23e12'))
        self.assertEqual(Decimal.from_decimal(_StdLibDecimal(12)),
                         Decimal(12))
        self.assertRaises(TypeError, Decimal.from_decimal, '1.23e12')
        self.assertEqual(Decimal.from_real(0.25), Decimal(0.25))
        self.assertEqual(Decimal.from_real(Fraction(1, 4)), Decimal(0.25))
        self.assertRaises(ValueError, Decimal.from_real, Fraction(1, 3))
        self.assertEqual(Decimal.from_real(Fraction(1, 3), exact=False),
                         Decimal(Fraction(1, 3), LIMIT_PREC))

    def testHash(self):
        d = Decimal('7.5')
        self.assertEqual(hash(d), hash(d))
        self.assertEqual(hash(d), hash(Decimal(d)))
        self.assertEqual(hash(Decimal('1.5')), hash(Decimal('1.5000')))
        self.assertNotEqual(hash(Decimal('1.5')), hash(Decimal('1.5001')))
        self.assertEqual(hash(Decimal('25')), hash(25))
        self.assertEqual(hash(Decimal('0.25')), hash(0.25))
        self.assertNotEqual(hash(Decimal('0.33')), hash(0.33))
        self.assertEqual(hash(Decimal('0.25')), hash(Fraction(1, 4)))
        self.assertEqual(hash(Decimal('0.33')), hash(Fraction('0.33')))

    def testMagnitude(self):
        self.assertEqual(Decimal('12.345').magnitude, 1)
        self.assertEqual(Decimal('10').magnitude, 1)
        self.assertEqual(Decimal('-286718.338524635465625').magnitude, 5)
        self.assertEqual(Decimal('286718338524635465627.500').magnitude, 20)
        self.assertEqual(Decimal('0.12345').magnitude, -1)
        self.assertEqual(Decimal('-0.0012345').magnitude, -3)
        self.assertEqual(Decimal('-0.01').magnitude, -2)

    def testCoercions(self):
        f = Decimal('23.456')
        g = Decimal('57.99999999999999999999999999999999999')
        self.assertEqual(int(f), 23)
        self.assertEqual(int(-f), -23)
        self.assertEqual(int(g), 57)
        self.assertEqual(int(-g), -57)
        self.assertEqual(float(f), 23.456)
        self.assertEqual(float(g), 58.0)
        self.assertEqual(str(f), '23.456')
        self.assertEqual(str(g), '57.99999999999999999999999999999999999')
        self.assertTrue(float(Decimal(sys.float_info.max)))
        self.assertEqual(str(Decimal(-20.7e-3, 5)), '-0.02070')
        self.assertEqual(str(Decimal(-20.7e-12, 13)), '-0.0000000000207')
        self.assertEqual(str(Decimal(-20.5e-12, 13)), '-0.0000000000205')
        self.assertEqual(repr(Decimal('-23.400007', 3)),
                         "Decimal('-23.4', 3)")
        self.assertEqual(repr(f), "Decimal('23.456')")
        self.assertEqual(repr(f), repr(copy.copy(f)))
        self.assertEqual(repr(f), repr(copy.deepcopy(f)))

    def test_as_tuple(self):
        d = Decimal('23')
        self.assertEqual(d.as_tuple(), (0, 23, 0))
        d = Decimal('123.4567890')
        self.assertEqual(d.as_tuple(), (0, 1234567890, -7))
        d = Decimal('-12.3000')
        self.assertEqual(d.as_tuple(), (1, 123000, -4))

    def testComparision(self):
        f = Decimal('23.456')
        g = Decimal('23.4562398')
        h = Decimal('-12.3')
        self.assertTrue(f != g)
        self.assertTrue(f < g)
        self.assertTrue(g >= f)
        self.assertTrue(min(f, g) == min(g, f) == f)
        self.assertTrue(max(f, g) == max(g, f) == g)
        self.assertTrue(g != h)
        self.assertTrue(h < g)
        self.assertTrue(g >= h)
        self.assertTrue(min(f, h) == min(h, f) == h)
        self.assertTrue(max(f, h) == max(h, f) == f)

    def testMixedTypeComparision(self):
        f = Decimal('23.456')
        g = Fraction('23.4562398')
        h = -12.5
        self.assertTrue(f == Fraction('23.456'))
        self.assertTrue(Decimal(h) == h)
        self.assertTrue(Decimal('-12.3') != h)
        self.assertTrue(f != g)
        self.assertTrue(f < g)
        self.assertTrue(g >= f)
        self.assertTrue(min(f, g) == min(g, f) == f)
        self.assertTrue(max(f, g) == max(g, f) == g)
        self.assertTrue(g != h)
        self.assertTrue(h < g)
        self.assertTrue(g >= h)
        self.assertTrue(min(f, h) == min(h, f) == h)
        self.assertTrue(max(f, h) == max(h, f) == f)
        self.assertNotEqual(f, 'abc')
        # following tests raise exception in Python3
        #self.assertTrue(f < 'abc')
        #self.assertTrue(f <= 'abc')
        #self.assertTrue('abc' > f)
        #self.assertTrue('abc' >= f)

    def testAdjustment(self):
        f = Decimal('23.456')
        g = Decimal('23.4562398').adjusted(3)
        h = Decimal('23.4565').adjusted(3)
        self.assertEqual(f.precision, g.precision)
        self.assertEqual(f, g)
        self.assertNotEqual(f, h)
        self.assertEqual(f.adjusted(0), 23)
        self.assertEqual(f.adjusted(-1), 20)
        self.assertEqual(f.adjusted(-5), 0)
        self.assertRaises(TypeError, f.adjusted, 3.7)

    def testQuantization(self):
        f = Decimal('23.456')
        g = Decimal('23.4562398').quantize(Decimal('0.001'))
        h = Decimal('23.4565').quantize(Decimal('0.001'))
        self.assertEqual(f.precision, g.precision)
        self.assertEqual(f, g)
        self.assertNotEqual(f, h)
        self.assertEqual(f.quantize(1), 23)
        self.assertEqual(f.quantize('10'), 20)
        self.assertEqual(f.quantize(_StdLibDecimal(100)), 0)
        f = Decimal(1.4, 28)
        for quant in [Decimal('0.02'), Decimal(3), Fraction(1, 3)]:
            q = f.quantize(quant)
            d = abs(f - q)
            print(f, quant, q, d)
            self.assertTrue(d < quant)
            r = q / quant
            self.assertEqual(r.denominator, 1)
        self.assertRaises(TypeError, f.quantize, complex(5))
        self.assertRaises(TypeError, f.quantize, 'a')

    def testRounding(self):
        self.assertEqual(round(Decimal('23.456')), 23)
        self.assertEqual(round(Decimal('23.456'), 1), Decimal('23.5'))
        self.assertEqual(round(Decimal('2345.6'), -2), Decimal('2300'))
        if sys.version_info.major < 3:
            # In versions before 3.0 round always returns a float
            self.assertEqual(type(round(Decimal('23.456'))), float)
            self.assertEqual(type(round(Decimal('23.456'), 1)), float)
        else:
            # Beginning with version 3.0 round returns an int, if called
            # with one arg, otherwise the type of the first arg
            self.assertEqual(type(round(Decimal('23.456'))), int)
            self.assertEqual(type(round(Decimal('23.456'), 1)), Decimal)
        # test whether rounding is compatible with decimal
        for i in range(-34, 39, 11):
            d1 = _StdLibDecimal(i) / 4
            d2 = Decimal(d1, 2)
            self.assertEqual(round(d1), round(d2))
        for rounding in rounding_modes:
            for i in range(-34, 39, 11):
                e = _StdLibDecimal(i)
                d1 = e / 4
                d2 = Decimal(d1, 2)
                i1 = int(d1.quantize(e, rounding=rounding))
                i2 = int(d2.adjusted(0, rounding=rounding))
                self.assertEqual(i1, i2)

    def testComputation(self):
        f = Decimal('23.25')
        g = Decimal('-23.2562398')
        h = f + g
        self.assertEqual(--f, +f)
        self.assertEqual(abs(g), abs(-g))
        self.assertEqual(g - g, 0)
        self.assertEqual(f + g - h, 0)
        self.assertEqual(f - 23.25, 0)
        self.assertEqual(23.25 - f, 0)
        self.assertTrue(-(3 * f) == (-3) * f == 3 * (-f))
        self.assertTrue((2 * f) * f == f * (2 * f) == f * (f * 2))
        self.assertEqual(3 * h, 3 * f + 3 * g)
        f2 = -2 * f
        self.assertTrue((-f2) / f == f2 / (-f) == -(f2 / f) == 2)
        self.assertEqual(g / f, Fraction(-116281199, 116250000))
        self.assertEqual(2 / Decimal(5), Decimal(2) / 5)
        self.assertRaises(ZeroDivisionError, f.__truediv__, 0)
        self.assertEqual(g // f, -2)
        self.assertEqual(g // -f, 1)
        self.assertEqual(g % -f, h)
        self.assertEqual(divmod(24, f), (Decimal(1, 2), Decimal('.75')))
        self.assertEqual(divmod(-g, f), (1, -h))
        self.assertEqual(f ** 2, f * f)
        self.assertEqual(g ** -2, 1 / g ** 2)
        self.assertEqual(2 ** f, 2.0 ** 23.25)
        self.assertEqual(1 ** g, 1.0)
        self.assertEqual(math.floor(f), 23)
        self.assertEqual(math.floor(g), -24)
        self.assertEqual(math.ceil(f), 24)
        self.assertEqual(math.ceil(g), -23)
        self.assertEqual(round(f), 23)
        self.assertEqual(round(g), -23)

    def testMixedTypeComputation(self):
        f = Decimal('21.456')
        g = Fraction(1, 3)
        h = -12.5
        i = 9
        self.assertEqual(f + g, Fraction(8171, 375))
        self.assertEqual(g + f, Fraction(8171, 375))
        self.assertEqual(f + h, Decimal('8.956'))
        self.assertEqual(h + f, Decimal('8.956'))
        self.assertEqual(f + i, Decimal('30.456'))
        self.assertEqual(i + f, Decimal('30.456'))
        self.assertEqual(f - g, Fraction(7921, 375))
        self.assertEqual(g - f, Fraction(-7921, 375))
        self.assertEqual(f - h, Decimal('33.956'))
        self.assertEqual(h - f, Decimal('-33.956'))
        self.assertEqual(f - i, Decimal('12.456'))
        self.assertEqual(i - f, Decimal('-12.456'))
        self.assertEqual(f * g, Fraction(894, 125))
        self.assertEqual(g * f, Fraction(894, 125))
        self.assertEqual(f * h, Decimal('-268.2', 4))
        self.assertEqual(h * f, Decimal('-268.2', 4))
        self.assertEqual(f * i, Decimal('193.104'))
        self.assertEqual(i * f, Decimal('193.104'))
        self.assertEqual(f / g, Fraction(8046, 125))
        self.assertEqual(g / f, Fraction(125, 8046))
        self.assertEqual(f / h, Decimal('-1.71648'))
        self.assertEqual(h / f, Fraction(-3125, 5364))
        self.assertEqual(f / i, Decimal('2.384'))
        self.assertEqual(i / f, Fraction(125, 298))
        self.assertEqual(f // g, 64)
        self.assertEqual(g // f, 0)
        self.assertEqual(f // h, Decimal(-2, 3))
        self.assertEqual(h // f, Decimal(-1, 3))
        self.assertEqual(f // i, Decimal(2, 3))
        self.assertEqual(i // f, Decimal(0, 3))
        self.assertEqual(f % g, Fraction(46, 375))
        self.assertEqual(g % f, Fraction(1, 3))
        self.assertEqual(f % h, Decimal('-3.544'))
        self.assertEqual(h % f, Decimal('8.956'))
        self.assertEqual(f % i, Decimal('3.456'))
        self.assertEqual(i % f, Decimal(9, 3))
        self.assertEqual(Decimal('0.5') + 0.3,
                         Fraction(14411518807585587, 18014398509481984))
        self.assertEqual(0.3 + Decimal('0.5'),
                         Fraction(14411518807585587, 18014398509481984))
        self.assertEqual(Decimal('0.5') - 0.3,
                         Fraction(3602879701896397, 18014398509481984))
        self.assertEqual(0.3 - Decimal('0.5'),
                         Fraction(-3602879701896397, 18014398509481984))
        self.assertEqual(Decimal(2 ** 32) * 0.3,
                         Decimal('1288490188.7999999523162841796875'))
        self.assertEqual(0.3 * Decimal(2 ** 32),
                         Decimal('1288490188.7999999523162841796875'))
        self.assertEqual(Decimal('0.5') * 0.3,
                         Fraction(5404319552844595, 36028797018963968))
        self.assertEqual(0.3 * Decimal('0.5'),
                         Fraction(5404319552844595, 36028797018963968))
        self.assertEqual(0.3 / Decimal(2),
                         Fraction(5404319552844595, 36028797018963968))
        self.assertEqual(Decimal(2) / 0.3,
                         Fraction(36028797018963968, 5404319552844595))

    def testPickle(self):
        d = Decimal(Decimal(1))
        self.assertEqual(loads(dumps(d)), d)
        d = Decimal(-1, 2)
        self.assertEqual(loads(dumps(d)), d)
        d = Decimal(-37, 100)
        self.assertEqual(loads(dumps(d)), d)
        d = Decimal(sys.maxsize ** 100)
        self.assertEqual(loads(dumps(d)), d)
        d = Decimal(1.111e12)
        self.assertEqual(loads(dumps(d)), d)
        d = Decimal('+21.4')
        self.assertEqual(loads(dumps(d)), d)
        d = Decimal('+1e2')
        self.assertEqual(loads(dumps(d)), d)
        d = Decimal('12345678901234567890e-234')
        self.assertEqual(loads(dumps(d)), d)
        d = Decimal('-1E2')
        self.assertEqual(loads(dumps(d)), d)
        d = Decimal('.23e+2')
        self.assertEqual(loads(dumps(d)), d)
        d = Decimal('+1e-2000')
        self.assertEqual(loads(dumps(d)), d)

    def testFormat(self):
        d = Decimal('1234567890.12345678901234567890')
        loc = locale.getlocale()
        if sys.platform == 'win32':
            locale.setlocale(locale.LC_ALL, 'German_Germany.1252')
        else:
            locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
        pth = os.path.dirname(__file__)
        fn = os.path.join(pth, "format.tests")
        with open(fn) as tests:
            for line in tests:
                formatSpec, result = [s.strip("'")
                                      for s in line.strip().split('\t')]
                if formatSpec:
                    self.assertEqual(format(d, formatSpec), result)
                else:
                    self.assertEqual(format(d), result)
        d = Decimal('0.0038')
        self.assertEqual(format(d), str(d))
        self.assertEqual(format(d, '<.3'), str(d.adjusted(3)))
        self.assertEqual(format(d, '<.7'), str(d.adjusted(7)))
        locale.setlocale(locale.LC_ALL, loc)
        self.assertRaises(ValueError, format, d, ' +012.5F')
        self.assertRaises(ValueError, format, d, '_+012.5F')
        self.assertRaises(ValueError, format, d, '+012.5e')
        self.assertRaises(ValueError, format, d, '+012.5E')
        self.assertRaises(ValueError, format, d, '+012.5g')
        self.assertRaises(ValueError, format, d, '+012.5G')


class PyImplTest(unittest.TestCase, DecimalTest):

    """Testing the Python implementation."""

    def setUp(self):
        global Decimal
        Decimal = _PyDecimal


@unittest.skipIf(platform.python_implementation() != 'CPython',
                 'Skip CImplTest unless running CPython.')
class CImplTest(unittest.TestCase, DecimalTest):

    """Testing the Cython implementation."""

    def setUp(self):
        global Decimal
        Decimal = _CDecimal


if __name__ == '__main__':
    unittest.main()
