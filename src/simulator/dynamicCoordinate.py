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

import random   # Python random-number generator module.

from fixed  import Fixed     # Fixed-precision math class.

import logmaster; from logmaster import *
logger = getLogger(logmaster.sysName + '.simulator')
    # The dynamicCoordinate module is part of our core simulator component.

from .hamiltonian                    import HamiltonianTerm,Hamiltonian
from .hamiltonianVariable            import PositionVariable,MomentumVariable,VelocityVariable
from functions.kineticEnergyFunction          import SimpleQuadraticKineticEnergyFunction

class SimulationContext: pass

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

    def __init__(inst, name:str=None, posval:Fixed=None,
                 momval:Fixed=None, postime:int=0, 
                 hamiltonian:Hamiltonian=None,
                 context:SimulationContext=None):

        inst.name = name

        if isinstance(name,str):
            qname = 'q' + name
        else:
            qname = None

        if isinstance(name,str):
            pname = 'p' + name
        else:
            pname = None

        #-- Create the position and momentum variables.
            
        q = PositionVariable(qname, value=posval, hamiltonian=hamiltonian, context=context)
        p = MomentumVariable(pname, value=momval, hamiltonian=hamiltonian, context=context)

        if doDebug:
            logger.debug("CanonicalCoordinatePair.__init__(): Just after creating " + 
                          "momentum variable, its value is %f" % p.value)

        #-- Tie those two lil' guys together.  They'll
        #   respond by automatically setting up their time
        #   derivative functions if the Hamiltonian is set.
        
        q.conjugateMomentum = p

        #-- Set up initial position and momentum time step numbers..

        q.time = postime
        p.time = postime + 1

        #-- Remember these dynamic variables internally for future reference.

        inst._posVar = q
        inst._momVar = p

        if doDebug:
            logger.debug("CanonicalCoordinatePair.__init__(): Just before exiting, " + 
                          "momentum value is %f" % inst._momVar.value)

    def renameTo(me, name:str):
        me.name = name
        me._posVar.renameTo('q'+name)
        me._momVar.renameTo('p'+name)

    # When we talk about evolving a CCP to a specific timestep, what we mean by this
    # is to evolve its position variable to that timestep.

    def evolveTo(inst, timestep:int):
        inst._posVar.evolveTo(timestep)

    @property
    def posVar(self):
        return self._posVar

    @property
    def momVar(self):
        return self._momVar
        
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

            # Tell both variables in this pair what their Hamiltonians are.

            self.q.hamiltonian = hamiltonian
            self.p.hamiltonian = hamiltonian


# ReinitializationException - The semantics of this class of
#   exceptions is that the program attempted to re-initialize
#   some structure that was previously initialized, and where
#   such reinitialization is not allowed.

class ReinitializationException(Exception): pass

# DynamicCoordinate class.  For our purposes here, a DynamicCoordinate
# always means a canonical coordinate pair (q,p), where q is a
# generalized position coordinate and p is its associated conjugate
# momentum coordinate.  Further, by default all coordinates come
# equipped with an associated kinetic-energy Hamiltonian term of the
# form (1/2)m*v^2 = (1/2)p^2/m, where m is an effective mass associated
# with the coordinate.  Please note that this is a simple nonrelativistic
# expression for the kinetic energy, and would need to be modified for
# other scenarios.  The partial wrt p of this term is just p/m=v, and so
# that becomes the d/dt for the position q.  Meanwhile, a Coordinate can
# be decorated with additional potential energy or interaction terms which
# depend upon the q of this (and possibly other) coordinates in the system;
# the partial wrt q of these terms will determine the force dp/dt that
# updates the momentum variable.

