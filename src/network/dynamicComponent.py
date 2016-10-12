from typing                     import Iterable

import logmaster;   from logmaster import *

from functions.differentiableFunction     import BaseDifferentiableFunction

from .dynamicLink               import  DynamicLink as  Link
from .dynamicPort               import  DynamicPort as  Port
from .dynamicNode               import  DynamicNode as  Node

from simulator.hamiltonian      import HamiltonianTerm

from    network     import  _logger, dynamicNetwork

__all__ = ['DynamicComponent']

#-- This is a base class from which to derive subclasses for specific
#   types of Dynamic components.  The general features of a component
#   are:
#
#       * It has a set of "ports," which are named interface
#           points that can be linked up to external dynamic nodes.
#
#       * It has a set of interaction functions that interrelate
#           the dynamical states of subsets of nodes connected to
#           various ports.  For our present purposes, these consist
#           of potential energy functions of one or more variables
#           (one per node in a set).  In the context of a network,
#           these translate to Hamiltonian interactions between
#           the nodes' coordinates.

class DynamicComponent:

    #-- Private data members:
    #
    #       ._network [DynamicNetwork] - Network this component is in.
    #
    #       ._ports [dict] - Map from port name to Port object.
    #
    #       ._interactions [list] - Set of interaction functions.
    #           The argument list of each function should be a
    #           subset of the set of our port names.
    #
    #       ._hamTerms [dict] - Map from interaction indices to
    #           the corresponding terms in the network's Hamiltonian.

    #-- Initializer.  This just creates an initially-empty port
    #       map and interaction set.

    def __init__(inst, name:str=None, network=None):

        if name != None: inst.name = name
        if network != None: inst._network = network

        netname = dynamicNetwork.netName(network)

        if doDebug:        
            _logger.debug("Initializing a new DynamicComponent named '%s' in network '%s'" %
                         (str(name), netname))
        
        inst._ports = dict()        # Initially-empty dictionary mapping port name to port object.
        inst._interactions = []     # Initially-empty list of interaction functions.
        inst._hamTerms = dict()     # Initially-empty dictionary mapping interaction indices to Hamiltonian terms.

        inst._enterOurNetwork()    # Tell ourselves, yeah, now actually go into our network (if any).

    @property
    def network(self):
        if hasattr(self, '_network'):
            return self._network
        else:
            return None

    @property
    def ports(self):
        if hasattr(self, '_ports'):
            return self._ports
        else:
            return None

    def portNamed(inst, name:str):
        ports = inst.ports
        if ports != None:
            if name in ports:
                port = ports[name]
            else:
                port = None
        #print("Port named %s is %s" % (name, str(port)))
        return port

    def _enterOurNetwork(self):

        net = self.network

        if net != None:
            net.addComponent(self)      # Tell our network to take us into itself.

    def __str__(self):
        if hasattr(self,'name'):
            return str(self.name)
        else:
            return '(unnamed component)'

    #== Private methods.

    #-- inst._addPort(portName:str) - Creates a new port of this component
    #       named <portName>.  It's initially not linked to anything.

    def _addPort(this, portName:str):

        if doDebug:
            _logger.debug("Adding a port named '%s' to component '%s'..."
                         % (portName, str(this)))
        
        this._ports[portName] = Port(this, portName)

    #-- inst._addPorts(nameList) - Creates new ports of this component
    #       with the names in <nameList>, which should be a list of strings.

    def _addPorts(this, *nameList:Iterable[str]):
        for name in nameList:
            #print("Adding port %s..."%name)
            this._addPort(name)

    #-- .link(portName, node) - Links the port named <portName> of this
    #       component to the external node <node>.

    def link(this, portName:str, node:Node):

        if doInfo:
            _logger.info("Linking port '%s' of component '%s' to node '%s'..."
                         % (portName, str(this), str(node)))

        Link(this.portNamed(portName), node)

    #-- inst.portLinked(portName) - Returns True if our port named 'portName' is linked
    #       to some node currently; returns False otherwise (including if we have no such port).

    def portLinked(this, portName:str):
        #print("Checking to see if port named %s is linked..." % portName)
        port = this.portNamed(portName)     # Get our port of the given name.
        if port == None: return False       # If we didn't have one of that name, return False.
        #print("Checking whether port %s is linked..." % str(port))
        return port.linked                  # Return True if the port is liked to a node, else False.

    # Return True if all the ports of a given one of our interactions are linked to actual nodes.

    def interactionPortsLinked(this, interactionID:int):

        interaction = this._interactions[interactionID]

        argNames = interaction.argNames       # Get the list of arguments for this potential.

        #print("Checking for linked ports with names: %s" % str(argNames))

        return all(map((lambda argName: this.portLinked(argName)), argNames))

    def _hamiltonianTermFor(this, interactionIndex:int):

        if not interactionIndex in this._hamTerms:
            this._hamTerms[interactionIndex] = this._newHamTerm(interactionIndex)
            
        return this._hamTerms[interactionIndex]

    # Create and return a new Hamiltonian term for this interaction.

    def _newHamTerm(self, interactionIndex:int):

        interaction = self._interactions[interactionIndex]

        # First we need to generate the list of DynamicVariables corresponding
        # to the arguments of the interaction function.  These come from the
        # nodes connected to the ports corresponding to those arguments.

        varList = []
        varnames = ""
        for argName in interaction.argNames:    # Iterate through the interaction's argument names.
            port = self.portNamed(argName)      # Look up the port with that name.
            link = port.link                    # Get the link connected to that port.
            node = link.node                    # Get the node at the other end of that link.
            coord = node.coord                  # Get the DynamicCoordinate maintained at that node.
            posVar = coord.position             # Get the generalized position variable for that coordinate.
            varList.append(posVar)              # Append it to our variable list.
            if varnames == "":
                varnames += posVar.name
            else:
                varnames += ', ' + posVar.name

        if doDebug:
            _logger.debug("New term name for interaction %s combines %s and %s..." % (interaction, interaction.name, varnames))
        
        termname = interaction.name + '(' + varnames + ')'

        # OK, now we are ready to construct a new Hamiltonian term implementing
        # this interaction in the case of this component instance.
        
        hamTerm = HamiltonianTerm(termname, varList, interaction)

        if doDebug:
            _logger.debug("Just created a new Hamiltonian term %s..." % str(hamTerm))

        return hamTerm

    # Adds a given interaction function to this component's list of interaction functions.
    # This is marked private because it should normally only be used as subclasses while they are
    # building up the component.

    def _addInteraction(this, potential:BaseDifferentiableFunction):

        if doDebug:
            _logger.debug("Adding interaction function %s to component %s..." %
                         (str(potential), this.name))

        interactionIndex = len(this._interactions)

        # Add the given potential to our list.  (Note that even if it was already
        # present, the semantics here is to add it again... Generating another
        # parallel term in the Hamiltonian which effectively increases the potential.)

        this._interactions.append(potential)

        # If all the named ports are linked to nodes, we can go ahead and create
        # a Hamiltonian term for the interaction.

        if this.interactionPortsLinked(interactionIndex):

            if doDebug:
                _logger.debug("Interaction ports are linked; adding term to network's Hamiltonian...")

                # This returns the Hamiltonian term for this interaction if we haven't
                # previously constructed it.
            
            term = this._hamiltonianTermFor(interactionIndex)

                # Add this new term to the network's Hamiltonian.

            this.network._addHamiltonianTerm(term)

        else:
            if doWarn:
                _logger.warn("Interaction ports not yet linked; can't create Hamiltonian term yet...")

    # Removes a given interaction function from this component's list of interactions functions.

    def _removeInteraction(this, potential:BaseDifferentiableFunction):

        _logger.fatal("DynamicComponent._removeInteraction is not yet implemented!")

        # Be sure to remove the corresponding Hamiltonian term (if any) as well.
        

