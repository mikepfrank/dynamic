#|==============================================================================
#|                                  TOP OF FILE
#|
#|      File name:  circuitViewer.py                [Python module source file]
#|
#|      Description:
#|
#|              This Python module provides a GUI for visualization of
#|              a dynamic circuit, i.e. a network of interacting dynamic
#|              elements.  The state of each dynamic element is visual-
#|              ized via a set of phase diagrams, one for each general-
#|              ized coordinate making up the state of the element.
#|              Within each phase diagram, the state is plotted in two
#|              dimensions using the position x and velocity v of the
#|              coordinate.  The point representing the present state is
#|              animated and a gradually-fading trail illustrates the
#|              dynamical history of the coordinate.  The network
#|              structure is illustrated as a graph with links between
#|              nodes (representing dynamic elements) and icons (repre-
#|              senting interactions).  For interactions implementing
#|              logic gates or other circuit elements, standard icons
#|              are used.  Some elements (such as memristors) can have
#|              internal state variables, and a different representation
#|              is used for these in which a node (representing the
#|              internal dynamical state variables) is illustrated
#|              inside the icon representing the element.
