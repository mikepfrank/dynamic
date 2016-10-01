# differentiableDynamicFunction.py

from typing import Callable,Iterable,Iterator,Set

import logmaster; from logmaster import *
logger = getLogger(logmaster.sysName + '.simulator')
    # The dynamicVariable module is part of our core simulation component.

from differentiableFunction import BaseDifferentiableFunction
from dynamicVariable        import DynamicVariable
from derivedDynamicFunction import DerivedDynamicFunction

# A DifferentiableDynamicFunction is a DerivedDynamicFunction
# (derived from a set of DynamicVariables) that also sports the
# feature of being able to return, for any one of those variables,
# another DerivedDynamicFunction which represents the partial
# derivative of the original function with respect to the variables.

class DifferentiableDynamicFunction(DerivedDynamicFunction):

    # Instance public data members:
    #
    #       inst.name:str  -  A human-readable name of this function, as a string.
    #
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
    #           (Inherited from DerivedDynamicFunction.)
    #
    #           The function that computes the value of this term given
    #           values for all of its variables.
    #
    #       inst._partials:Dict[BaseDynamicFunction]
    #
    #           These dynamic functions are the partial derivatives
    #           of this term with respect to its variables.  The key
    #           to this dict is the variable index in [0..nVars-1].
    #           This is just a cache of partials computed elsewhere.

    # This initializer takes a list of the dynamic variables that this
    # term involves, and a differentiable function giving the value of
    # this term (given values of the variables).  The dynamical variables
    # in the given <varlist> must correspond (in the same order!) to the
    # arguments to the given function.

    def __init__(inst, name:str=None, varList:Iterable[DynamicVariable]=[],
                 function:BaseDifferentiableFunction=None):

            # First do generic initialization for DerivedDynamicFunction instances.
            # This remembers our variable list and our associated evaluation function.

        DerivedDynamicFunction.__init__(inst, name, varList, function)

        inst.initializeVarIndex()

            # Add all the given variables to our list of variables we can
            # be differentiated by.  NOTE: If one of those "variables" is iself
            # actually a DifferentiableDynamicFunction of some other varibles,
            # we can go on and add the variables that it depends on as well!

        for var in varList:
            inst.addVariable(var)

            # The following is kind of clumsy; it won't work if there is more
            # than one level of nested sub-variables.  Fix this at some point.

        for var in varList:
            if isinstance(var, DifferentiableDynamicFunction):
                
                if doDebug:
                    logger.debug(("DifferentiableDynamicFunction.__init__(): " +
                                  "Variable %s of %s is itself a DifferentiableDynamicFunction " +
                                  "so let's also add the variables it depends on.") %
                                 (str(var), str(inst)))
                    
                for subvar in var.varList:
                    inst.addVariable(subvar)

        if doDebug:
            logger.debug(("DifferentiableDynamicFunction.__init__(): "
                          "Setting ._function attribute of DDF %s to %s")
                         % (str(inst), str(function)))

        if function != None:
            inst._function = function       # Remember the function, if provided.

        inst._partials = dict()         # Initially empty cache of partials.

    def initializeVarIndex(inst):
        inst._varIndex = dict()
        if hasattr(inst, '_varList'):
            for var in inst._varList:
                index = inst._varList.index(var)
                inst._varIndex[var] = index

    # Adds a variable to the list of variables we can be differentiated by.
    # Doesn't attempt to figure out what our partial is WRT the new variable yet.

    def addVariable(inst, var:DynamicVariable):

        if doDebug:
            logger.debug(("DifferentiableDynamicFunction.addVariable():  " +
                          "Adding variable %s to the list of variables that " +
                          "function %s can be differentiated by...") % (str(var), str(inst)))

            # Create our variable list if it doesn't exist yet.

        if not hasattr(inst, '_varList'):
            inst._varList = []

            # Create our variable index if it doesn't exist yet.

        if not hasattr(inst, '_varIndex'):
            inst._varIndex = dict()

            # If the variable isn't already in the variable list, add it.

        if var not in inst._varIndex:

            if doDebug:
                logger.debug(("DifferentiableDynamicFunction.addVariable():  " +
                              "Previously %s's variable list was %s.") % (str(var), str(inst._varList)))
                logger.debug(("DifferentiableDynamicFunction.addVariable():  " +
                              "Previously %s's variable index was %s.") % (str(var), str(inst._varIndex)))
            
                # Figure out what this new variable's index is in the last.

            index = len(inst._varList)

                # Add the new variable to the list.

            inst._varList.append(var)

                # Add the new variable's index to the index.

            inst._varIndex[var] = index

            if doDebug:
                logger.debug(("DifferentiableDynamicFunction.addVariable():  " +
                              "Added variable %s to %s's variable list in the " +
                              "%d'th position.") % (str(var), str(inst), index))

    # Instance public methods:
    #
    #   .dynPartialDerivWRT(v:DynamicVariable) - Given the identification
    #       of one of the dynamic variables that this DerivedDynamicFunction
    #       depends on, return another DerivedDynamicFunction which
    #       is a callable function that, given a point in time t, evaluates
    #       the partial derivative of the term with respect to that
    #       variable at that point in time (given the values that other
    #       variables would have at that point in time).

    def dynPartialDerivWRT(self, v:DynamicVariable) -> DerivedDynamicFunction:

        if v not in self._varIndex:

            # If we can't do df/dv directly, search for another variable v' such
            # that we can compute df/dv = df/dv' * dv'/dv.  NOTE: This is presently
            # limited to only one level of chaining.
            
            dynPartial = self.chainRuleSearch(v)

            if dynPartial == None:        
                errmsg = ("Could not find any intermediate variable for chain rule when " +
                          "attempting to differentiate %s with respect to %s.")%(str(self),str(v))

                logger.critical("DifferentiableDynamicFunction.chainRuleSearch: " + errmsg)
        
                raise NoIntermediateVariableException(errmsg)

