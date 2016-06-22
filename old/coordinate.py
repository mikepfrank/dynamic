#/==============================================================================
#|                          TOP OF FILE:    coordinate.py
#/------------------------------------------------------------------------------
#|
#|      File name:      dynamic/coordinate.py
#|
#|      File type:                                  [Python module source code]
#|
#|      Description:
#|      ------------
#|
#|          This module provides a class Coordinate whose instances
#|          are objects representing generalized-coordinate variables
#|          within the context of a dynamical system.
#|
#|          Each Coordinate object maintains various contextual
#|          information, such as which other coordinates it interacts
#|          with (and via what terms in the system's Hamiltonian),
#|          and what time step it is currently at in the simulation
#|          (for both its position and associated momentum variables),
#|          what its generalized mass is and its associated kinetic
#|          energy function, and what are the current values of
#|          its position and associated velocity variables).
#|
#|          The values of position and velocity variables are updated
#|          as needed using an invertible centered-difference update
#|          rule operating in fixed-point arithmetic.  This allows the
#|          simulation to be exactly reversed and repeated as many
#|          times as necessary, with no losses.
#|
#|          Coordinates support operations such as advancing (or
#|          retracting) their state to any later (or earlier) point in
#|          time as requested.  Messages are automatically sent to
#|          neighboring coordinates to cause them to also update their
#|          states as needed.  In general, only a "light cone" space-
#|          time volume's worth of updates needs to be performed in
#|          order to calculate a coordinate value at any point in time.
#|
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

from abc import ABCMeta,abstractmethod      # Abstract base class support.

from fixed  import Fixed     # Fixed-precision math class.
from typing import Callable

import hamiltonian

class SimulationException(Exception): pass

class TimestepException(SimulationException): pass

class TimestepParity(TimestepException): pass

#   A dynamic variable (a.k.a., generalized coordinate, degree of freedom)
#   could in general correspond to either a generalized position, or to a
#   corresponding generalized velocity.
#
#   In Dynamic, a variable has the following general features:
#
#       * (Optional) a name, which is usually derived from
#           the name of the corresponding simulation node.
#
#       * A present value, which is a fixed-point number;
#
#       * A time-step number, which is the index of the present
#           point in time at which the variable has that value.
#
#       * A function giving the value of the time-derivative
#           of the variable at any given time step.
#
#   And, a variable supports the following operations:
#
#       * Evolve it to the given point in time (integer).
#
#       * Evolve forwards or backwards in time by a minimal amount.
#           (This is usually two time steps, for reasons given below.)
#
#   To ensure reversibility, the time-derivative function may not depend
#   directly on the present value of the variable at the same time step.
#
#   During simulation, variables will typically get updated in leapfrog
#   (centered-difference) fashion, so that, for example:
#
#               v(t) + 2Dv(t+1) = v(t+2).
#
#   where Dv = (dv/dt)*Dt is the delta of v extrapolated from the
#   derivative and the time delta Dt.
#
#   Since the arithmetic is fixed-point, addition is reversible, and so
#   this kind of leapfrog-style update can be exactly reversed.  This
#   ensures that the simulation is thermodynamically sound.
#
#   Normally in Dynamic, a position variable gets updated based on
#   velocity variables at adjacent time steps, and vice-versa.  It
#   would be possible to have update schemes involving cycles with
#   more than two phases (triple-leapfrog, etc.), but we do not plan
#   to explore that possibility at present.
#

