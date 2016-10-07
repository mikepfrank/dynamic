# Dynamic network package (`dynamic/src/network/`).

This directory defines the `network` package of the Dynamic system, which
allows creating networks of Dynamic nodes linked to Dynamic components.
It depends on the `..simulator` package.

## 1. Module hierarchy.

The dependency diagram of modules within this package is roughly as follows
(indirect dependencies may not all be shown):
				 _______________
	Package 	/               \
	module:		|    network    |
				| (__init__.py) |
				\_______________/
	Modules in		|		  |
	package:		|		  |
					V		  |
		dynamicNetwork.py	  V
					|		dynamicThreeTerminalGate.py
					|		dynamicTwoTerminalGate.py
					|		dynamicOneTerminalGate.py
					|		dynamicOneTerminalComponent.py
					|		  |
					V		  V
				dynamicComponent.py
					    |
						V
				   linkport.py
						|
						V
				  dynamicNode.py
				
					
The `network` package is used by the higher-level `boolean` and 
`examples` packages.

## 2. Working modules.

The following modules have been tested and are part of the current system.

### 2.1. Dynamic node module (`dynamicNode.py`).

This module defines a class for nodes in a Dynamic network.  A node holds one
or more (currently just one) dynamical state variables.

### 2.2. Links-and-ports module (`linkport.py`).

This module defines classes that support linking nodes to ports of components.

### 2.3. Dynamic component module (`dynamicComponent.py`).

This module defines a class for components of a Dynamic network.  A component
links one or more nodes together via Hamiltonian interaction terms.  Generally
components might also have internal state variables, but they don't yet. (We
can always extend the classes later for this purpose.)

### 2.4. Dynamic one-terminal component module (`dynamicOneTerminalComponent.py`).

Currently just used by the ..examples.rangeBinder module, this component
class involves one-terminal components whose incident node is not necessarily
to be thought of as an "output."

### 2.5. Dynamic one-terminal gate module (`dynamicOneTerminalGate.py`).

### 2.6. Dynamic two-terminal gate module (`dynamicTwoTerminalGate.py`).

### 2.7. Dynamic three-terminal gate module (`dynamicThreeTerminalGate.py`).

The above three modules define various sizes of generic component classes
called "gates" in which one terminal is conventionally designated as an
"output" terminal, and the others are implicitly "input" terminals.  Thus, 
the one-terminal "gate" has 0 inputs, the two-terminal gate has 1 input, 
and the three-terminal gate has 2 inputs.  

Maybe the abstraction here could be improved (e.g. have one "gate" class 
that is parameterized by the number of terminals), but this is fine for now.

### 2.8. Dynamic network module (`dynamicNetwork.py`).

This module defines a class for Dynamic networks.  Essentially a network is
just a set of nodes and a set of components, with an associated simulation
context.

### 2.9. Package initialization module (`__init__.py`).

This module is automatically loaded when the package is first accessed,
and it performs initialization operations associated with the package.
