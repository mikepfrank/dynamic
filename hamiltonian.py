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

from fixed                          import Fixed
from partialEvalFunc                import PartiallyEvaluatableFunction
from baseDifferentiableFunction     import BaseDifferentiableFunction
from dynamicVariable                import DynamicVariable,DerivedDynamicFunction

# A HamiltonianTerm is a primitive dynamic function (not expressed as
# a sum of other functions) giving a Hamiltonian energy as a function
# of some set of variables.  It should be differentiable with respect
# to all variables.

class HamiltonianTerm(DerivedDynamicFunction):

    # Instance private data members:
    #
    #       inst._varList:List[DynamicVariable]
    #
    #           The list of dynamical variables that the value of this
    #           term depends on.
    #
    #       inst._varIndex:Dict[DynamicVariable,int]
    #
    #           Maps a dynamical variable to its index within our list.
    #           This facilitates fast lookups of particular variables.
    #
    #       inst._function:BaseDifferentiableFunction
    #
    #           The function that computes the value of this term given
    #           values for all of its variables.
    #
    #       inst._partials:Dict[BaseDynamicFunction]
    #
    #           These dynamic functions are the partial derivatives
    #           of this term with respect to its variables.  The key
    #           to this dict is the variable index in [0..nVars-1].

    # This initializer takes a list of the dynamic variables that this
    # term involves, and a differentiable function giving the value of
    # this term (given values of the variables).  The dynamical variables
    # in the <varlist> should correspond (in the same order!) to the
    # arguments to the given function.

    def __init__(inst, varlist:Iterable[DynamicVariable],
                 function:BaseDifferentiableFunction):

            # First do generic initialization for DerivedDynamicFunction instances.
            # This remembers our variable list and our associated evaluation function.

        DerivedDynamicFunction.__init__(inst, varList, function)

            # Construct our map from variables to their indices.

        for index in range(len(varlist)):
            inst._varIndex[varlist[index]] = index

        inst._function = function       # Remember the function.

        inst._partials = dict()         # Initially empty cache of partials.

    # Instance public methods:
    #
    #   .dynPartialDerivWRT(v:DynamicVariable) - Given the identification
    #       of a particular dynamic variable mentioned in this term,
    #       return an object with signature Callable[[int],Fixed] which
    #       is a callable function that, given a point in time t, evaluates
    #       the partial derivative of the term with respect to that
    #       variable at that point in time (given the values that other
    #       variables would have at that point in time).

    def dynPartialDerivWRT(self, v:DynamicVariable) -> DerivedDynamicFunction:

        varIndex = self._varIndex[v]    # Look up this variable's index in our list.

            # We may have previously constructed the dynamic function for
            # this particular partial derivative.  If so, just look it up.

        if varIndex in self._partials:
            return self._partials[varIndex]

            # Ask our BaseDifferentialFunction for its partial derivative
            # with respect to the <varIndex>'th variable.  Note that at this
            # point, this function is still unevaluated.

        partial = self._function.partialDerivWRT(varIndex)

            # Now construct a dynamic function corresponding to this partial
            # derivative and remember it.

        dynPartial = DerivedDynamicFunction(self.varList, partial)
        self._partials[varIndex] = dynPartial

            # Return that dude.

        return dynPartial
            

# For our purposes, a Hamiltonian is most straightforwardly conceived
# as a list of terms, each of which is a function of some variables.
# For convenience, we also have the ability to quickly look up, for
# a variable, what are the terms in the Hamiltonian that include that
# variable.  Also, for each term we should be easily able to obtain
# its partial derivative with respect to any variable.

class Hamiltonian(DerivedDynamicFunction):

    # Private data members:
    #
    #   inst._terms:Set[HamiltonianTerms] - The set of Hamiltonian terms making up this
    #       Hamiltonian.
    #
    #   inst._varTerms:Set[HamiltonianTerm] - Maps variables to the set of terms of
    #       this Hamiltonian that mention them.

    def __init__(inst):

        DerivedDynamicFunction.__init__()   # Initializes ._varList and ._function to null values.
        
        inst._terms = set()         # Initially empty set of terms.
        inst._varTerms = dict()     # Initially empty map from variables to terms.

        inst._function = inst.hamFunction

    def hamFunction(inst):  # Note: No explicit arguments here!
        pass

    # Public member functions:
    #
    #   .addTerm(term:HamiltonianTerm) - Merges the given term to this
    #       Hamiltonian.  Merges its variable list into ours.

    def addTerm(inst, term:HamiltonianTerm):

        if term not in inst._terms:
            
            inst._terms |= {term}

                # Merge the variable list for the new term into that
                # for the overall Hamiltonian.

            inst._varList = list(set(inst._varList) | set(term._varList))

                # For each of the new term's variables, remember that
                # this term is in the set of terms that references
                # that variable.

            for var in term._varList:

                if term in inst._varTerms:
                        # Get the set of terms already associated w. this variable.
                    varTerms = set(inst._varTerms[var]) 
                else:
                    varTerms = set()    # Empty set of terms already associated with that variable.

                varTerms |= {term}     # Union the new term into the variable's set.

                inst._varTerms[var] = varTerms      # Store it back in the dict.

            # Since our set of variables and terms will in general have changed,
            # recalculate our 

        inst.recalculateFunction()
            
    
    #
    #   .dynPartialDerivWRT(v:DynamicVariable) - Given the identification
    #       of a particular dynamic variable mentioned in this Hamiltonian,
    #       return a DerivedDynamicFunction object which is a callable
    #       function that, given a point in time t, evaluates
    #       the partial derivative of the Hamiltonian with respect to that
    #       variable at that point in time (given the values that other
    #       variables would have at that point in time).
    #
    #       To implement this efficiently, we use a map to keep track of the
    #       list of terms that mention a given variable.
    #   
    #   .termsContaining(v:DynamicVariable) - Returns a list of all the
    #       terms within this Hamiltonian that involve the given variable.
    #
    
    def partialDerivWRT(self, v:DynamicVariable):

        relevantTerms = self.termsContaining(v)

        

        def termSummer(timestep:int):
            cumulativeSum = Fixed(0)            
            for term in self.termsContaining(v):
                partial = term.partialDerivWRT(v)
                cumulativeSum = cumulativeSum + partial(timestep)
            return cumulativeSum
            
        return termSummer


    def termsContaining(self, v:DynamicVariable):

        if self._varTerms.has_key(v):
            return self._varTerms[v]
        else:
            return []
