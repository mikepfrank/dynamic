#|==============================================================================
#|                  TOP OF FILE:    simulator/simulationContext.py
#|------------------------------------------------------------------------------
#|   The below module documentation string will be displayed by pydoc3.
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""

    FILE NAME:          simulationContext.py       [Python 3 module source file]

    FILE PATH:          $GIT_ROOT/dynamic/src/simulator/simulationContext.py

    MODULE NAME:        simulator.simulationContext

    IN COMPONENT:       Dynamic.simulator   (core simulation framework)


    MODULE DESCRIPTION:
    -------------------

        The simulationContext module tracks various parameter values
        and object references that are relevant to the simulation as a
        whole, such as the time-step magnitude, and the network of
        dynamic nodes that is being simulated.  It also provides
        methods for operating on the simulation as a whole, including
        a simple self-test method, which steps the simulation forward
        a modest number of steps.

        NOTE: Eventually, direct usage of simulationContext by high-
        level code will be deprecated, and users will be expected to
        go through the new simmor module instead, which supplies a
        somewhat higher-level interface to the simulator.


    BASIC MODULE USAGE:
    -------------------

        from simulator.simulationContext import *  # Class SimulationContext

        sc = SimulationContext()
            # Initializes a simulation context w default parameter values.

        net = MyNetworkClass(context=sc)
            # Creates a network within the simulation context sc.

        sc.test()   # Exercise the simulation with a simple self-test.


    PUBLIC CLASSES:
    ---------------

        See the class's docstring for details.

            SimulationContext                              [module public class]
        
                                                                             """
#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#| End of module documentation string.
#|------------------------------------------------------------------------------


    #|==========================================================================
    #|   1. Module imports.                                [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    #------------------------------------
    # Imports of standard Python modules.

from time import sleep      # Used in a temporary hack to prevent GUI locking.

    #----------------------------------------------------------------------
    # Logging-related imports.  Do these early in case we need to use them.

from logmaster import *     # Provides a range of logging capabilities.
from . import _logger       # Use simulator component logger in this module.

    #-------------------------------------------------------------------------
    # Imports from "lower-level" modules within the Dynamic system.  Note that
    # we are somewhat cheating here, since technically 'network' is considered
    # to be a higher-level package, but somehow we avoid creating any circular
    # module references... (Only because dynamicVariable.py does not actually
    # import simulationContext, but just passes a forward reference.  Or does
    # this mean that this is actually a higher-level module?  Anyway, we only
    # reference DynamicNetwork for type declaration purposes...)
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

from fixed                  import Fixed            # Fixed-point arithmetic.
from network.dynamicNetwork import DynamicNetwork   # A network of dynamic nodes.


    #|==========================================================================
    #|  2.  Global constants, variables, and objects.      [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|======================================================================
        #|  2.1.  Special globals.                      [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global __all__              # List of public symbols exported by this module.
__all__ = [
    'SimulationContext'     # Class of simulation context objects.
    ]


    #|==========================================================================
    #|  3.  Class definitions.                             [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
        #|======================================================================
        #|   3.1.  Normal public classes.               [module code subsection]
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
            #|------------------------------------------------------------------
            #|
            #|      SimulationContext                             [public class]
            #|
            #|          A SimulationContext tracks important overall
            #|          information about a simulation, such as, what
            #|          is the dynamic network that's being simulated,
            #|          and what are the values of general simulation
            #|          parameters such as the size of the time steps.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class SimulationContext:

    #vvvvvvvvvvvv Begin docstring for class SimulationContext vvvvvvvvvvvvvvvvvv
    
    """simulator.simulationContext.SimulationContext              [public class]

            An instance of class SimulationContext tracks important
        overall information about a given simulation, such as, what
        dynamic network is being simulated, and what are the values
        of general simulation parameters such as the size of the time
        steps.

            Public data-member attributes:
            ------------------------------

                inst.timedelta:fixed.Fixed                  [public data member]

                    A fixed-point number giving the magnitude of the
                    time increment between subsequent time steps.  For
                    consistency and to mantain reversibility, this
                    value should stay the same throughout a given
                    simulation run.  (However, there may be times when
                    the user wants to adjust it interactively, so as
                    to explore the simulation more quickly vs. more
                    precisely.)
                                                                             """
    #^^^^^^^^^^^ End of docstring for class SimulationContext ^^^^^^^^^^^^^^^^^^

    #---------------------------------------------------------------------------
    #   [In class SimulationContext.]
    #
    #       Public properties:                             [class documentation]
    #       ------------------
    #
    #           Note:  These are not documented within the class
    #           docstring above because they are documented within
    #           their own individual properties' docstrings below.
    #           Thus, their description here is somewhat redundant.
    #
    #               inst.network:DynamicNetwork
    #
    #                   The specific Dynamic network that's being
    #                   simulated in this specific simulation context.
    #                   (We don't yet support letting multiple networks
    #                   simultaneously share the same simulation context
    #                   object.)
    #
    #               inst.timestep:int
    #    
    #                    Our idea of the current "global" time-step index.
    #                    However, in reality, individual pieces of the
    #                    network being simulated may be ahead or behind
    #                    this time by a small amount at any given moment.
    #
    #---------------------------------------------------------------------------
    
    #---------------------------------------------------------------------------
    #  [In class SimulationContext.]
    #
    #      Private data-member attributes:        [class internal documentation]
    #      -------------------------------
    #
    #           inst._network:DynamicNetwork
    #
    #               The Dynamic network being simulated.
    #
    #           inst._timestep:int
    #
    #               Our idea of the current "global" time-step
    #               number.  In reality, individual pieces of the
    #               network being simulated may be ahead or behind
    #               this by a small amount at any given moment.
    #
    #---------------------------------------------------------------------------

    #===========================================================================
    #   [In class SimulationContext.]
    #
    #       Special instance methods.                       [class code section]
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            #-------------------------------------------------------------------
            #   inst.__init___()                       [special instance method]
            #
            #       Initializes data members of a new object of class
            #       SimulationContext upon its creation.  The initial
            #       values of the object's parameters can be specified
            #       as arguments, but this is optional.  They can also
            #       be specified at a later time.  If the <timedelta>
            #       parameter is not provided, a default value of 0.01
            #       time units is adopted.
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def __init__(inst, timedelta:Fixed=None, network:DynamicNetwork=None):
        
        """Initializes various data members of a new object of class
           SimulationContext upon its creation.  The initial values of
           the object's parameters can be specified as arguments, but
           this is optional.  They can also be (re)assigned at a later
           time.  If the <timedelta> parameter is not provided, a
           default value of 0.01 time units is adopted."""

            #-----------------------------------------------------------
            # Default the time-delta, if not provided, to 0.01.  This
            # is small enough to roughly approximate the ideal behavior,
            # but large enough to provide a reasonably fast simulation.
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        if timedelta is None:
            timedelta = Fixed(0.01)

        inst.timedelta = timedelta      # Remember it. (Uses setter.)

            #--------------------------------------------------
            # If the network was provided, remember it as well.

        if network is not None:
            inst.network = network      # Uses property setter below.

        # We lazily don't bother setting the ._timestep data member until
        # the first time the .timestep property is accessed, in its getter.

    #__/ End method SimulationContext.__init__().

            
    #===========================================================================
    #   [In class SimulationContext.]
    #
    #       Public properties.                              [class code section]
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            #-------------------------------------------------------------------
            #   inst.network:DynamicNetwork                    [public property]
            #
            #       The specific Dynamic network that's being
            #       simulated in the present simulation context.  If
            #       no network has been assigned yet, this is None.
            #
            #       Note there is as yet no deleter method defined.
            #       We haven't needed one yet...
            #
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv      

    @property                                           # Property getter.
    def network(self) -> DynamicNetwork:                
        
        """
            inst.network:DynamicNetwork                      [settable property]

                This property refers to the specific Dynamic network
            that's being simulated in the given simulation context.  If
            no network has been assigned yet, the value is None.  There
            is a setter method, but (currently) no deleter method.
            
                Note that setting this property to refer to a given
            network has the side-effect of evolving the state of that
            network forwards or backwards in time as ineeded to be
            consistent with the current value of the inst.timestep
            property.                                                        """
        
        if hasattr(self, '_network'):   # If the underlying attribute exists,
            return self._network        #   return its value,
        else:                           # otherwise,
            return None                 #   return None (instead of error).
        
    #__/ End .network getter.

    @network.setter                                     # Property setter.
    def network(self, network:DynamicNetwork=None):
        
        if network is None:
            if hasattr(self,'_network'):
                del self._network           # Just remove the attribute.
        else:
            # Really should check here to make sure network is really
            # an instance of DynamicNetwork.
            self._network = network
            network.evolveTo(self.timestep)
            
    #__/ End .network setter.


            #-------------------------------------------------------------------
            #   inst.timestep:int                              [public property]
            #
            #       Our idea of the current "global" time-step index.
            #       However, in reality, individual pieces of the
            #       network being simulated may be ahead or behind
            #       this time by a small amount at any given moment.
            #
            #       Note that the setter method actually evolves the
            #       state of the simulation forwards or backwards in
            #       time as needed, as a side-effect.
            #
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv      

    @property                                               # Property getter.
    def timestep(self) -> int:

        """
            inst.timestep:int                                [settable property]
                
                This property represents our idea of the current
            "global" time-step index in the current state of the
            simulation.  However, in reality, individual pieces of the
            network being simulated may be ahead or behind this time
            by a small amount at any given moment.

                There is a setter method, but no deleter method.  This
            property should always have an integer value when examined.
            Its initial value will be 0 if the user did not specify
            otherwise.  Setting this property to a non-integer value
            may have unpredictable consequences.
            
                Note that assigning to this property actually evolves
            the state of the simulation forwards or backwards in time
            as needed to get to (roughly) the indicated point in time,
            as a side-effect.                                                """

        # If our timestep-number hasn't been set yet, initialize it to zero.
        
        if not hasattr(self,'_timestep'):   self._timestep = 0
            
        return self._timestep

    #__/ End .timestep getter.

    @timestep.setter                                        # Property setter.
    def timestep(self, timestep:int):

        # Really should do some error-checking here, to make sure that timestep
        # is really an integer or can be converted to an integer.

        self.evolveTo(timestep)

    #__/ End .timestep setter.

        #=======================================================================
        #   [In class SimulationContext.]
        #
        #       Public instance methods.                    [class code section]
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            #|------------------------------------------------------------------
            #|  inst.evolveTo()                         [public instance method]
            #|
            #|      This is our core method that takes the current
            #|      simulation to a new point in time.  (Note that
            #|      the .timestep setter calls this, and thus the
            #|      below stepForward() and stepBackward methods
            #|      indirectly do as well.  However, the real work
            #|      is done by the underlying DynamicNetwork object.
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def evolveTo(self, timestep:int):
        """Evolves the state of the simulation to the specified absolute
           point in time (denoted by an integer timestep index)."""
        if timestep != self.timestep:       # Don't do anything if no change.
            self._timestep = timestep       # Set the underlying attribute.
            network = self.network          # Retrieve our network property.
            if network is not None:         # If the network is set (non-None),
                network.evolveTo(timestep)  # evolve it to the given time-point.

            #|------------------------------------------------------------------
            #|  inst.step{Forward,Backward}()          [public instance methods]
            #|
            #|      These methods provide a simple interface to take
            #|      the current simulation forwards or backwards to a
            #|      new point in time, by specifying a number of time
            #|      steps to go (starting from the current time).
            #|          Note that they work by using the += and -=
            #|      operators on the .timestep property, which call
            #|      the .timestep setter, which in turn calls the
            #|      .evolveTo() method, which evolves the state of the
            #|      entre underlying Dynamic network.
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

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


            #|------------------------------------------------------------------
            #|  inst.test()                             [public instance method]
            #|
            #|      This method implements a simple diagnostic self-
            #|      test, by stepping the state of the simulation
            #|      forwards by +2 .timedelta-size steps, <nSteps>
            #|      times in a row, displaying network diagnostics
            #|      after each step.  The value of <nSteps> defaults
            #|      to (currently) 1,000 if not otherwise specified.
            #|      (This method was used to generate the data that
            #|      was graphed in the Chaotic Logic presentation at
            #|      ICRC 2016.)
            #|
            #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def test(self, nSteps:int=1000):
        """Displays the states of the nodes from times 0 to 2*<nSteps>,
           stepping forward 2 time units at a time.  (This ensures
           that both position & momentum get updated between points.)"""

        self.network.initStats()            # Prepares to accumulate statistics.
        self.network.printCsvHeader()       # Header for CSV-format output.
        self.network.printDiagnostics()     # Initial state as a CSV line.

        for t in range(nSteps):             # We'll do <nSteps> more lines...
            self.stepForward(2)                 # Updates both p's and q's.
            self.network.printDiagnostics()     # Prints the new state as CSV.
            self.network.gatherStats()          # Accumulates some stats.

                # The following needs some discussion.  Without it, the GUI
                # freezes up (won't respond to mouse actions on window) while
                # this test is running.  Presumably, this is because the guibot
                # queue gets filled up with output-related requests, and so no
                # new window events can be serviced until the queue is emptied.
                # The following gives time between output rows for GUI events
                # to be handled.  However, this is an inelegant solution as it
                # slows down the execution (perhaps substantially).  We really
                # need a more elegant, general solution to this sort of issue.
            
            sleep(0.02)     # This is a temporary hack to prevent GUI locking.

        #__/ End for.
            
        self.network.printStats()   # Output accumulated statistics (averages).

#__/ End class SimulationContext.

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                   BOTTOM OF FILE:    simulationContext.py
#===============================================================================
