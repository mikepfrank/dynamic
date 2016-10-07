# Dynamic Boolean package (`dynamic/src/boolean/`).

This directory defines the `boolean` package of the Dynamic system, which
provides Dynamic-style implementations of standard Boolean logic gates.
It depends on the `..network` and `..function` packages.

## 1. Module hierarchy.

The dependency diagram of modules within this package is as follows:

				 _______________
	Package 	/               \
	module:		|    boolean    |
				| (__init__.py) |
				\_______________/
	Modules in			|
	package:			|
						V
				dynamicXORGate.py
				dynamicORGate.py
				dynamicANDGate.py
				dynamicNOTGate.py

Overall the `boolean` package uses the `network` package.
				
The `boolean` package is used by the `examples` package.

## 2. Working modules.

The following modules have been tested and are part of the current system.

### 2.1. Dynamic NOT gate module (`dynamicNOTGate.py`).

### 2.2. Dynamic AND gate module (`dynamicANDGate.py`).

### 2.3. Dynamic OR gate module (`dynamicORGate.py`).

### 2.4. Dynamic XOR gate module (`dynamicXORGate.py`).

### 2.5. Package initialization module (`__init__.py`).

This module is automatically loaded when the package is first accessed,
and it performs initialization operations associated with the package.
