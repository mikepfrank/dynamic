# hamiltonianVariable.py

from abc import ABCMeta,abstractmethod      # Abstract base class support.

import logmaster
logger = logmaster.getLogger(logmaster.sysName + '.simulator')
    # The dynamicCoordinate module is part of our core simulator component.

from fixed                          import Fixed     # Fixed-precision math class.
from linearFunction                 import ProportionalFunction
from dynamicVariable                import DynamicVariable
from hamiltonian                    import Hamiltonian
from differentiableDynamicFunction  import DifferentiableDynamicFunction

class SimulationContext: pass

class HamiltonianException(Exception): pass

class UnsetHamiltonianException(HamiltonianException): pass
class UnsetMomentumException(HamiltonianException): pass
class UnsetPositionException(HamiltonianException): pass


# Base class for a dynamic variable appearing in a Hamiltonian.  Such variables
# remember the Hamiltonian that they are associated with and their time derivative
# can be inferred from it.  If their Hamiltonian is changed, then their time
# derivative needs to be recomputed; the setTimeDeriv() method does this.
#However, it is abstract and must be defined by subclasses.

class HamiltonianVariable(DynamicVariable,metaclass=ABCMeta):

    def __init__(inst, name:str=None, value:Fixed=None, time:int=0,
                 hamiltonian:Hamiltonian=None, context:SimulationContext=None):

        logger.debug("Initializing the HamiltonianVariable named %s..." % name)

        if hamiltonian != None:  inst.hamiltonian = hamiltonian
            # Goes ahead and sets our time derivative as a side-effect.

        DynamicVariable.__init__(inst, name, value, time, context=context)

    @property
    def hamiltonian(self):
        if hasattr(self,'_hamiltonian'):
            return self._hamiltonian
        else:
            return None

    @hamiltonian.setter
    def hamiltonian(self, hamiltonian:Hamiltonian):
        if hamiltonian != None:
            
            self._hamiltonian = hamiltonian

                # Add this variable to the list of variables that the Hamiltonian can be
                # differentiated by.

            hamiltonian.addVariable(self)

                # Automatically set up our time-derivative in reference to that Hamiltonian.

            self.setTimeDeriv()

    @abstractmethod
    def setTimeDeriv(self): pass

# Forward declarations to avoid circularity.

class PositionVariable(HamiltonianVariable): pass
class MomentumVariable(HamiltonianVariable): pass
#class VelocityVariable(Variable): pass

#  A (generalized) PositionVariable is a variable whose time
#  derivative is ∂H/∂p, where H is a Hamiltonian function, p is
#  the corresponding conjugate MomentumVariable, and ∂H/∂p
#  denotes the partial derivative of H with respect to p.

#  When we create a PositionVariable, we (optionally) specify
#  the MomentumVariable that it is associated with.

class PositionVariable(HamiltonianVariable):

    # Public properties:
    #
    #   .hamiltonian - The Hamiltonian energy function of the system
    #       that this position variable is a part of.  
    #
    #   .conjugateMomentum - The momentum variable that this position
    #       variable is associated with in canonical coordinates.
    #
    # Private data members:
    #
    #   ._hamiltonian - The Hamiltonian energy function of the system
    #       that this position variable is a part of.  Accessed through
    #       the .hamiltonian public @property.
    #
    #   ._conjugateMomentum  - The momentum variable that this position
    #       variable is associated with in canonical coordinates.
    #       Accessed through the .conjugateMomentum public @property.
    #

    def __init__(inst, name:str=None, value:Fixed=None, time:int=0,
                 hamiltonian:Hamiltonian=None, conjugateMomentum:MomentumVariable=None,
                 context:SimulationContext=None):

        logger.debug("Creating a new PositionVariable named %s..." % name)

        # Remember our conjugate momentum variable.

        inst.conjugateMomentum  = conjugateMomentum

        # Do default initialization for Hamiltonian variables.
        
        HamiltonianVariable.__init__(inst, name, value, time, hamiltonian, context)

        # If we know our Hamiltonian already, we can do ahead and set
        # up the dynamic function for our time derivative.

        if hamiltonian != None:
            inst.setTimeDeriv()
                                              
    @property
    def conjugateMomentum(self):
        if hasattr(self,'_conjugateMomentum'):
            return self._conjugateMomentum
        else:
            return None

    @conjugateMomentum.setter
    def conjugateMomentum(self, conjMom:MomentumVariable):

        # If the conjugate momentum variable is being provided,
        # and we're not already configured to use it, then use it.

        if conjMom != None and conjMom != self.conjugateMomentum:
        
            logger.info("Setting conjugate momentum of %s to %s..." % (self, conjMom))

            self._conjugateMomentum = conjMom
            self.setTimeDeriv()

            # Also inform our conjugate momentum variable that
            # we are its "conjugate position" variable.

            conjMom.conjugatePosition = self

    def setTimeDeriv(self):

        if self.hamiltonian != None and self.conjugateMomentum != None:
        