class DynamicVariable:

    # Public data members:
    #
    #   .name [str]
    #
    #           The name of this variable, a string.  No default.
    #           Names should be unique within a given simulation.
    #
    #   .value [Fixed]
    #
    #           The current value of this variable, a fixed-point
    #           number.  Initially defaults to 0.
    #
    #   .time [int]
    #
    #           The integer index of the current time step.
    #           Initially defaults to 0.
    #
    # Public properties:
    #
    #   .timeDeriv [Callable[[int],Fixed]]
    #
    #           A function that takes an integer time-step
    #           number, and returns what the time derivative
    #           of this variable would be at that time step.
    #           This should be prescaled by 2Dt (two time units).
    #
    #           We can expect that this function will work by
    #           internally causing other state variables to
    #           evolve to the requested point in time as needed.
    #
    # Private data members:
    #
    #   ._timeDeriv [Callable[[int],Fixed]]
    #
    #           A function that takes an integer time-step
    #           number, and returns what the time derivative
    #           of this variable would be at that time step.
    #           This should be prescaled by 2Dt (two time units).
    #
    #           We can expect that this function will work by
    #           internally causing other state variables to
    #           evolve to the requested point in time as needed.
    #
    #           Accessed through the .timeDeriv public @property.
    #
    #   

    def __init__(inst, name:str=None, value:Fixed=Fixed(0), time:int=0,
                 timeDeriv:Callable[[int],Fixed]=None):

        if name != None:  inst.name = name

        inst.timeDeriv = timeDeriv

        inst.value = value
        inst.time = time

    @property
    def timeDeriv(self):
        if self.hasattr('_timeDeriv'):
            return self._timeDeriv
        else:
            return None

    @timeDeriv.setter
    def timeDeriv(self, timeDeriv:Callable[[int],Fixed]):
        if timeDeriv != None:
            self._timeDeriv = timeDeriv

    # Calling a variable returns its current value, or its
    # value at a given timestep (if specified).  NOTE:
    # The latter may change the state of the simulation!

    def __call__(self, timestep:int = None):

        if timestep != None:

            self.evolveTo(timestep)

        return self.value

    # Cause the variable to update itself to the given point
    # in time (specified as an integer time-step number).  If
    # the parities of current and requested time-step numbers
    # do not match, throws a TimestepParity exception.

    def evolveTo(this, timestep:int):

        # First, make sure that the time parities match.
        
        if (timestep - this.time)%2 != 0:
            raise TimestepParity(("Can't get from time step %d to %d " +
                                 "because parities don't match")%(this.time,
                                                                  timestep))

        # Proceed either forward or backward as needed till we get there.

        while timestep > this.time:
            this.stepForward()

        while timestep < this.time:
            this.stepBackward()

    # Steps forwards in time by one minimal time increment (+2 units).

    def stepForward(this):

        this.value = this.value + this.timeDeriv(this.time + 1)
        this.time  = this.time + 2

    # Steps backwards in time by one minimal time increment (-2 units).

    def stepBackward(this):

        this.value = this.value - this.timeDeriv(this.time - 1)
        this.time  = this.time - 2
            
# Abstract class for a variable appearing in a Hamiltonian.
# Abstract because the .setTimeDeriv() method can't be defined
# without first knowing whether it's a generalized position or
# a generalized momentum type of variable.

class HamiltonianVariable(DynamicVariable,metaclass=ABCMeta):

    def __init__(inst, name:str=None, value:Fixed=Fixed(0), time:int=0,
                 hamiltonian:Hamiltonian=None):

        this.hamiltonian = hamiltonian

        Variable.__init__(inst, name, value, time)

    @property
    def hamiltonian(self):

        if self.hasattr('_hamiltonian'):
            return self._hamiltonian
        else:
            return None

    @hamiltonian.setter
    def hamiltonian(self, hamiltonian:Hamiltonian):

        if hamiltonian != None:

            self._hamiltonian = hamiltonian
            self.setTimeDeriv()

    # Subclasses must implement this method.

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


    def __init__(inst, name:str=None, value:Fixed=Fixed(0), time:int=0,
                 hamiltonian:Hamiltonian=None, conjugateMomentum:MomentumVariable=None):

        #-- Remember our conjugate momentum variable.

        this.conjugateMomentum  = conjugateMomentum
        
        #-- Complete default initialization for Hamiltonian variables.
        
        HamiltonianVariable.__init__(inst, name, value, time, hamiltonian)

    @property
    def conjugateMomentum(self):
        
        if self.hasattr('_conjugateMomentum'):
            return self._conjugateMomentum
        else:
            return None

    @conjugateMomentum.setter
    def conjugateMomentum(self, conjMom:MomentumVariable):

        # If the conjugate momentum variable is being provided,
        # and we're not already configured to use it, then use it.

        if conjMom != None and conjMom != self.conjugateMomentum:
        
            self._conjugateMomentum = conjMom
            self.setTimeDeriv()

            # Also inform our conjugate momentum variable that
            # we are its "conjugate position" variable.

            conjMom.conjugatePosition = self

    #-- This causes our time derivative to be recalculated knowing
    #   our Hamiltonian and the identity of our conjugate momentum.

    def setTimeDeriv(self):

        if self.hamiltonian != None and self.conjugateMomentum != None:

            #-- The lambda here is needed to negate the partial derivative.
            self.timeDeriv = lambda timestep:int:
                -self.hamiltonian.partialDerivWRT(self.conjugateMomentum)(timestep)
           
    
#  A (generalized) MomentumVariable is a variable whose time
#  derivative is -∂H/∂q, where H is a Hamiltonian function, q is
#  the corresponding conjugate PositionVariable, and ∂H/∂q denotes
#  the partial derivative of H with respect to q.

#  When we create a MomentumVariable, we (optionally) specify
#  the PositionVariable that it is associated with.

