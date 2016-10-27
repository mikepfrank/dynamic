# Dynamic repository (`dynamic/`).

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
          Plot mean/deviation of coordinate values.

 * Plot circuit diagram color-coding node values.  Overlay inferred 
          digital values?

## 5. Statistics

Dynamic will be able to be configured to connect important statistics 
about the trajectories of coordinates of interest in the system, 
for purposes of analyzing whether computationally meaningful 
information is contained in the trajectory.

## 6. Software Architecture

For notes on the software architecture of Dynamic, see the docs/Notes.txt file.

## 7. File Hierarchy

Contents of the 'dynamic' repository are as follows:

### 7.1. Batch subdirectory (`batch/`).

Contains MS-DOS style batch (.BAT) files to facilitate working with the source tree
in Windows environments.

### 7.2. Data subdirectory (`data/`).

Contains various raw output data from the simulation as well as Excel workbooks.

### 7.3. Documentation subdirectory (`docs/`).

Contains miscellaneous notes and other documentation.

### 7.4. Log subdirectory (`log/`).

This directory is initially empty and exists solely to be the location
where log files will be written.

### 7.5. Old source subdirectory (`old/`).

Old source files; no longer used.  Deprecated; to be deleted.

### 7.6. Old logs subdirectory (`old-logs/`).

Old log files from test runs; no longer needed.  Can be deleted.

### 7.7. Main source file hierarchy (`src/`).

Current source file tree.

### 7.8. Test directory (`test/`).

Auxilliary source files for testing.

### 7.9. README file (`README.md`).

This file.