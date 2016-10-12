# Dynamic simulator package (`dynamic/src/simulator/`).

This directory defines the `simulator` package of the Dynamic system, 
which implements the core simulation framework.  It deals at the level
of canonical dynamical coordinates interrelated via Hamiltonian 
interaction functions and updated according to Hamilton's equations.

## 1. Module hierarchy.

The dependency diagram of modules within this package is roughly as follows
(indirect dependencies may not all be shown):

                 _______________
    Package     /               \
    module:     |   simulator   |
                | (__init__.py) |
                \_______________/
    Modules in      |         | 
    package:        |         V 
                    |       simmor.py
                    |               \
                    V                \
              dynamicCoordinate.py    \
                        |              \
                        V               \
             hamiltonianVariable.py      \
                        |                 \
                        V                 |
                 hamiltonian.py           |
                        |                 |
                        V                 |
        differentiableDynamicFunction.py  |
                        |                 /
                        V                /
             derivedDynamicFunction.py  /
                        |              /
                        V             /
                dynamicVariable.py   /
                    |       |       /
                    V       |      /
      dynamicFunction.py    |      |
                            V      V
                    simulationContext.py

The `simulator` package uses the `functions` package, as well as the 
top-level module `fixed.py`.

The `simulator` package is used by the `network` package as well as 
by the main application script `dynamic-demo.py`.

## 2. Working modules.

The following modules have been tested and are part of the
current system.  Below, they are presented in order from 
lowest-level to highest-level (later ones depend on earlier 
ones.)

### 2.1. Simulation context module (`simulationContext.py`).

This module defines global properties that apply to the entire 
simulation, e.g., the time step size.

### 2.2. Dynamic functions module (`dynamicFunction.py`).

This module defines classes for dynamic functions, which are 
functions of time whose value at a given time is computed by
first stepping the simulation forwards or backwards as needed
to arrive at that time, and then evaluating the function.

### 2.3. Dynamic variables module (`dynamicVariable.py`).

This module defines a class for dynamic variables, which can 
step their own value forwards or backwards in time as needed 
by applying a time-derivative function.  The core 
centered-difference state-updating algorithm for time 
integration is here.

### 2.4. Derived dynamic functions module (`derivedDynamicFunction.py`).

This module defines a class for derived dynamic functions, that is,
dynamic functions of one or more dynamic variables, which are evaluated
by stepping those variables forwards or backwards and time as needed,
and then evaluating the function.

### 2.5. Differentiable dynamic functions module (`differentiableDynamicFunction.py`).

This module defines a class for differentiable dynamic functions,
which are derived dynamic functions that are also differentiable
with respect to any of their variables, and whose partial derivative
with respect to any given variable is itself another derived dynamic 
function.

### 2.6. Hamiltonian module (`hamiltonian.py`).

This module defines classes for individual Hamiltonian terms, as 
well as general Hamiltonian functions which may be expressed as
a sum of terms.

### 2.7. Hamiltonian variable module (`hamiltonianVariable.py`).

This module defines a class for Hamiltonian variables, which are
dynamic variables that keep track of the Hamiltonian that they are 
associated with, and that can infer their time-derivative from it.

### 2.8. Dynamic coordinate module (`dynamicCoordinate.py`).

This module defines a class for dynamical coordinates, which means
canonical coordinate pairs consisting of a generalized position
coordinate and an associated generalized momentum coordinate.  The 
'leapfrog'-style approach for time integration (alternately
updating the position and momentum coordinates) is implemented here.

### 2.9. Simulator object module (`simmor.py`).

This module (still experimental) defines a top-level class Simmor 
to manage the entire simulation.

### 2.10. Package initialization module (`__init__.py`).

This module is automatically loaded when the package is first accessed,
and it performs initialization operations associated with the package.
