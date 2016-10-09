#===============================================================
# Terminal.py
#
# This module is a factory for creating objects of the general
# class Terminal, which represents a virtual-terminal window,
# which displays a text output stream and accepts text input.
#
# However, the Terminal class is itself only an abstract class,
# and it must be instantiated via a more specific implementation
# subclass.  The default constructor takes care of this.
#================================================================

#import TikiTerm     # This is our default implementation class.
#
## IMPLEMENTATION [module global] - Defines our default implementation.
##   We'll use the TikiTerm module, which is a simple terminal built
##   on top of the TkInter toolkit.
#
#IMPLEMENTATION = TikiTerm.TikiTerm

#------------------------------------------------------------------
# TextStyle [module class] - Abstract class for text styles used to
#   determine how text will be drawn.  Implementations of Terminal
#   should subclass this as appropriate for their own purposes.

class TextStyle:
    # __init__(*args) [special instance method] - Initialize a newly
    #   created TextStyle object.  If called with no arguments, it
    #   should return a default style.
    def __init__(self, *args): pass     # Default initializer does nothing.

#------------------------------------------------------------------
# Terminal [module class] - Defines our abstract class for virtual
#   terminal objects.  When this class is instantiated, it
#   actually creates an instance of its default implementation
#   class instead.

class Terminal:
    
    # defImplClass (class variable) - The default implementation
    #   subclass to use for instantiations of the Terminal class.
    #   Terminal users should modify this class variable as
    #   desired before instantiating Terminal for the first time.
    
    defImplClass = None

    # new() [class method] - Create a new instance of an
    #       implementation of Terminal.
    def new(*args, **kwargs):
        # Ask our default implementation class to create a new
        # version of itself, instead.  Pass it our arguments.
        return Terminal.defImplClass(*args, **kwargs)

##    #-------------------------------------------------------------
##    # __new__() (special static method) - Creates a new "Terminal"
##    #   object by creating an instance of the default implementation
##    #   class instead.
##
##    def __new__(ofClass, *args):
##        
##        # Ask our default implementation class to create a new
##        # version of itself, instead.  Pass it our arguments.
##        termObj = Terminal.defImplClass.__new__(Terminal.defImplClass, *args)        
##
##        # Calls the new object's __init__ method.  This won't
##        # happen otherwise, since the new object is (usually)
##        # not of our own class Terminal.
##
##        if termObj.__class__ != Terminal:       # Check just in case, to avoid double-inits.
##            termObj.__init__(termObj, *args)    # Initialize the object.

    #----------------------------------------------------------
    # put() (abstract instance method) - Given a string, outputs
    #   that string to the virtual terminal.  The default method
    #   just uses STDOUT.  Subclasses should override this
    #   method.
    #
    #   Tabs should be handled appropriately, with tab stops
    #   at regular intervals (ideally, every 8 columns if in
    #   a fixed-width font).
    #
    #   Ideally, Enter (LF, 0x0a), Return (CR, 0x0d), and
    #   both CR/LF and LF/CR pairs should be all be treated as
    #   individual newline characters, advancing the cursor to
    #   the start of the next line.
    #
    #   Bell (^G, 0x07) should sound a beep or flash the
    #   terminal display if possible.
    #
    #   Backspace (^H, 0x08) should back the cursor up one
    #   position and erase the last character output, but not
    #   beyond the leftmost column of the display.
    #
    #   Other nonprintable ASCII characters should either
    #   produce no output, or produce implementation-dependent
    #   output.  Implementations can also define special escape
    #   sequences if they wish.
    
    def put(self, text:str, style:TextStyle):
        print(text)

