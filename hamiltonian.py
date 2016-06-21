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
#|          The main class is Hamiltonian, and its instances
#|          are conceived as lists of HamiltonianTerms, which
#|          may individually involve one or more Variables.
#|          The Hamiltonian can give us its partial derivative
#|          with respect to any of these Variables.
#|
#|          Typically, we build up a Hamiltonian describing
#|          a complex system's dynamics by adding terms to it
#|          one at a time, as needed.
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

from typing import Callable,Iterable

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
    #   .energyFunction - A differentiable function representing
    #                   how the potential energy depends on the
    #                   coordinate values.  Should be a subclass
    #                   of BaseDifferentiableFunction.
    
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

# A HamiltonianTerm is a primitive function (not expressed as a sum of
# other functions) giving a Hamiltonian energy as a function of some set
# of variables.  It should be differentiable with respect to all variables.

class HamiltonianTerm:

    # This initializer takes a list of the dynamic variables that this
    # term involves, and a differentiable function giving the value of
    # this term (given values of the variables).

    def __init__(inst, varlist:Iterable[DynamicVariable],
                 function:Callable[Iterable[Fixed],Fixed]):

        

# For our purposes, a Hamiltonian is most straightforwardly conceived
# as a list of terms, each of which is a function of some variables.
# For convenience, we also have the ability to quickly look up, for
# a variable, what are the terms in the Hamiltonian that include that
# variable.  Also, for each term we should be easily able to obtain
# its partial derivative with respect to any variable.

class Hamiltonian:

    # Public member functions:
    #
    #   .partialDerivWRT(v:DynamicVariable) - Given the identification
    #       of a particular dynamic variable mentioned in this Hamiltonian,
    #       return an object with signature Callable[[int],Fixed] which
    #       is a callable function that, given a point in time t, evaluates
    #       the partial derivative of the Hamiltonian with respect to that
    #       variable at that point in time (given the values that other
    #       variables would have at that point in time).
    #
    #       To implement this efficiently, we pre-associate variables with
    #
    #   .termsContaining(v:DynamicVariable) - Returns a list of all the
    #       terms within this Hamiltonian that involve the given variable.
    #

    def partialDerivWRT(self, v:DynamicVariable):

        return lambda timestep:int:

            cumulativeSum = Fixed(0)
            
            foreach term in self.termsContaining(v):

                partial = term.partialDerivWRT(v)

                cumulativeSum = cumulativeSum + partial(timestep)

            return cumulativeSum

    def termsContaining(self, v:DynamicVariable):

        