class MomentumVariable(Variable):

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

    def __init__(inst, name:str=None, value:Fixed=Fixed(0), time:int=0,
                 hamiltonian:Hamiltonian=None,
                 conjugatePosition:PositionVariable=None):

        this.conjugatePosition = conjugatePosition

        # Complete default initialization for Hamiltonian variables.
        HamiltonianVariable.__init__(inst, name, value, time, hamiltonian)

    @property
    def conjugatePosition(self):
        return self._conjugatePosition

    @conjugatePosition.setter
    def conjugatePosition(self, conjPos):

        # If the conjugate position variable is being provided,
        # and we're not already configured to use it, then use it.

        if conjPos != None and conjPos != self.conjugatePosition:
            
            self._conjugatePosition = conjPos
            self.setTimeDeriv()

            # Also inform our conjugate position variable that
            # we are its conjugate momentum variable.

            conjPos.conjugateMomentum = self

    #-- This causes our time derivative to be recalculated knowing
    #   our Hamiltonian and the identity of our conjugate position.

    def setTimeDeriv(self):

        if self.hamiltonian != None and self.conjugatePosition != None:

            self.timeDeriv = self.hamiltonian.partialDerivWRT(self.conjugateMomentum)

    

#  A CanonicalCoordinatePair object is essentially a pair of
#  a generalized position coordinate and its corresponding
#  conjugate momentum.
#
#  When these coordinate-pair objects are first created, by
#  default the positions are specified at time step 0, and the
#  momenta at time step 1, to allow leapfrogging.
#
#  As a naming convention, if the generalized position coordinate
#  is named 'x' then its conjugate momentum coordinate will be
#  named 'px'.

class CanonicalCoordinatePair:

    def __init__(inst, name:str=None, posval:Fixed=Fixed(0),
                 momval:Fixed=Fixed(0), postime:int=0,
                 hamiltonian:Hamiltonian=None):

        inst.name = name

        if isinstance(name,str):
            pname = 'p' + name
        else:
            pname = None

        #-- Create the position and momentum variables.
            
        q = PositionVariable(name, hamiltonian=hamiltonian)
        p = MomentumVariable(pname, hamiltonian=hamiltonian)

        #-- Tie those two lil' guys together.  They'll
        #   respond by automatically setting up their time
        #   derivative functions if the Hamiltonian is set.
        
        q.conjugateMomentum = p

        #-- Set up initial position and momentum values.

        q.value = posval;   q.time = postime
        p.value = momval;   p.time = postime + 1
        
    @property
    def hamiltonian(self):

        if self.hasattr('_hamiltonian'):
            return self._hamiltonian
        else:
            return None

    @hamiltonian.setter
    def hamiltonian(self, hamiltonian:Hamiltonian):

        if hamiltonian != None:

            self._hamiltonian = hamiltonian

            # Tell both variables in this pair what their Hamiltonians are.

            self.q.hamiltonian = hamiltonian
            self.p.hamiltonian = hamiltonian


#  A VelocityVariable is a variable v that is related to a
#  corresponding momentum variable p by the relation p=mv, where
#  m is an effective mass which is normally a constant.  Note
#  that this formulation does not encompass relativistic or
#  quantum-mechanical concepts of momentum.  Momentum and
#  velocity variables are normally closely locked together.

# (Not yet implemented.)

# DynamicCoordinate class.  For our purposes here, a DynamicCoordinate always means
# a canonical coordinate pair (q,p), where q is a generalized position
# coordinate and p is its associated conjugate momentum coordinate.
# Further, by default all coordinates come equipped with an associated
# kinetic-energy Hamiltonian term of the form (1/2)m*v^2 = (1/2)p^2/m
# where m is an effective mass associated with the coordinate.  Please
# note that this is a simple nonrelativistic kinetic energy, and would
# need to be modified for other scenarios.  The partial wrt p of this
# term is just p/m=v and so that becomes the d/dt for the position q.
# Meanwhile, a Coordinate can be decorated with additional potential
# energy terms which depend upon the q of this (and possibly other)
# coordinates in the system, the partial wrt q of these terms will
# determine the force dp/dt that updates 

class DynamicCoordinate:

    #-- Data members:
    #
    #       name [str] - Name of this coordinate, as a string.  (For
    #           simple nodes, this will generally be the same as the
    #           node name.)
    #
    #       ccp [CanonicalCoordinatePair] - This object holds the
    #           coordinate's position and momentum degrees of freedom.
    #
    #       position [Fixed] - Generalized position of this coordinate
    #       velocity [Fixed] - Generalized velocity of this coordinate
    #
    #       .kinetic_term - A term in the system's Hamiltonian that
    #           depends only on the generalized velocity of this
    #           coordinate (and no other positions or velocities).
    #
    #       .potential_term - A term in the system's Hamiltonian that
    #           depends only on the generalized position of this
    #           coordinate (and no other positions or velocities).
    #
    #       .interaction_terms - A list of pairs (T,n), where T is an
    #           interaction term in the system's Hamiltonian whose
    #           value depends on the generalized positions of this
    #           and other coordinates.
    #
    #
    #       pos_t [Integral] - Time step index of cur. position coordinate.
    #       vel_t [Integral] - Time step index of cur. velocity coordinate.
    
    def __init__(inst):

        #-- Default the position,velocity to 0 until we know better.
        inst.position = Fixed(0)
        inst.velocity = Fixed(0)

        #-- Also default the time step indices to 0 until a simulation is started.
        inst.pos_t = 0
        inst.vel_t = 0
        




