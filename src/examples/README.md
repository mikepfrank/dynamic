# Dynamic examples package (`dynamic/src/examples/`).

This directory defines the `examples` package of the Dynamic system.

## 1. Working modules.

The following modules have been tested and are part of the current system.

### 1.1. Range binder module (`rangeBinder.py`).

This module defines a simple one-terminal component that imposes a quartic
double-well potential that keeps a node's value from wandering too far away
from 0 or 1.  Not currently used.

### 1.2. Dynamic memory cell module (`dynamicMemCell.py`).

This module defines a simple one-terminal component that provides a quadratic
potential-well to bias the output node's value to a desired level (usually 0 
or 1).  This component is used extensively by the `exampleNetworks` module.

### 1.3. Example networks module (`exampleNetworks.py`).

This module defines a variety of simple example networks biased by fixed
memory cells, from a single memory cell by itself, up through a full adder.
Currently used by the demo script (`../dynamic-demo.py`).

## 2. Unfinished modules.

### 2.1. Half-adder module (`halfAdder.py`).

This module is intended to define a half-adder subnetwork that can be used 
like a component, as a piece within a larger network.  It is not yet
finished, but in the meantime there is a standalone half-adder network class
in `exampleNetworks.py`.

### 2.2. Full adder module (`fullAdder.py`).

This module is intended to define a full adder subnetwork that can be used 
like a component, as a piece within a larger network.  It is not yet
finished, but in the meantime there is a standalone full adder network class
in `exampleNetworks.py`.
