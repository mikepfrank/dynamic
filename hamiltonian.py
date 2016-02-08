#/------------------------------------------------------------------------------
#|
#|      File name:      dynamic/hamiltonian.py      [Python module source code]
#|
#|      Synopsis:
#|      ---------
#|
#|          This module provides various classes related to a
#|          Hamiltonian formulation of mechanics.
#|
#|          The most important class is PotentialEnergyTerm,
#|          which defines a class of potential energy function
#|          that depends on a set of generalized coordinates
#|          (their generalized positions, but not their
#|          velocities).  The partial derivatives of the
#|          potential with respect to the position variables
#|          can be retrieved in order to extract force
#|          components, which (together with those for other
#|          potential energy terms in which a given coordinate
#|          appears) are used to update velocity variables.
#|
#|          Additional classes will be defined as needed.
#|
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

from    decimalfp       import  *

import  coordinate

class PotentialEnergyTerm:
    
    def __init__():     pass

    # Instance attributes (once fully initialized):
    # ---------------------------------------------
    #
    #   .coordinates - A tuple of Coordinate objects.  These are
    #                   the degrees of freedom that appear in this
    #                   term of the system's Hamiltonian.
    #
    #   .function - A lambda object that takes N numeric arguments
    #                   (where N is the length of the list of
    #                   .coordinates) and returns the value of the
    #                   energy function at those coordinates.
    #
    #   .partialDerivs - A tuple of N lambdas, where N is the length
    #                   of the list of .coordinates).  The lambda
    #                   for the i'th coordinate takes N arguments
    #                   (current values of the N coordinates) and
    #                   returns the value of the partial derivative
    #                   of .function with respect to the i'th coor-
    #                   dinate, at the given coordinates.
    #
    #
    # Public instance methods (available after initialization):
    # ---------------------------------------------------------
    #
    #   .evaluate() - First, ensures that all constituent coordinates
    #                   have been brought up to the same time point
    #                   (advancing lagging ones as necessary).  Then
    #                   evaluates the .function at those coordinates
    #                   and returns the result.
    #
    #   .partial_wrt() - First, ensures that all constituent coordinates
    #                       have been brought up to the same time point
    #                       advancing lagging ones as necessary).  Then,
    #                       evaluates the partial derivative of .function
    #                       with respect to the given Coordinate at that
    #                       time point and returns the result.
    #
    #                   

