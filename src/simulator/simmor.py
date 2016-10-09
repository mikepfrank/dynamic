# simulator.simmor
#
#   This module creates a thread object that is designated to actually
#   run the simulation.  We put this in its own thread rather than running
#   the simulation in the main thread so that the GUI will still be responsive
#   even while the simulation is running.

from    logmaster   import  *
from    simulator   import  _logger

from    .simulationContext          import  SimulationContext   as SimCon
    # Used for tracking global state of the simulation.

from    examples.exampleNetworks    import  FullAdderNet
    # The exampleNetworks module defines various simple example
    # networks to be used for development and testing.  Here we import
    # the one that we will use here for our demo.

from    gui.worklist                import  *

__all__ = ['simbot', 'initSimbot', 'Simmor']

    # The simbot is a worker thread to handle possibly time-consuming
    # simulator tasks, so that they don't bog down the main thread.

global  simbot
simbot = None

def initSimbot():
    global simbot
    if simbot is None:
        simbot = Worker(role="simbot", component="simulator")

class   Simmor:

    def __init__(me):
        initSimbot()

    def doDemo(me):

            #-----------------------------------------------------------
            # Tell logging facility that for the next little while here,
            # we are running on behalf of the simulator component.

        setComponent('simulator')

            #-----------------------------------------------------------------
            # First create a new simulation context object, initially empty.
            # This stores global parameters of the simulation (such as the
            # time delta value) and tracks global variables of the simulation
            # (such as the current time-step number).  We'll let it take its
            # default values for now.  At this point, the network to be
            # simulated has not been created yet.

        me.sc = sc = SimCon()


            #---------------------------------------------------------
            # Create an extremely simple example network for initial
            # testing during development.  Tell it that it's going to
            # be using that simulation context that we just created.

        ##    _logger.normal("Creating an exampleNetworks.MemCellNet instance...")                
        ##    net = exampleNetworks.MemCellNet(context=sc)

        ##    _logger.normal("Creating an exampleNetworks.InverterNet instance...")                
        ##    net = exampleNetworks.InverterNet(context=sc)

        ##    if doNorm:
        ##        _logger.normal("Creating an exampleNetworks.AndGateNet instance...")     
        ##    net = exampleNetworks.AndGateNet(context=sc)

        ##    if doNorm:
        ##        _logger.normal("Creating an exampleNetworks.HalfAdderNet instance...")     
        ##    net = exampleNetworks.HalfAdderNet(context=sc)

        if doNorm:
            _logger.normal("Creating an exampleNetworks.FullAdderNet instance...")     
        me.net = net = FullAdderNet(context=sc)

        ##    _logger.debug("Initial node X momentum is: %f" % 
        ##                  net.node('X').coord.momentum.value)

            #---------------------------------------------------------
            # Run the built-in .test() method of the example network.

        if doNorm:
            _logger.normal("Requesting simulator to run a simple test...")
        
            # This method exercises some basic simulation capabilities.
            # It's time-consuming, so we farm it out to the simbot worker
            # thread.
        simbot(lambda: sc.test())

