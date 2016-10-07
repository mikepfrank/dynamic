# Dynamic functions package (`dynamic/src/functions/`).

This directory defines the `functions` package of the Dynamic system, 
which is a low-level package that provides a variety of classes of
function objects that support differentiation operations.  Please note 
that the function classes defined in this package are lower-level 
objects than the differentiable *dynamic* function class defined as 
part of the simulator package.  

## 1. Module hierarchy.

The dependency diagram of modules within this package is as follows.		
					 _______________
	Package 		/               \
	module:		 	|   functions   |
					| (__init__.py) |
					\_______________/
	Modules in			|		  |
	package:			|		  |
						V		  V
		doubleWellFunction.py	dynamicBiasFunction.py 
						|		kineticEnergyFunction.py 
						|			|
						V			V
			quarticFunction.py 	quadraticFunction.py 
						|			|
						V			V
				unaryDifferentiableFunction.py
										|
	binaryDifferentiableFunction.py		|
	ternaryDifferentiableFunction.py	|
						|				|
						V				V
					differentiableFunction.py

Besides standard Python libraries, the `functions` only uses the 
top-level `logmaster.py` module.
					
The `functions` package is used by the `simulator` package as well as 
by the higher-level `boolean` and `examples` packages.
				
## 2. Working modules.

The following modules have been tested and are part of the
current system.  Below, they are presented in order from 
lowest-level to highest-level (later ones depend on earlier 
ones.)

### 2.1. Differentiable function module (`differentiableFunction.py`).

This module defines an abstract base class for functions that 
support differentiation operations.

### 2.2. Unary differentiable function module (`unaryDifferentiableFunction.py`).

### 2.3. Binary differentiable function module (`binaryDifferentiableFunction.py`).

### 2.4. Ternary differentiable function module (`ternaryDifferentiableFunction.py`).

The above three modules define subclasses of the base differentiable-function class 
that are specific for functions of one, two, and three variables respectively.

### 2.5. Linear function module (`linearFunction.py`).

### 2.6. Quadratic function module (`quadraticFunction.py`).

### 2.7. Quartic function module (`quarticFunction.py`).

The above three modules define subclasses of the unary differentiable function class 
that are specific to first-order, second-order, and fourth-order polynomial functions
respectively.  Possibly this could have been done in a more abstract way, by defining
a general class for polynomials of any natural order N, and then parameterizing it 
with the specific value of the order, but this is fine for the moment.

### 2.8. Kinetic energy function module (`kineticEnergyFunction.py`).

This module defines a subclass of quadratic functions that gives the 
usual nonrelativistic expression for kinetic energy in terms of a 
generalized velocity variable.

### 2.9. Dynamic bias function module (`dynamicBiasFunction.py`).

This module defines a subclass of quadratic functions that gives a 
potential energy function whose minimum lies at a given "bias" value 
of the input generalized-position variable.

### 2.10. Double well function module (`doubleWellFunction.py`).

This module defines a subclass of quartic functions that gives a 
common form for a double-well potential defined as the product of 
two quadratic potentials with minima at different coordinate values.

### 2.11. Package initialization module (`__init__.py`).

This module is automatically loaded when the package is first accessed,
and it performs initialization operations associated with the package.

