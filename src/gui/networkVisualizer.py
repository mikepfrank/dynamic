#|==============================================================================
#|                                  TOP OF FILE
#|
#|      File name:  networkVisualizer.py             [Python module source file]
#|
#|      Description:
#|
#|              This Python module provides a GUI for visualization of
#|              a dynamic circuit, i.e. a network of interacting dynamic
#|              elements.  The state of each dynamic element is visual-
#|              ized via a set of phase diagrams, one for each general-
#|              ized coordinate making up the state of the element.
#|              Within each phase diagram, the state is plotted in two
#|              dimensions using the position q and momentum p of the
#|              coordinate.  The point representing the present state is
#|              animated and a gradually-fading trail illustrates the
#|              dynamical history of the coordinate.  The network
#|              structure is illustrated as a graph with links between
#|              nodes (representing dynamic elements) and icons (repre-
#|              senting interactions).  For interactions implementing
#|              logic gates or other circuit elements, standard icons
#|              are used.  Some elements (such as memristors) can have
#|              internal state variables, and a different representation
#|              is used for these in which a node (representing the
#|              internal dynamical state variables) is illustrated
#|              inside the icon representing the element.
#|
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

from    threading       import  *

from    tkinter         import  *

from    logmaster   import  *
from    gui         import  _logger

from    .worklist   import  *
from    .           import  guiapp       # For refreshing guibot
from    .guiapp     import  *

from    network.dynamicNetwork    import  DynamicNetwork

__all__ = [
        'NetworkVisualizer'
    ]


    # We make ourselves a subclass of Canvas for now, because that will
    # be implementing the guts of our functionality.  Later we may add more
    # widgets around the edges and the Canvas may be demoted to an instance
    # attribute.

class NetworkVisualizer(Canvas):

    def __init__(inst, master:BaseWidget=None,
                 title:str="Dynamic Network Visualizer",
                 network:DynamicNetwork=None):

        global guibot;  guibot = guiapp.guibot      # Refresh this global

        if not ambot():
            return guibot(lambda: inst.__init__(master, title, network))
        
        inst.lock = RLock()

        with    inst.lock:

            inst.network = network

            if master is None:
                master = TopWin(title=title)

            Canvas.__init__(inst, master=master)
                            
            guigo()     # Start TkInter if not already running.

            inst.outputDriver = Worker(role="netVisDrv")
            
    def  amDriver(this):  return  current_thread() == this.outputDriver    

