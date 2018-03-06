# Dynamic main source tree (`dynamic/src/`).

This directory is the root of the Python package hierarchy for the Dynamic project.
It contains the demo script `dynamic-demo.py`, several top-level modules, and
subdirectories for the various larger packages making up the simulation.

## 1. Software architecture.

A rough picture of the software architecture is shown below (not including standard
Python modules used).  Subsequent sections of this file describe the parts of this
diagram.  See the `README.md` files within individual packages for further detail.

        
    Application script:        dynamic-demo.py
                                 |         |
                               __/         \______
    Packages:                 /                   \
                             /   ___________       \
                            /   /           \       \
                            |   | examples  |<--+    \
                            |   \___________/   |     \
                            |         |         |      \
                            |    _____V_____    |      |
                            |   /           \   |      |
                            |   |  boolean  |   |      |
                            |   \___________/   |      |
                            |         |         |      |
                            |    _____V_____    |      |
                            |   /           \   /      |
                            |   |  network  |  /       |
                            |   \___________/ /        |
                            |         |      /         |
                            |    _____V_____/          |
                            |   /           \          |
                            +-->| simulator |          |
                                \___________/          |
                                /     |     \          |
                               / _____V_____ \       __V__
                              / /           \ \     /     \
                              | | functions | |     | gui |
                              | \___________/ |     \_____/
                              V               V
    Top-level              fixed.py   partialEvalFunc.py
        modules:                  |        |
                                  V        V
                                 logmaster.py
                                      |
                                      V
                                  appdefs.py 

## 2. Application scripts.

These top-level scripts (currently there is just one) implement the complete
standalone Python applications that are provided as part of the Dynamic system
that the user can execute.  (On Windows platforms, we recommend using the batch
files provided in `..\bat\` to work with the application script.)

### 2.1. Main demo script (`dynamic-demo.py`).

This is the main application provided for demonstration and testing purposes.
Currently, this just creates an example network (full adder) and simulates
it for a fixed number of time steps, producing diagnostic output to the text 
console.  It depends on the `logmaster`, `gui` and `simulation` packages.

## 3. Package subdirectories.

All of these packages depend on the `logmaster` top-level module.  They are 
listed here roughly in order from highest-level to lowest-level.

### 3.1. Examples package (`examples/`).

This package defines some specialized example components (`RangeBinder`, 
`MemCell`) and several complete example networks such as a half-adder
and full adder.  Depends on the `boolean`, `network`, and `functions`
packages.

### 3.2. Boolean logic package (`boolean/`).

This package defines Dynamic versions of several standard Boolean logic gates
(currently NOT, AND, OR, XOR).  Depends on the `network` and `functions` 
packages.

### 3.3. Network package (`network/`).

This package provides a framework for constructing networks of nodes linked
to components, wherein the nodes incorporate dynamical state variables, and 
the components introduce interactions between the nodes.  Depends on the 
`simulator` package.

### 3.4. Simulator package (`simulator/`).

This package implements the core of the simulation framework.  It allows 
creating canonical coordinates (generalized position/momentum pairs) that
are updated according to Hamiltonian functions expressed as sums of terms.
Depends on the `functions` package and the `fixed` module.  Also refers 
upwards to the `examples` package.

### 3.5. Functions package (`functions/`).

This low-level package defines various classes of differentiable functions.

### 3.6. GUI package (`gui/`).

This package (still under construction) will provide an interactive graphical 
user interface featuring animated visualizations.

## 4. Top-level modules.

These modules live in top level source directory for the Dynamic project 
and have not yet been moved into packages.

### 4.1. Fixed-point arithmetic module (`fixed.py`).

A simple module providing fixed-point arithmetic with 9 decimal places of
precision.  This makes it easy to ensure state updates are bit-reversible.
Referenced from several places in the simulator.

### 4.2. Partially-evaluatable function module (`partialEvalFunc.py`).

This module allows defining "partially-evaluatable functions" whose 
arguments can be supplied incrementally, rather than all at once.  (This 
is actually not used in the simulator in any particularly essential way 
at the moment, and could be removed if necessary.)  It is currently 
referenced by the derivedDynamicFunction.py module in the simulator 
package.

### 4.3. Logging facility (`logmaster.py`).

A general logging framework to aid in debugging.  This will be particularly
essential when debugging  multithreaded GUI-based applications.

### 4.4. Application definitions (`appdefs.py`).

This file (expected by the logmaster module) defines some constants naming
the overall software system (`Dynamic`) and the main application component
of that system (`Dynamic.demo`).

