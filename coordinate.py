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

class Variable:

    # Data members:
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

    def __init__(inst, name:str=None, value:Fixed=Fixed(0), time:int=0,
                 timeDeriv:Callable[[int],Fixed]=None):

        if None != name:        inst.name      = name
        if None != timeDeriv:   inst.timeDeriv = timeDeriv

        inst.value = value
        inst.time = time

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

        this.value = this.value + this.timeDeriv(time.time + 1)
        this.time  = this.time + 2

    # Steps backwards in time by one minimal time increment (-2 units).

    def stepBackward(this):

        this.value = this.value - this.timeDeriv(time.time - 1)
        this.time  = this.time - 2
            
# Forward declarations to avoid circularity.

class PositionVariable(Variable): pass
class MomentumVariable(Variable): pass
class VelocityVariable(Variable): pass

#  A (generalized) PositionVariable is a variable whose time
#  derivative is ∂H/∂p, where H is a Hamiltonian function, p is
#  the corresponding MomentumVariable, and ∂H/∂p denotes the
#  partial derivative of H with respect to p.

#  When we create a PositionVariable, we (optionally) specify
#  the MomentumVariable that it is associated with.

class PositionVariable(Variable):

    # Data members:
    #
    #   .conjugateMomentum  - The momentum variable that this position
    #       variable is associated with in canonical coordinates.
    #
    #   .hamiltonian - The Hamiltonian energy function of the system
    #       that this position variable is a part of.

    def __init__(inst, name:str=None, value:Fixed=Fixed(0), time:int=0,
                 conjugateMomentum:MomentumVariable=None, hamiltonian:Hamiltonian=None):

        if None != conjugateMomentum:   this.conjugateMomentum = conjugateMomentum
        if None != hamiltonian:         this.hamiltonian = hamiltonian

        if None != conjugateMomentum and None != hamiltonian:
            timeDeriv = hamiltonian.partialDerivWRT(conjugateMomentum)
        else:
            timeDeriv = None    # Simply meaning, not yet set

        # Complete default initialization for dynamical variables.
        Variable.__init__(inst, name, value, time, timeDeriv)

#  A (generalized) MomentumVariable is a variable whose time
#  derivative is -∂H/∂q, where H is a Hamiltonian function, q is
#  the corresponding PositionVariable, and ∂H/∂q denotes the
#  partial derivative of H with respect to q.

class MomentumVariable(Variable):

    # Data members:
    #
    #   .conjugatePosition  - The position variable that this position
    #       variable is associated with in canonical coordinates.
    #
    #   .hamiltonian - The Hamiltonian energy function of the system
    #       that this momentum variable is a part of.

    def __init__(inst, name:str=None, value:Fixed=Fixed(0), time:int=0,
                 conjugatePosition:PositionVariable=None,
                 hamiltonian:Hamiltonian=None):

        if None != conjugatePosition:   this.conjugatePosition = conjugatePosition
        if None != hamiltonian:         this.hamiltonian = hamiltonian

        if None != conjugatePosition and None != hamiltonian:
            timeDeriv = hamiltonian.partialDerivWRT(conjugatePosition)
        else:
            timeDeriv = None    # Simply meaning, not yet set

        # Complete default initialization for dynamical variables.
        Variable.__init__(inst, name, value, time, timeDeriv)

#  A CanonicalCoordinatePair object is essentially a pair of
#  a generalized position coordinate and its conjugate momentum.
#
#  When these coordinate-pair objects are first created, by
#  default the positions are specified at time step 0, and the
#  momenta at time step 1, to allow leapfrogging.
#
#  As a naming convention, if the generalized position coordinate
#  is named 'x' then its conjugate momentum coordinate will be
#  named 'px'.
#
#  

class CanonicalCoordinatePair:

    def __init__(inst, name:str=None, hamiltonian:Hamiltonian=None):

        if isinstance(name,str):
            pname = 'p' + name
        else:
            pname = None

        #-- Create the position and momentum variables.
        q = PositionVariable(name, hamiltonian=hamiltonian)
        p = MomentumVariable(name, hamiltonian=hamiltonian)

        #-- Tie those two lil' guys together.
        q.setConjugateMomentum(p)
        p.setConjugatePosition(q)


#  A VelocityVariable is a variable v that is related to a
#  corresponding momentum variable p by the relation p=mv, where
#  m is an effective mass which is normally a constant.  Note
#  that this formulation does not encompass relativistic or
#  quantum-mechanical concepts of momentum.  Momentum and
#  velocity variables are normally closely locked together.
    

class Coordinate:

    #-- Data members:
    #
    #       name [str] - Name of this coordinate, as a string.  (For
    #           simple nodes, this will generally be the same as the
    #           node name.)
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
        




