# Dynamic examples package (`dynamic/src/examples/`).

This directory defines the `examples` package of the Dynamic system.
It depends on the `..boolean` package.

## 1. Module hierarchy.

The dependency diagram of modules within this package is as follows:
				 _______________
	Package 	/               \
	module:		|    examples   |
				| (__init__.py) |
				\_______________/
	Modules in		|		|
	package:		|		|
					|		V
					|	exampleNetworks.py
					|		|
					V		V
		 rangeBinder.py	  dynamicMemCell.py
				
The `examples` package uses the `boolean` and `function` packages.
				
The `examples` package is used by the main application script `dynamic-demo.py`.

## 2. Working modules.

The following modules have been tested and are part of the current system.

### 2.1. Range binder module (`rangeBinder.py`).

This module defines a simple one-terminal component that imposes a quartic
double-well potential that keeps a node's value from wandering too far away
from 0 or 1.  Not currently used.

### 2.2. Dynamic memory cell module (`dynamicMemCell.py`).

This module defines a simple one-terminal component that provides a quadratic
potential-well to bias the output node's value to a desired level (usually 0 
or 1).  This component is used extensively by the `exampleNetworks` module.

### 2.3. Example networks module (`exampleNetworks.py`).

This module defines a variety of simple example networks biased by fixed
memory cells, from a single memory cell by itself, up through a full adder.
Currently used by the demo script (`../dynamic-demo.py`).

### 2.4. Package initialization module (`__init__.py`).

This module is automatically loaded when the package is first accessed,
and it performs initialization operations associated with the package.

## 3. Unfinished modules.

### 3.1. Half-adder module (`halfAdder.py`).

This module is intended to define a half-adder subnetwork that can be used 
like a component, as a piece within a larger network.  It is not yet
finished, but in the meantime there is a standalone half-adder network class
in `exampleNetworks.py`.

### 3.2. Full adder module (`fullAdder.py`).

This module is intended to define a full adder subnetwork that can be used 
like a component, as a piece within a larger network.  It is not yet
finished, but in the meantime there is a standalone full adder network class
in `exampleNetworks.py`.