class DynamicCoordinate:

    # Public properties:
    #
    #       .mass [Real] - Effective mass value associated with
    #           this dynamic coordinate.
    #
    #       .hamiltonian [Hamiltonian] - The overall Hamiltonian
    #           for the system that this particular DynamicCoordinate
    #           is a part of.  This is a "set-once" property.
    #           (Subsequent attempts to set it after the first will
    #           generate an exception.)
    #
    #       .context:SimulationContext - The simulation context
    #           that this dynamical coordinate exists in the context of.
    #
    #       position [Fixed] - Generalized position of this coordinate
    #       velocity [Fixed] - Generalized velocity of this coordinate

    # Public data members:
    #
    #       name [str] - Name of this coordinate, as a string.  (For
    #           simple nodes, this will generally be the same as the
    #           node name.)
    #
    #       ccp [CanonicalCoordinatePair] - This object holds the
    #           coordinate's position and momentum degrees of freedom.
    #
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
    #
    # Private data members:
    #
    #       ._hamiltonian [Hamiltonian] - The overall Hamiltonian
    #           for the system that this particular DynamicCoordinate
    #           is a part of.
    #
    
    def __init__(inst, hamiltonian:Hamiltonian, name:str=None, mass=None,
                 context:SimulationContext=None):

            # Give a new dynamical coordinate a unit mass by default.

        if mass==None: mass = 1

        if doDebug:
            logger.debug("Creating a new dynamical coordinate named %s with effective mass %f..."
                         % (name, mass))

            # Remember how to get to our Hamiltonian for future reference.

        inst.hamiltonian = hamiltonian

            # Generate an initial momentum value by sampling from thermal distribution.
            # Later this should be temperature-dependent, but units are arbitrary for now
            # anyway so just assume some arbitrary fixed unit temperature.

        momval = random.normalvariate(0, 1)     # Normally distributed about origin, unit sigma.

            # Create our dynamical guts, namely a CanonicalCoordinatePair (q,p).
        
        inst.ccp = CanonicalCoordinatePair(name, momval=Fixed(momval),
                                           hamiltonian=hamiltonian,
                                           context=context)

            # Next we need to create the kinetic energy term associated
            # with this dynamical coordinate, and add it to the Hamiltonian.
            # First we create a generic quadratic kinetic energy function.

        KEfunc = SimpleQuadraticKineticEnergyFunction(m=mass)

            # Generate the velocity "variable" (really, a derived function
            # of momentum) for this coordinate.

        v = VelocityVariable(inst.ccp._momVar, mass)
        inst._velVar = v

            # Put the velocity variable together with the kinetic energy
            # function to generate a new Hamiltonian term.

        termName = KEfunc.name + '(' + v.name + ')'
        KEHterm = HamiltonianTerm(termName, [v], KEfunc)

        inst.kinetic_term = KEHterm

            # Introduce this new kinetic energy term into the Hamiltonian.

        hamiltonian.addTerm(KEHterm)

    def renameTo(me, name:str):
        me.ccp.renameTo(name)

    def evolveTo(inst, timestep:int):
        inst.ccp.evolveTo(timestep)

    @property
    def position(self):
        return self.ccp.posVar

    @property
    def momentum(self):
        return self.ccp.momVar
        
    @property
    def hamiltonian(self):
        #logger.debug("Retrieving %s's Hamiltonian..." % (str(self)))
        if hasattr(self,'_hamiltonian'):
            hamiltonian = self._hamiltonian
        else:
            hamiltonian = None
        #logger.debug("It looks like %s's Hamiltonian is %s." % (str(self), str(hamiltonian)))
        return hamiltonian

    @hamiltonian.setter
    def hamiltonian(self, hamiltonian:Hamiltonian):
        #logger.debug("Setting %s's Hamiltonian to %s" % (str(self), str(hamiltonian)))
        if hamiltonian != None:
            if self.hamiltonian == None:
                self._hamiltonian = hamiltonian
            else:
                raise ReinitializationException()

    def printInfo(me):
        if doInfo:
            logger.info("\t\tPosition variable: %s" % str(me.position))
            logger.info("\t\tMomentum variable: %s" % str(me.momentum))
            #logger.normal("\t\tHamiltonian:")
            #me.hamiltonian.printInfo()