##            errmsg = ("DyanmicVariable %s not found in _varIndex{} of " +
##                      "DifferentiableDynamicFunction %s!") % (str(v), str(self))
##            logger.exception("DifferentiableDynamicFunction.dynPartialDerivWRT(): " + errmsg)
##            raise 

        else:

            if doDebug:
                logger.debug("DifferentiableDynamicFunction.dynPartialDerivWRT(): " +
                             "Looking up the index of DynamicVariable %s..." % str(v))

                logger.debug("The ._varIndex dict of %s is %s." % (str(self), str(self._varIndex)))

            varIndex = self._varIndex[v]    # Look up this variable's index in our list.

            if doDebug:
                logger.debug("DifferentiableDynamicFunction.dynPartialDerivWRT(): " +
                             "The index of DynamicVariable %s is %d..." % (str(v), varIndex))

                # We may have previously constructed the dynamic function for
                # this particular partial derivative.  If so, just look it up.

            if varIndex in self._partials:
                return self._partials[varIndex]

                # Check to see if this is a case where we can use the chain rule.

            dynPartial = self.chainRuleSearch(v)

            if dynPartial == None:

                    # Ask our BaseDifferentiableFunction for its partial derivative
                    # with respect to the <varIndex>'th variable.  Note that at this
                    # point, this function is still unevaluated.

                try:
                    try:
                        partial = self._function.partialDerivWRT(varIndex)
                    except IndexError as e:
                        logger.exception(("DifferentiableDynamicFunction.dynPartialDerivWRT(): " +
                                          "IndexError exception in %s trying to find the partial derivative of %s " +
                                          "with respect to %s!") % (str(self), str(self._function), str(v)))
                        raise e
                    
                    # Now construct a dynamic function corresponding to this partial
                    # derivative and remember it.

                    dynPartial = DerivedDynamicFunction("d%s_over_d%s"%(self.name,v.name), self.varList, partial)
                    
                except TypeError as e:
                    logger.exception(("DifferentiableDynamicFunction.dynPartialDerivWRT(): " +
                                      "TypeError exception in %s trying to find the partial derivative of %s " +
                                      "with respect to %s!") % (str(self), str(self._function), str(v)))
                    raise e

            # Cache this result so we don't have to recalculate it each time.
            
        self._partials[varIndex] = dynPartial

            # Return that dude.

        return dynPartial
    
    def chainRuleSearch(self, v:DynamicVariable) -> DerivedDynamicFunction:

        # Search all possible intermediate variables.

        for var in self._varIndex:

            if isinstance(var, DifferentiableDynamicFunction):
                
                if v in var._varIndex:

                    # First, find the partial of self with respect to var.

                    leftPartial = self.dynPartialDerivWRT(var)

                    if doDebug:
                        logger.debug("The partial of %s with respect to %s is %s..." %
                                    (str(self), str(var), str(leftPartial)))

                    # Next, find the partial of var with respect to v.

                    rightPartial = var.dynPartialDerivWRT(v)

                    if doDebug:
                        logger.debug("The partial of %s with respect to %s is %s..." %
                                    (str(var), str(v), str(rightPartial)))

                    # Now multiply them.

                    overallPartial = leftPartial * rightPartial

                    # Remember that, yes, we are a function of v.

                    self.addVariable(v)

                    return overallPartial

        return None

    def printInfo(me):
        if doInfo:
            msg = "\t\t%s[" % me.name
            for v in me._varList:
                msg += v.name
                if v is not me._varList[-1]:
                    msg += ','
            msg += ']'
            logger.info(msg)
