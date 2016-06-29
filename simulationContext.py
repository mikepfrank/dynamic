import logmaster
logger = logmaster.getLogger(logmaster.sysName + '.simulator')
    # The hamiltonian module is part of our core simulation component.

from fixed          import Fixed
from dynamicNetwork import DynamicNetwork

class SimulationContext:

    # Public data members:
    # --------------------
    #
    #       inst.timedelta:Fixed
    #
    #           Magnitude of the time increment between subsequent time steps.
    #           For consistency and to mantain reversibility, this should be
    #           the same throughout a given simulation run.  However, there
    #           may be times when the user wants to adjust it interactively,
    #           so as to explore the simulation more quickly vs. more
    #           precisely.
    #
    #
    # Public properties:
    # ------------------
    #
    #       inst.network:DynamicNetwork
    #
    #           The Dynamic network being simulated.
    #
    #       inst.timestep:int
    #
    #           Our idea of the current "global" time-step number.  In reality,
    #           individual pieces of the network being simulated may be ahead
    #           or behind this by a small amount at any given moment.
    #
    #
    # Private data members:
    # ---------------------
    #
    #       inst._network:DynamicNetwork
    #
    #           The Dynamic network being simulated.
    #
    #       inst._timestep:int
    #
    #           Our idea of the current "global" time-step number.  In reality,
    #           individual pieces of the network being simulated may be ahead
    #           or behind this by a small amount at any given moment.
    

    def __init__(inst, timedelta:Fixed=None, network:DynamicNetwork=None):

        # Default the time-delta, if not provided, to 0.01.  This is small
        # enough to roughly approximate the ideal behavior, but large enough
        # to provide a fast simulation.

        if timedelta is None:
            timedelta = Fixed(0.01)

        inst.timedelta = timedelta      # Remember it.

            # If the network was provided, remember it as well.

        if network is not None:
            inst.network = network
            
    @property
    def network(self) -> DynamicNetwork:
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

    @property
    def timestep(self) -> int:

            # If our timestep-number hasn't been set yet,
            # initialize it to zero.
        
        if not hasattr(self,'_timestep'):
            self._timestep = 0
            
        return self._timestep

    @timestep.setter
    def timestep(self, timestep:int):
        self.evolveTo(timestep)

    def evolveTo(self, timestep:int):
        if timestep != self.timestep:
            self._timestep = timestep
            network = self.network
            if network is not None:
                network.evolveTo(timestep)

    def stepForward(self, nSteps:int=1):
        self.timestep += nSteps

    def stepBackward(self, nSteps:int=1):
        self.timestep -= nSteps

    # A simple test:  Simply step the simulation forward 10 steps.

    def printDiagnostics(self):
        
            # Some simple diagnostic output (not general): Display
            # position and momentum values of the node named 'q'.
            
        logger.normal("%d, %.9f, %d, %.9f" %
                      (self.network._nodes['q'].coord.ccp._posVar.time,
                       self.network._nodes['q'].coord.ccp._posVar.value,
                       self.network._nodes['q'].coord.ccp._momVar.time,
                       self.network._nodes['q'].coord.ccp._momVar.value))

    def test(self):
        self.printDiagnostics()
        for t in range(500):
            self.stepForward(2)
            self.printDiagnostics()

        

    
