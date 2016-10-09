#|==============================================================================
#|                      TOP OF FILE:    simulationContext.py
#|------------------------------------------------------------------------------
#|   The below module documentation string will be displayed by pydoc3.
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""

    FILE NAME:          simulationContext.py       [Python 3 module source file]

    MODULE NAME:        simulationContext

    SOFTWARE SYSTEM:        Dynamic         (simulator for dynamic networks)

    SOFTWARE COMPONENT:     Dynamic.simulator   (core simulation framework)


    MODULE DESCRIPTION:
    -------------------

        The simulationContext module tracks various parameter values
        and object references that are relevant to the simulation as a
        whole, such as the time-step magnitude, and the network of
        dynamic nodes that is being simulated.  It also provides
        methods for operating on the simulation as a whole, including
        a simple self-test method, which steps the simulation forward
        a modest number of steps.


    BASIC MODULE USAGE:
    -------------------

        import  simulationContext               
        from    simulationContext   import *    # Defines SimulationContext

        sc = SimulationContext()
            # Initializes a simulation context w default parameter values.

        net = MyNetworkClass(context=sc)
            # Creates a network within the simulation context sc.

        sc.test()   # Exercise the simulation with a simple self-test.


    PUBLIC CLASSES:
    ---------------

        See class docstring for details.

            SimulationContext                              [module public class]
        
                                                                             """
#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#| End of module documentation string.
#|------------------------------------------------------------------------------


    #|==========================================================================
    #|   1. Module imports.                                [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

import logmaster; from logmaster import *   # Provides logging capabilities.

import time

from fixed          import Fixed                # Fixed-point arithmetic.
from network.dynamicNetwork import DynamicNetwork       # A network of dynamic nodes.

    #|==========================================================================
    #|  2.  Global constants, variables, and objects.      [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|  2.1.  Special globals.                      [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global  __all__         # List of public symbols exported by this module.

__all__ = ['SimulationContext']     # Class for simulation context objects.


        #|======================================================================
        #|  2.2.  Private globals.                      [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global  _logger
    # The logmaster-based logger object that we'll use for logging
    # within this module.
    
_logger = getLogger(logmaster.sysName + '.simulator')
    # The simulationContext module is part of our core simulation facility.


    #|==========================================================================
    #|  3.  Class definitions.                             [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
        #|======================================================================
        #|   3.1.  Normal public classes.               [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
            #|------------------------------------------------------------------
            #|
            #|      SimulationContext                              [public class]
            #|
            #|          A SimulationContext tracks important overall
            #|          information about a simulation, such as, what
            #|          is the dynamic network that's being simulated,
            #|          and what are the values of general simulation
            #|          parameters such as the size of the time steps.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class SimulationContext:

    """A SimulationContext tracks important overall information about
       a simulation, such as, what dynamic network is being simulated,
       and what are the values of general simulation parameters such
       as the size of the time steps.

            Public data members:
            --------------------

                inst.timedelta:Fixed

                    A fixed-point number giving the magnitude of the
                    time increment between subsequent time steps.  For
                    consistency and to mantain reversibility, this
                    value should stay the same throughout a given
                    simulation run.  (However, there may be times when
                    the user wants to adjust it interactively, so as
                    to explore the simulation more quickly vs. more
                    precisely.)
                                                                             """


##            Public properties:
##            ------------------
##
##                inst.network:DynamicNetwork
##
##                    The specific Dynamic network that's being
##                    simulated in this context.
##
##                inst.timestep:int
##    
##                    Our idea of the current "global" time-step index.
##                    However, in reality, individual pieces of the
##                    network being simulated may be ahead or behind
##                    this time by a small amount at any given moment.



        #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        #
        #  [In class SimulationContext.]
        #
        #      Private data members:
        #      ---------------------
        #
        #          inst._network:DynamicNetwork
        #
        #              The Dynamic network being simulated.
        #
        #          inst._timestep:int
        #
        #              Our idea of the current "global" time-step
        #              number.  In reality, individual pieces of the
        #              network being simulated may be ahead or behind
        #              this by a small amount at any given moment.
        #
        #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        #   [In class SimulationContext.]
        #
        #       Special instance methods.                   [class code section]
        #.......................................................................

            #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            #   inst.__init___()                       [special instance method]
            #
            #       Initializes data members of a new object of class
            #       SimulationContext upon its creation.  The initial
            #       values of the object's parameters can be specified
            #       as arguments, but this is optional.  They can also
            #       be specified at a later time.  If the <timedelta>
            #       parameter is not provided, a default value of 0.01
            #       time units is adopted.
            #...................................................................      

    def __init__(inst, timedelta:Fixed=None, network:DynamicNetwork=None):
        
        """Initializes data members of a new object of class
           SimulationContext upon its creation.  The initial values of
           the object's parameters can be specified as arguments, but
           this is optional.  They can also be specified at a later
           time.  If the <timedelta> parameter is not provided, a
           default value of 0.01 time units is adopted."""

            #---------------------------------------------------------
            # Default the time-delta, if not provided, to 0.01.  This
            # is small enough to roughly approximate the ideal behavior,
            # but large enough to provide a fast simulation.

        if timedelta is None:
            timedelta = Fixed(0.01)

        inst.timedelta = timedelta      # Remember it.

            # If the network was provided, remember it as well.

        if network is not None:
            inst.network = network

        # We lazily don't bother setting the ._timestep data member until
        # the first time the .timestep property is accessed, in its getter.

    #__/ End method SimulationContext.__init__().

            
        #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        #   [In class SimulationContext.]
        #
        #       Public properties.                          [class code section]
        #.......................................................................

            #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            #   inst.network:DynamicNetwork                    [public property]
            #
            #       The specific Dynamic network that's being
            #       simulated in the present simulation context.  If
            #       no network has been assigned yet, this is None.
            #...................................................................      

    @property
    def network(self) -> DynamicNetwork:
        
        """The specific Dynamic network that's being simulated in the
           given simulation context."""
        
        if hasattr(self, '_network'):
            return self._network
        else:
            return None

    @network.setter
    def network(self, network:DynamicNetwork=None):
        if network is None:
            if hasattr(self,'_network'):
                del self._network
        else:
            self._network = network
            network.evolveTo(self.timestep)


            #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            #   inst.timestep:int                              [public property]
            #
            #       Our idea of the current "global" time-step index.
            #       However, in reality, individual pieces of the
            #       network being simulated may be ahead or behind
            #       this time by a small amount at any given moment.
            #...................................................................      

    @property
    def timestep(self) -> int:

        """Our idea of the current "global" time-step index.  However,
           in reality, individual pieces of the network being simula-
           ted may be ahead or behind this time by a small amount at
           any given moment."""

            # If our timestep-number hasn't been set yet,
            # initialize it to zero.
        
        if not hasattr(self,'_timestep'):
            self._timestep = 0
            
        return self._timestep

    @timestep.setter
    def timestep(self, timestep:int):
        self.evolveTo(timestep)


        #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        #   [In class SimulationContext.]
        #
        #       Public instance methods.                    [class code section]
        #.......................................................................

    def evolveTo(self, timestep:int):
        """Evolves the state of the simulation to the specified point
           in time (denoted by an integer timestep index)."""
        if timestep != self.timestep:
            self._timestep = timestep
            network = self.network
            if network is not None:
                network.evolveTo(timestep)

    def stepForward(self, nSteps:int=1):
        """Advances the state of the simulation forwards in time by
           <nSteps> timesteps (each of magnitude .timedelta).  If the
           <nSteps> argument is not provided, it defaults to 1."""
        self.timestep += nSteps

    def stepBackward(self, nSteps:int=1):
        """Regresses the state of the simulation backwards in time by
           <nSteps> timesteps (each of magnitude .timedelta).  If the
           <nSteps> argument is not provided, its value defaults to 1."""
        self.timestep -= nSteps

        # A simple test:  Simply step the simulation forward 10 steps.

# Moved this code into the example networks themselves.
##    def printDiagnostics(self):
##        """A quick-and-dirty diagnostic method which assumes that
##           there is a node named 'q' in the simulated network, and
##           displays its position and momentum coordinates."""
##        
##            # Some simple diagnostic output (not general): Display
##            # position and momentum values of the node named 'q'.
##            
##        _logger.normal("%d, %.9f, %d, %.9f, %d, %.9f, %d, %.9f" %
##                      (self.network.nodes['X'].coord.position.time,
##                       self.network.nodes['X'].coord.position(),
##                       self.network.nodes['X'].coord.momentum.time,
##                       self.network.nodes['X'].coord.momentum(),
##                       self.network.nodes['Y'].coord.position.time,
##                       self.network.nodes['Y'].coord.position(),
##                       self.network.nodes['Y'].coord.momentum.time,
##                       self.network.nodes['Y'].coord.momentum()
##                       ))

    def test(self):
        """Displays the states of the nodes from times 0 to 10,000,
           stepping forward 2 time units at a time.  (This ensures
           that both position & momentum are updated between points.)"""

        self.network.initStats()

        self.network.printStatsHeader()

        self.network.printDiagnostics()
        #for t in range(10):
        #for t in range(100):
        for t in range(1000):
        #for t in range(10000):
            self.stepForward(2)
            self.network.printDiagnostics()
            self.network.gatherStats()
            time.sleep(0.02)

        self.network.printStats()

#__/ End class SimulationContext.

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                   BOTTOM OF FILE:    simulationContext.py
#===============================================================================
