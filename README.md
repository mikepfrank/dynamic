![Dynamic logo, fractal version](/artwork/dynamix2.jpg "Dynamic logo - fractal version")

# Dynamic repository (`dynamic/`).

Dynamic is a simple simulator for dynamical systems construed as 
computations.  See the [project homepage](https://cfwebprod.sandia.gov/cfdocs/CompResearch/templates/insert/softwre.cfm?sw=56 "Dynamic homepage")
for links to related publications.

## 1.  Copyright Notice and Licensing Terms

The following information may also be found in the file LICENSE.txt.

Except as stated below, all files in this repository are Copyright 
©2017 Sandia Corporation.  Under the terms of Contract 
DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government 
retains certain rights in this software.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated  documentation  files  (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

Certain third-party software is included in this package and carries
its own separate copyright and licensing terms.  See the file
NOTICE.txt for details.
    
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN  AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## 2.  Version and Status

The present version number designation of Dynamic is 0.1 (alpha).
The status of this software should be considered PRE-RELEASE.  It 
is still in early development.  User-friendly visualization and 
configuration features have still not been implemented.

## 3.  Purpose

Dynamic is a framework for simulating simple models of (conservative, 
nonlinear, generally chaotic) dynamical systems, for the purpose of 
investigating to what extent such models can be used as the 
foundation for new computational paradigms.

## 4.  Approach

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

## 5.  Language

The initial prototype implementation of Dynamic is being written 
in Python (3.5.1) and tested on Windows (8.1 Professional, 64-bit), 
although we may eventually port it to C++ for better performance, 
and/or perhaps code a parallel version using MPI and/or OpenMP.

## 6.  Visualization

We plan to support a variety of interactive, animated views of the 
data for visualization and analysis purposes.  Some possibilities 
for this may include: 

 * Plot position/velocity (phase portrait) of each coordinate on 
		a 2D plane.  Animate fading trails showing coordinate history.
          Plot mean/deviation of coordinate values.

 * Plot circuit diagram color-coding node values.  Overlay inferred 
          digital values?

The present status of the development of the visualization 
capabilities is:  A window is created for visualization purposes,
but nothing is displayed in it yet.  More work is needed...
          
## 7.  Statistics

Dynamic will be able to be configured to connect important statistics 
about the trajectories of coordinates of interest in the system, 
for purposes of analyzing whether computationally meaningful 
information is contained in the trajectory.

Presently, the demo applications calculates and displays mean values 
of the generalized position coordinate of each node.

## 8.  Software Architecture

For notes on the software architecture of Dynamic, see the docs/Notes.txt file.

## 9.  File Hierarchy

Contents of the '`dynamic/`' repository are as follows:

### 9.1.  Artwork subdirectory ([`artwork/`](artwork "artwork/ subdirectory")).

Contains source files and high-resolution reference versions of graphic artwork
for the Dynamic system (splash pages, logos, etc.).

### 9.2.  Batch subdirectory ([`batch/`](batch "batch/ subdirectory")).

Contains MS-DOS style batch (.BAT) files to facilitate working with the source tree
in Windows environments.

### 9.3.  Data subdirectory ([`data/`](data "data/ subdirectory")).

Contains various raw output data from the simulation as well as Excel workbooks.

### 9.4.  Documentation subdirectory ([`docs/`](docs "docs/ subdirectory")).

Contains miscellaneous notes and other documentation.

### 9.5.  Log subdirectory ([`log/`](log "log/ subdirectory")).

This directory is initially empty and exists solely to be the location
where log files will be written.

### 9.6.  Main source file hierarchy ([`src/`](src "src/ subdirectory")).

Current source file tree.

### 9.7.  Test directory ([`test/`](test "test/ subdirectory")).

Auxilliary source files for testing.

### 9.8.  Copyright/license files ([`LICENSE.txt`](LICENSE.txt "LICENSE.txt file"), [`NOTICE.txt`](NOTICE.txt "NOTICE.txt file")).

The main copyright/license file is `LICENSE.txt`.  An additional 
notice relevant to incorporated third-party software is in `NOTICE.txt`.

### 9.9. README file (`README.md`).

This file.