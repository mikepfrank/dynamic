Decimal fixed-point arithmetic
==============================

.. automodule:: decimalfp

Class `Decimal`
---------------

.. autoclass:: Decimal
    :members: from_float, from_decimal, from_real,
        precision, magnitude, numerator, denominator, real, imag,
        adjusted, quantize, as_tuple, as_integer_ratio, __hash__,
        __eq__, __lt__, __le__, __gt__, __ge__,
        __abs__, __neg__, __pos__,
        __add__, __radd__, __sub__, __rsub__,
        __mul__, __rmul__, __div__, __rdiv__,
        __truediv__, __rtruediv__, __pow__,
        __floor__, __ceil__, __round__,
        __repr__, __str__, __format__

Rounding modes
--------------

`Decimal` supports all rounding modes defined by the standard library module
`decimal`: ROUND_DOWN, ROUND_UP, ROUND_HALF_DOWN, ROUND_HALF_UP,
ROUND_HALF_EVEN, ROUND_CEILING, ROUND_FLOOR and ROUND_05UP. It uses the
rounding mode set as default in that module.

As shortcut to get or set the rounding mode, the module `decimalfp` provides
the following two functions:

.. autofunction:: get_rounding

.. autofunction:: set_rounding
