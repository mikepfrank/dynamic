# Dynamic
A simple simulator for dynamical systems construed as computations.

## 1. Purpose
Dynamic is a framework for simulating simple models of (nonlinear, chaotic) dynamical systems, for the purpose of investigating to what extent such models can be used as the foundation for new computational paradigms.

## 2. Language
The plan is to initially write Dynamic in Python (3.5.1 Windows 64-bit), although we may eventually port it to C++ for better performance, and perhaps code a parallel version using MPI or OpenMP.

## 3. Visualization
We plan to support a variety of interactive, animated views of the data for visualization and analysis purposes.  Some possibilities for this may include: 

* Plot position/velocity of each coordinate on a 2D plane.  Draw lines between interacting coordinates?
* Plot circuit diagram color-coding node values.

## 4. Statistics
Dynamic can be configured to connect statistics about the trajectories of coordinates of interest in the system, for purposes of analyzing whether computationally meaningful information is contained in the trajectory.

## 5. Key Classes
The plan is for Dynamic to include (at least) the following core classes:

* **FixedPoint** - A class for working with fixed-point numbers with specified precision.  The purpose of using fixed point in this application is to support invertible updates (without rounding).  **NOTE:** Now using the existing class decimalfp.py.

* **SimulationContext** - This structure holds global, constant parameters that apply to the whole simulation such as the timestep (∆*t*).

* **Coordinate** - A generalized-position coordinate or degree of freedom.  Each position also has an associated velocity, an associated effective mass, and associated kinetic and potential energy terms in the system's Hamiltonian.  Positions and velocities are updated on alternate timesteps using a centered-difference algorithm.  A coordinate can be queried as to its value at any given time (in the past or the future), and the simulation will update its state to calculate this.

* **PotentialEnergyTerm** - A potential-energy function of some set of coordinates; a term in the system's Hamiltonian.  This object can calculate its value, as well as the value of its partial derivative with respect to any of its coordinates.

* Classes for implementing particular "gates" as potential energy terms in the Hamiltonian.  More complex types of devices that also include internal state information may eventually be supported.

