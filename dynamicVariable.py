from fixed  import Fixed     # Fixed-precision math class.
from typing import Callable

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
            
