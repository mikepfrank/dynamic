# Dynamic

Dynamic is a simple simulator for dynamical systems construed as computations.

## 1. Purpose

Dynamic is a framework for simulating simple models of (nonlinear, 
generally chaotic) dynamical systems, for the purpose of investigating 
to what extent such models can be used as the foundation for new 
computational paradigms.

## 2. Approach

Dynamic provides for the construction and simulation of arbitrary
networks (undirected graphs) of canonical coordinates, coupled to
their neighbors by arbitrary Hamiltonian interaction terms.  The
simulation method does discrete time-domain integration using a 
centered-difference leapfrog-style update rule, alternating between 
position and momentum coordinates.  Coordinates are represented in
fixed point.  Together the centered-difference update rule and the
fixed-point coordinates ensure complete bit-level reversibility of
the simulation, ensuring that the simulated time-evolution does not 
destroy entropy.

## 3. Language

The initial prototype implementation of Dynamic is being written 
in Python (3.5.1) and tested on Windows (8.1 Professional, 64-bit), 
although we may eventually port it to C++ for better performance, 
and/or perhaps code a parallel version using MPI and/or OpenMP.

## 4. Visualization

We plan to support a variety of interactive, animated views of the 
data for visualization and analysis purposes.  Some possibilities 
for this may include: 

 * Plot position/velocity (phase portrait) of each coordinate on 
		a 2D plane.  Animate fading trails showing coordinate history.

 * Plot circuit diagram color-coding node values.

## 5. Statistics

Dynamic will be able to be configured to connect important statistics 
about the trajectories of coordinates of interest in the system, 
for purposes of analyzing whether computationally meaningful 
information is contained in the trajectory.

## 6. Software Architecture

For notes on the software architecture of Dynamic, see the Notes.txt file.