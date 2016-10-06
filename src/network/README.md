# Dynamic network package (`dynamic/src/network/`).

This directory defines the `network` package of the Dynamic system, which
allows creating networks of Dynamic nodes linked to Dynamic components.
It depends on the `..simulator` package.

## 1. Working modules.

The following modules have been tested and are part of the current system.

### 1.1. Links-and-ports module (`linkport.py`).

This module defines classes that allow linking nodes to ports of components.

### 1.2. Dynamic node module (`dynamicNode.py`).

This module defines a class for nodes in a Dynamic network.  A node holds one
or more (currently just one) dynamical state variables.

### 1.3. Dynamic component module (`dynamicComponent.py`).

This module defines a class for components of a Dynamic network.  A component
links one or more nodes together via Hamiltonian interaction terms.  Generally
components might also have internal state variables, but they don't yet. (We
can always extend the classes later for this purpose.)

### 1.4. Dynamic one-terminal component module (`dynamicOneTerminalComponent.py`).

Currently just used by the ..examples.rangeBinder module, this component
class involves one-terminal components whose incident node is not necessarily
to be thought of as an "output."

### 1.5. Dynamic one-terminal gate module (`dynamicOneTerminalGate.py`).

### 1.6. Dynamic two-terminal gate module (`dynamicTwoTerminalGate.py`).

### 1.7. Dynamic three-terminal gate module (`dynamicThreeTerminalGate.py`).

The above three modules define various sizes of generic component classes
called "gates" in which one terminal is conventionally designated as an
"output" terminal, and the others are implicitly "input" terminals.  Thus, 
the one-terminal "gate" has 0 inputs, the two-terminal gate has 1 input, 
and the three-terminal gate has 2 inputs.  

Maybe the abstraction here could be improved (e.g. have one "gate" class 
that is parameterized by the number of terminals), but this is fine for now.

### 1.8. Dynamic network module (`dynamicNetwork.py`).

This module defines a class for Dynamic networks.  Essentially a network is
just a set of nodes and a set of components, with an associated simulation
context.