##        if self.hamiltonian == None:
##
##            errStr = ("Can't get %s's time derivative because its Hamiltonian hasn't been set." %
##                         str(self))
##            
##            logger.exception("PositionVariable.setTimeDeriv: " + errStr)
##
##            raise UnsetHamiltonianException(errStr)
##            
##        elif self.conjugateMomentum == None:
##
##            errStr = ("Can't get %s's time derivative because its conjugate momentum hasn't been set." %
##                         str(self))
##            
##            logger.exception("PositionVariable.setTimeDeriv: " + errStr)
##
##            raise UnsetMomentumException(errStr)
##            
##        else:
        
                # Create the dynamic function representing our time derivative.
                # This is just the partial derivative of the Hamiltonian with
                # respect to our conjugate momentum variable, ∂q/∂t = ∂H/∂p.
            dH_over_dp = self.hamiltonian.dynPartialDerivWRT(self.conjugateMomentum)
                # Store that thang for later reference.
            self._timeDeriv = dH_over_dp

    
#  A (generalized) MomentumVariable is a variable whose time
#  derivative is -∂H/∂q, where H is a Hamiltonian function, q is
#  the corresponding conjugate PositionVariable, and ∂H/∂q denotes
#  the partial derivative of H with respect to q.

#  When we create a MomentumVariable, we (optionally) specify
#  the PositionVariable that it is associated with.

class MomentumVariable(HamiltonianVariable):

    # Private data members:
    #
    #   ._conjugatePosition  - The position variable that this position
    #       variable is associated with in canonical coordinates.
    #       Accessed through the .conjugatePosition @property.
    #
    # Public data members:
    #
    #   .hamiltonian - The Hamiltonian energy function of the system
    #       that this momentum variable is a part of.

    def __init__(inst, name:str=None, value:Fixed=None, time:int=0,
                 hamiltonian:Hamiltonian=None,
                 conjugatePosition:PositionVariable=None,
                 context:SimulationContext=None):

        logger.debug("Creating a new MomentumVariable named %s with initial value %f..."
                     % (name,value))

        inst.conjugatePosition = conjugatePosition

            # Do default initialization for Hamiltonian variables.
        HamiltonianVariable.__init__(inst, name, value, time, hamiltonian, context)

    @property
    def conjugatePosition(self):
        if hasattr(self,'_conjugatePosition'):
            return self._conjugatePosition
        else:
            return None

    @conjugatePosition.setter
    def conjugatePosition(self, conjPos):

        # If the conjugate position variable is being provided,
        # and we're not already configured to use it, then use it.

        if conjPos != None and conjPos != self.conjugatePosition:
            
            logger.info("Setting conjugate position of %s to %s..." % (self, conjPos))

            self._conjugatePosition = conjPos
            self.setTimeDeriv()

            # Also inform our conjugate position variable that
            # we are its conjugate momentum variable.

            conjPos.conjugateMomentum = self

    def setTimeDeriv(self):

        if self.hamiltonian != None and self.conjugatePosition != None:
            
                # Create the dynamic function representing our time derivative.
                # This is just the negative of the partial derivative of the
                # Hamiltonian with respect to our conjugate position variable,
                # ∂p/∂t = -∂H/∂q.

            dH_over_dq = self.hamiltonian.dynPartialDerivWRT(self.conjugatePosition)
            momTimeDeriv = -dH_over_dq
            
                # Store that thang for later reference.

            self._timeDeriv = momTimeDeriv            

        

#  A VelocityVariable is a variable v that is related to a
#  corresponding momentum variable p by the relation p=mv, where
#  m is an effective mass which is normally a constant.  Note
#  that this formulation does not encompass relativistic or
#  quantum-mechanical concepts of momentum.  Momentum and
#  velocity variables are normally closely locked together.

# Here, we implement a VelocityVariable v as a DifferentiableDynamicFunction
# that is derived from a corresponding MomentumVariable p.  Its value is defined
# by v=p/m where m is a corresponding effective generalized mass.

class VelocityVariable(DifferentiableDynamicFunction):

    def __init__(inst, momVar:MomentumVariable, mass=None):

        if mass == None:  mass = 1      # Default to unit mass.

        inst._momVar = momVar
        inst._mass = mass

        velFunc = ProportionalFunction('v', momVar.name, 1/mass)

        #velFunc = lambda p: p/mass

        velVarName = 'v' + momVar.name[1:]

        DifferentiableDynamicFunction.__init__(inst, velVarName, [momVar], velFunc)

    @property
    def value(inst):
        return inst()

