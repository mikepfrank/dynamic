#/==============================================================================
#|                          TOP OF FILE:    coordinate.py
#/------------------------------------------------------------------------------
#|
#|      File name:      dynamic/coordinate.py       [Python module source code]
#|
#|      Synopsis:
#|      ---------
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
#|          what its generalized mass is, and the current values of
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

from fixed import *     # Defines the fixed-precision math class Fixed.

import hamiltonian

class Coordinate:

    #-- Data members:
    #
    #       position [Fixed] - Generalized position of the coordinate
    #       velocity [Fixed] - Generalized velocity of the coordinate
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
        




