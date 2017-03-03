#|***********************************************************************************
#|   tikiterm.py(w)                                          [python module]
#|
#|      A simple virtual terminal module based on the TkInter GUI
#|      toolkit.
#|
#|      This is implemented as a subclass of the Terminal class.
#|      It installs itself as the default implementation of Terminal.
#|      (Terminal implementations based on other GUI toolkits could
#|      be created as well.)
#|
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    #|============================================================================
    #|  Imports.                                                     [code section]
    #|
    #|      Import names from other modules for use in the current module.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|----------------------------------------------------------------------
        #|  Import standard modules.
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

import sys      # For stdout/stderr (& double-underscore-delimited versions of them)
import re       # For regexp search(), split().

from time                   import sleep
from threading              import *
from tkinter                import *
from tkinter.scrolledtext   import *        # The actual TikiTerm application will use one of these.

        #|-----------------------------------------------------------------------
        #|  Import custom modules.
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

from .flag                   import *
from .terminal               import *
from .worklist               import *
from . import guiapp                               # For refreshing guibot
from .guiapp                 import *
from logmaster              import *

    #|============================================================================
    #|  Initialize global variables.                             [code section]
    #|
    #|      In this section we initialize important global variables for
    #|      use by this module and its customers.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|-----------------------------------------------------------------------------
        #|  Get a child logger for logging events that occur within this module.
        #|  for now, we consider the virtual terminal to be part of the application.
        #|  So its logger name is the name of the application logger plus ".term".
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

logger = getLogger(appName + '.term')

        #|------------------------------------------------------------------------------
        #|  __all__                                         [special global variable]
        #|
        #|      List of names that we publicly export to modules that import
        #|      names from this module using "from tikiterm import * "
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

__all__ = [     # Names of color constants, for selecting text foreground/background colors.
            'Black', 'Red', 'Green', 'Blue', 'Cyan', 'Magenta', 'Yellow', 'White',
            'DarkRed', 'DarkGreen', 'DarkBlue', 'DarkCyan', 'DarkMagenta', 'DarkYellow',
            'LightGray', 'DarkGray', 'Pink', 'Purple',
                # Names of classes we provide to our customers.
            'TikiTermTextStyle', 'TikiTermApp', 'TikiTerm',
                # Names of functions we provide to our customers.
            'style',
          ]

        #|---------------------------------------------------------------------
        #|  Some color constants, using TkInter color string format.
        #|  This is intentionally the same color set as is available on
        #|  MS Windows consoles.  However, any RGB color combination
        #|  (up to 24-bit) can also be used.
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

Black = "black";    Red = "red";            Green = "green";    Blue = "blue";
Cyan = "cyan";      Magenta = "magenta";    Yellow = "yellow";  White = "white"

DarkRed = "#700";   DarkGreen = "#070";     DarkBlue = "#007";
DarkCyan = "#077";  DarkMagenta = "#707";   DarkYellow = "#770"

LightGray = "#888"; DarkGray = "#777"

    # A couple of extra colors, for Juliet.

Pink = "#faa";      Purple = "#8a2be2"      # <- Someone else calls this RGB code "Blue Violet"

    # Some custom mark names.

END_OUTPUT      = "endout"      # Marks the end of the output area of the terminal.
START_INPUT     = "startin"     # Marks the beginning of the input area of the terminal.

    # Graphic object - blurry purplish separator between output & input areas.

horiz_divider = None
def init_graphics():            # Call this function after TkInter init & before 1st use.
    global horiz_divider
    if horiz_divider == None:
        horiz_divider = PhotoImage(file="images/purple-beam.gif")

    #|=====================================================================================
    #|
    #|      Class definitions.                                              [code section]
    #|
    #|          In this code section, we define the various classes of objects
    #|          that this module is providing.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|-------------------------------------------------------------------------------
        #|
        #|   TikiTermTextStyle                                   [module public class]
        #|
        #|       Class representing the type of text styles that our particular
        #|       implementation of Terminal knows how to handle.  At present, our
        #|       text styles consist only of a text foreground color and an optional
        #|       background (highlight) color.  They are implemented using TkInter
        #|       text tags.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class TikiTermTextStyle(TextStyle):

    #---------------------------------------------------------------------------------------
    #   Instance data members:
    #
    #       fgColor:string - Foreground (text) color, in Tkinter-understandable format.
    #
    #       bgColor:string - Background (hilite) color in Tkinter-understandable format.
    #           None means to use the regular background color of the terminal (i.e.,
    #           transparent background).
    #
    #       tagName:string - TkInter TagName representing this text style.
    #
    #----------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------
        #   __init__()                                    [special instance method]
        #
        #       Initializes a new TikiTermTextStyle object to represent a
        #       given combination of a foreground text color and (optional)
        #       background highlight color.  If no background color is
        #       specified, the character background is transparent.
        #
    
    def __init__(self, fg=White, bg=None):      # Default to white text.
        self.fgColor = fg
        self.bgColor = bg
        self.tagName = fg
        if self.bgColor != None:                # If background is present,
            self.tagName += ":" + bg            # format tagName as "fgColor:bgColor".

#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#|  End class TikiTermTextStyle.
#|-----------------------------------------------------------------------------------------

        #|---------------------------------------------------------------------------
        #|
        #|   style()                                       [module public function]
        #|
        #|       This is just a convenient little factory function that creates a
        #|       new TikiTermTextStyle object, given a foreground color string and
        #|       an (optional) background color string.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def style(*args):
    return TikiTermTextStyle(*args)

    #|---------------------------------------------------------------------------------
    #|
    #|   TikiTerm                                             [module public class]
    #|
    #|       An object of this class represents an instance of a TikiTerminal
    #|       application running within some particular enclosing master widget,
    #|       which may or may not be a main window or other top-level window.
    #|       (It may also be some smaller frame nested as a panel within some
    #|       larger window.)
    #|
    #|       Multiple TikiTerm instances may exist within the same python
    #|       interpreter process, and they may be created and manipulated
    #|       dynamically from within any thread.  This is accomplished using
    #|       the guiapp module, which automatically queues up major GUI
    #|       requests for execution within a single worker thread.
    #|
    #|       TikiTerm supports writing text to its terminal window display
    #|       in any combination of foreground/background colors, using the
    #|       TikiTermTextStyle class above.
    #|
    #|       Eventually, TikiTerm will be made into a subclass of the
    #|       built-in class "file", or at least will support a subset of its
    #|       interface.  In particular, this will allow it (or auxilliary
    #|       classes) to act as a drop-in replacement for sys.stdin,
    #|       sys.stdout, and sys.stderr (where writes to sys.stderr can even
    #|       produce text of a different color, and input text can be
    #|       shown in a different color as well.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class TikiTerm(Terminal, ScrolledText):

    #-----------------------------------------------------------------------------
    #   Nested classes of TikiTerm.
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #--------------------------------------------------------------------
        #   In                                      [nested public class]
        #
        #       TikiTerm.In will eventually provide a text stream
        #       like interface for reading typed input from a
        #       TikiTerm terminal object.  Not yet implemented.
        #
        #   INTERFACE:
        #
        #       In.readline()   - Returns next 
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    class In():     # Eventually, subclass File or imitate it.

            #----------------------------------------------------------------
            #
            #   Instance data members:
            #
            #       lock:RLock      - Reentrant mutex lock, to serialize
            #                           atomic operations on this structure
            #                           for thread-safety.
            #
            #       ready:Flag      - Flag that is raised when the input
            #                           buffer has text in it, and lowered
            #                           when the input buffer is empty.
            #                           Threads can do ready.wait() to
            #                           block until data is available.
            #
            #       hasLine:Flag    - Flag that is raised when the input
            #                           buffer has at least one full line
            #                           in it, and lowered when it no longer
            #                           has a complete line.  Threads can
            #                           do hasLine.wait() to block until a
            #                           full line is available to read.
            #
            #       EOF:Flag        - Flag that is raised when the input
            #                           terminal is closing / has closed.
            #
            #       blocking:bool   - True if read() and readline() calls
            #                           on this object will block by default
            #                           when there is no data available.
            #
            #       buffer:string   - The content of the buffered text
            #                           input.  Stuff that has been typed,
            #                           but not yet consumed by a reader.
            #
            #--------------------------------------------------------------------

        class Timeout(Exception): pass

            # Constructor
        
        def __init__(inst, term:Terminal=None, block:bool=True):

            logger.info("TikiTerm.In.__init__(): Initializing terminal's input buffer pseudo-stream...")

            inst.lock = RLock()     # Create our mutex lock.

            with inst.lock:
                
                    # Initialize blocking field properly based on constructor argument.
        
                inst.blocking = block

                    # Create the condition flags, initially down
                    # (no data is in buffer initially).  These all use
                    # the same lock as the overall In structure so that a
                    # wait() on any of them will release the structure lock.

                inst.ready      = Flag(lock=inst.lock)
                inst.hasLine    = Flag(lock=inst.lock)
                inst.EOF        = Flag(lock=inst.lock)

                logger.info("TikiTerm.In.__init__(): Initial state of EOF flag is %s." % str(inst.EOF()))

                    # Initialize input buffer to empty string.

                inst.buffer = ""
                
        # End method In.__init__().

            # Closes the input buffer stream.  After the stream has been closed,
            # no more data may come in.  Readers should notice the EOF and finish up.

        def close(inst):

            with inst.lock:

                logger.info("TikiTerm.In.close(): Closing terminal's input buffer stream.")

                inst.EOF.rise()     # Raise the EOF flag.

                    # Also wave the ready and hasLine flags, in hopes that any waiters
                    # on those flags will wake up, notice that the flag value hasn't
                    # changed but that the EOF flag has gone up, and realize that there's
                    # no point in waiting for any more newlines, for example, to appear
                    # in the input buffer.
                
                inst.ready.wave()       # Doesn't change the flag state - just waves the flag.
                inst.hasLine.wave()
                
        # End method close()
            
            # Sets the contents of the input buffer to the given string.
            # Updates flag states appropriately.

        def setbuffer(inst, string:str):

            with inst.lock:

                inst.buffer = string

                logger.info("Input buffer now contains: " + repr(string) + ".")
                
                    # Raise the ready flag if string is non-empty, else lower it.

                inst.ready.setTo(string != "")

                    # Raise the hasLine flag if string has a line-end char, else lower it.

                inst.hasLine.setTo(re.search("\r|\n", string))

        # End method In.setbuffer().

            #  Appends the given string to the end of the input buffer.
            #  Updates flag states appropriately.  Does nothing if the
            #  input stream has already been closed.

        def append(inst, string:str):
            with inst.lock:
                if not inst.EOF():
                    inst.setbuffer(inst.buffer + string)

            # Unconditionally consumes a line from the input buffer & returns it.
            # If there are no line-end sequences in the buffer, consumes
            # entire buffer contents.  The string returned includes
            # a newline (\n) if a line-end sequence was present.  If you want
            # to block until a full line is available, use readline() instead.
            # Anyway, class customers should not use this class-private method.

        def _getline(inst):

            with  inst.lock:

                if inst.hasLine():
                    logger.debug("TikiTerm.In._getline(): About to parse 1st line out of input buffer [%s]..." % repr(inst.buffer))
                    (first, rest) = re.split("\r\n|\n|\r", inst.buffer, maxsplit=1);
                    line = first + "\n"
                    logger.info("TikiTerm.In._getline(): A reader is about to be given the line: " + repr(line) + ".")
                    inst.setbuffer(rest)
                    return line         # Always end line with \n
                
                else:
                    logger.debug("TikiTerm.In._getline(): No line-end in buffer, so returning entire buffer [%s]..." % repr(inst.buffer))
                    everything = inst.buffer
                    inst.setbuffer("")
                    return everything
                
        # End method In._getline()

            #  Read a line from input buffer, possibly blocking if no
            #  line is available yet and the block option is set.
            #  This allows a customer thread to ensure a line is read.
            #  An optional timeout flag (secs) can be provided.  If it is,
            #  and the readline() times out, it throws an exception of
            #  class TikiTerm.In.Timeout.  Otherwise, the line just
            #  read is returned.
            #
            #  NOTE:  Because we provide this method, another version
            #  of which is specified in io.TextIOBase, we provide a
            #  variant, partial implementation of an io.TextIOBase
            #  stream, and so objects of the TikiTerm.In class can
            #  sometimes be used in place of such a stream.
            #

        def readline(inst, block=None, timeout=None):

            logger.debug("Entered TikiTerm.In.readline() method...")

            should_block = inst.blocking    # Should we block?  Init to default.
            
            if block != None:               # Allow block argument to override
                should_block = block        #   that setting if present.

            with  inst.lock:                    # Grab lock for state consistency.

                if not should_block:
                    logger.info("TikiTerm.In.readline(): Reading in non-blocking mode.")

                    # Determine if we should block until a full line is available,
                    # and if so, then do so, with an appropriate timeout if any.
                
                if should_block:
                    if inst.EOF():
                        logger.info("TikiTerm.In.readline(): Stream is closed, so just getting remaining buffer contents...")
                    else:
                        logger.info("TikiTerm.In.readline(): About to wait %s secs for a line..." % str(timeout))
                        if not inst.hasLine.wait(timeout=timeout):         # Wait till a line is ready.
                            raise Timeout()     # If we timed out, raise Timeout exception.

                line = inst._getline()      # Forcible line-reading.    

                logger.debug("Got input line [%s], returning it to caller..." % repr(line))

                return line

        #--------------------------------------------------------------------
        #   Out                                     [nested public class]
        #
        #       TikiTerm.Out provides a file-like interface to a
        #       TikiTerm object.  After creating an instance with
        #
        #           out = TikiTerm.Out(tikiterm, style),
        #
        #       the operation "out.write(str)" will output <str>
        #       to the terminal using style <style>.  This enables
        #       stdout/stderr replacement by setting sys.stdout, etc.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    class Out():

            # Object initializer.
        
        def __init__(inst, term:Terminal=None, style:TikiTermTextStyle=None):
            inst.term = term        # Remember what TikiTerm object this output stream will use.
            inst.style = style      # Remember what text style we'll use for this output stream.

            # write() method, expected by users of File objects.

        def write(this, text:str):
            if text == "": return   # Nothing to write.
#TMI            debug("text [%s] color [%s]" % (text, this.style.fgColor))
            this.term.put(text, this.style)     # Output using output stream's default text style.

            # flush() method, expected by users of File objects.

        def flush(this):
            this.term.flush()       # Pass request through to underlying TikiTerm object.

    #|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #|  End nested class TikiTerm.Out.
    #|----------------------------------------------------------------------------

        # TO DO:  Finish In, Out nested class definitions.

    #------------------------------------------------------------------------
    # Instance variables:
    #
    #   lock:RLock - A re-entrant threading lock to prevent
    #       simultaneous changes to the terminal state from
    #       within different threads.
    #
    #   styleDict:dict - A dictionary mapping from style tagnames
    #       to style objects.  Used for keeping track of what-all
    #       styles have been used so far within our scrText widget,
    #       so we don't try to create a given style more than once.
    #
    #   outputDriver:Worker - A worker thread whose job it is to
    #       coordinate and execute output requests to the terminal.
    #       Output requests get queued up on his worklist for
    #       processing and display.
    #
    #   curstyle:TikiTermTextStyle - The text style currently
    #       being used for output to the display.
    #
    #   curtags:tuple - List of tags currently being used for
    #       output to the display.
    #
    #   outbuf:string - A string for buffering up output for display.
    #       this is done to reduce the overhead of calls to the guibot
    #       to actually write to the display.  Characters are buffered
    #       up here until we get to the end of a given write request,
    #       then the whole string is sent to the display.
    #
    #   lastch:char - A single character (length-1 string) that was
    #       the last character output to the display.  This is needed
    #       for purposes of processing CRLF sequences properly.  It is
    #       sometimes set to empty string ("") when the last character
    #       doesn't matter.
    #
    #   instream:TikiTerm.In - A nested class object providing a
    #       File-like interface to input characters from this terminal.
    #
    #   outstream:TikiTerm.Out - A nested class object providing a File-like
    #       interface to output characters to this terminal.
    #
    #   errstream:TikiTerm.Out - A nested class object providing a File-like
    #       interface to output characters to this terminal using a
    #       special "error" output style.
    #
    #   in_hook:callable    - A function or other callable object
    #       to be invoked, with each newly-entered line as input.
    #       The default method sends the line to instream.  Users can
    #       override this to do something else instead.  HOWEVER, this
    #       runs in the guibot, so users must return quickly to avoid
    #       hanging the gui!  And, be careful about possible deadlocks.
    #
    #---------------------------------------------------------------------------

        #----------------------------------------------------------------------
        #   __init__()                              [special instance method]
        #
        #       Initializer method for class TikiTerm.
        #
        #       Initializes a newly created TikiTerm within the given
        #       master (parent) widget.  If no master is provided,
        #       creates its own new toplevel window instead.  If the
        #       optional <title> string is specified, that will be the
        #       title of the new window.  Also initializes the
        #       underlying ScrolledTextWidget.  Creates a new thread
        #       for receiving, processing, and displaying output text.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def __init__(inst, master:BaseWidget=None, title:str="TikiTerm Virtual Terminal",
                 fg = "white", bg = "black", insertbackground = "yellow",
                 width=80, height=24,   # These are in CHARACTER CELLS, not pixels.
                 role = "tt", in_hook=None):

        global horiz_divider        # Make this global for object persistence.

            #---------------------------------------------------------------------------
            # Locate the global guibot object.
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        # Wait, is the below even necessary?  We already imported * from guiapp above
        # Yes, because it's changed since we imported it?
        
        global guibot               # Reference the global guibot object defined in class guiapp.
        guibot = guiapp.guibot      # Make sure value of this global
            # is current with the module it came from.
            # It's kind of ugly that this is necessary - try to
            #   think of a cleaner approach.

            #---------------------------------------------------------------------------
            # This next construct effectively switches us temporarily into the guibot
            # worker thread, for purposes of consistently tinkering around with the
            # state of TkInter.
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        
        if not ambot():
            return guibot(lambda: inst.__init__(master, title, fg, bg, insertbackground, width, height, role, in_hook))

            #--------------------------------------------------------------------------
            # Keep in mind the below is all happening within the guibot worker thread.
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        logger.debug("guibot: entered TikiTerm.__init__()...")

        inst.role = role        # Remember the role string that was passed into initializer.

            #-----------------------------------------------------------------------------
            # Create the mutual exclusion lock for thread-safe manipulation of our state.
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        inst.lock = RLock()     # Reentrant mutex lock for changing terminal state.

            #-----------------------------------------------------------------------
            # Create condition flags to allow other threads to block while waiting
            # for certain important changes in the state of the TikiTerm object.
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        inst.dying     = Flag()     # Raise this flag when the terminal begins to die.
        inst.destroyed = Flag()     # Raise this flag when it has finished being destroyed.

            #--------------------------------------------------------------------------
            #  The remaining initialization is all done within the context of our re-
            #  entrant mutex lock being locked, to make sure that no one else tries
            #  mucking around with the state of this terminal object while it's still
            #  in the process of being initialized.  This sort of thing helps to make
            #  sure that the TikiTerm object's state, as seen by other threads, is
            #  always self-consistent.
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        with  inst.lock:         # In the context of the acquired mutex lock,

                #---------------------------------------------------------------
                # If no master (enclosing) widget was provided, then create one
                # for ourselves as a new toplevel window.  Give it the provided
                # title, or a default title specific to TikiTerm.

            if master is None:  master = TopWin(title=title)

                #-----------------------------------------------------------------
                # Initialize our underlying ScrolledText widget, using the master
                # widgets and the remaining arguments to this initializer.
        
            ScrolledText.__init__(inst, master=master,
                                  fg=fg, bg=bg, insertbackground=insertbackground,
                                  width=width, height=height)
                    # (Tells our ScrolledText superclass what other widget this
                    # widget is nested inside, and gives it other arguments that
                    # ScrolledText knows how to handle.)

                #--------------------------------------------------------------------
                #  Bind the TkInter "<Destroy>" event (the destruction of this widget)
                #  to invoke a special extra method of ours for announcing this event
                #  to stakeholders who may be interested in it.

            inst.bind("<Destroy>", inst._gotDestroyEvent, add=True)

                #---------------------------------------------------------------
                #  Specify layout for this widget within its parent widget.
                #  Note: This is where the widget actually first gets rendered
                #  (if its parent widget is already mapped).
            
            inst.pack(side=TOP, expand=YES, fill=BOTH)

                #--------------------------------------------------------------------
                # Grab the text input focus and set it to this new widget.
                # (Of course, user may click on another window to set it elsewhere.)

            inst.focus_set()

                #----------------------------------------------------------------
                # Create an initially-empty dictionary for maintaining our list
                # of text styles that have already been applied in this terminal.
            
            inst.styleDict = {}             # Initially empty style dictionary.
            inst.curstyle = None            # No style yet.
            inst.curtags = ()               # No tags yet.

#                # Test raw ScrolledText output capability (remove after debugging).
#            inst.insert(INSERT, "This is a test.\n")

                #----------------------------------------------------------
                #  Go ahead and start the TkInter GUI in the "background"
                #  (i.e., in the guibot thread) (this does nothing if it's
                #  already started).

            guigo()

                #------------------------------------------------------
                # Initialize output buffer and last-character memory.

            inst.outbuf = "";   inst.lastch = ""

                #----------------------------------------------------------
                #  Create in, out, err virtual file handles.
                #  Note that we assign different default colors 
                #  for regular vs. error output streams.

            inst.instream = TikiTerm.In(inst)
            inst.outstream = TikiTerm.Out(inst, style=style(Green))     # Revert to green when printing to outstream.
            inst.errstream = TikiTerm.Out(inst, style=style(Red))       # Just like outstream, but with red text.

                #--------------------------------------------------------
                #  Load the input area separator graphic.   Also,
                #  create the end-of-output and start-of-input markers
                #  surrounding it.


                # Insert the input-area separator graphic at the end of the buffer.
            
#            inst.insert(END, "\n")                                  # Insert NL before graphic
#            inst.insert(END,"Purple beam should be on the next line by itself.\n")
            init_graphics()                                         # Initialize global horizontal divider graphic
            inst.image_create(END, image=horiz_divider)
            inst.insert(END, "\n> ")                                  # Insert NL, prompt after graphic
#            inst.insert(END,"Purple beam should be on the previous line by itself.\n")
                # That leaves the separator on a line by itself, between output & input.

            inst.mark_set(START_INPUT, "2.2")       # Create start-input mark after separator.
            inst.mark_gravity(START_INPUT, LEFT)    # Make the start-input mark have LEFT gravity.
                # This means that when textever is inserted at the mark, the mark stays at
                # the left end of the text.
            inst.mark_set(INSERT, START_INPUT)      # Put insertion point at start of input area.

                # Create the end-output marker at the start of the buffer, just
                # before the separator.
            inst.mark_set(END_OUTPUT, "1.0")          # Create end-output mark at start of buffer.
            inst.mark_gravity(END_OUTPUT, RIGHT)
                # By default, the end-output mark has RIGHT gravity, meaning that whenever
                # text is inserted there, the mark stays at the end of the text.  

                #----------------------------------------------------------
                #  Set up event handlers to enforce that the insertion
                #  point must remain within the input area.  Generally, 
                #  we just want to add new handlers ("+" option) without
                #  unbinding the existing ones.

            inst.bind("<ButtonRelease-1>", inst._fixInsPt, "+")
                # The reason we bind ButtonRelease instead of Button is to
                # allow user to still select text regions (useful, e.g., for
                # copy-and-paste to other windows).
                
                # Here, we need to override <BackSpace> completely to avoid
                # the possibility of deleting characters before START_INPUT.
                # (Except this doesn't actually override the default behavior!)
            inst.bind("<BackSpace>", inst._carefulBS, add=None)
                # Generally, other keys we leave alone, & allow them
                # to take their default bindings (except for the below).

            inst.bind("<Control-c>", inst._break)

            inst.bind("<Key>", inst._fixInsPt, "+")
                # After each keypress, make sure the insertion point has not
                # somehow wandered outside of the input area.  Normally this
                # would only happen on an up-arrow keypress, but just in case
                # there are other keys that would do it, handle all of them.

                # Here, we need to add a binding to the <<Selection>> virtual
                # event to make sure that the selection area doesn't straddle
                # the end-output to start-input region.  Not yet implemented.
#            inst.bind("<<Selection>>", inst._fixSel, "+")

                #-----------------------------------------------------------
                #  Here, we add a binding to the <Return> keypress for the
                #  specific purpose of transferring the contents of the
                #  input area (now the user has finished his line editing)
                #  to the input buffer, so that readers can access it, as
                #  well as to the output area, in a designated color (say,
                #  yellow) so that it can be seen appropriately interspersed
                #  with the output that is coming in to the terminal window.
                #
                #  Well, it might be more elegant to put the input into a
                #  temporary area of the window between output & input areas,
                #  and then transfer it to the output area only after the
                #  text is actually consumed by a reader client.  But, let's
                #  not worry about all that extra complexity for now!
                #
                #  Some notes:
                #       put(text, style=style(Yellow))

            inst.bind("<Return>", inst._sendUserInput)

                # Set the input hook (to handle entered text lines).

            if in_hook == None:
                logger.debug("Installing default input hook.")
                in_hook = inst._defaultInputAction      # Initialize input hook to default if not privided.
            else:
                logger.debug("Installing input hook: " + str(in_hook))
            inst.in_hook = in_hook                                      # Install input hook.

                #-------------------------------------------------------
                #  Create new outputDriver worker thread.  This thread
                #  is responsible for accepting, serializing, and
                #  processing output requests to this terminal.

            inst.outputDriver = Worker(onexit=inst.destroy, role=(inst.role + "consDrv"))     
                # Tell it, when it's exiting, to go ahead and destroy this whole TikiTerm widget
                # (if not already destroyed).  (When we have no console driver, we're no longer
                # useful.

    #|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #|  End method TikiTerm.__init__().
    #|-----------------------------------------------------------------------------------------

        # Default thing to do with input lines (besides echo them to output area).
        # Just append them to our input buffer.

    def _defaultInputAction(inst, input_line):
        inst.instream.append(input_line)

        # Transfer the copy of the input area into the input buffer, and also
        # echo it in yellow to the output buffer.

    def _sendUserInput(this, event):

            # Make sure we're in the guibot thread before doing any graphics stuff.
        
        if not ambot(): return guibot(this._sendUserInput)
        
        with this.lock:     # Mutex lock for thread safety.

            text = this.get(START_INPUT, END)       # Get contents of input area.

            logger.info("User entered this line: " + repr(text) + ".")

            this.delete(START_INPUT, END)           # Clear the input area.

#            this.instream.append(text)              # Send text to input buffer.
            this.in_hook(text)                       # Call the input hook to do 'whatever' with the text.
                #  \_ By default, this sends it to our line input stream.

            this.put(text, style(Yellow))           # Echo input to output area, in yellow.

            guibot.do(lambda: this.event_generate("<BackSpace>"))      # Force backspace over newline just entered.

    # End method TikiTerm._sendUserInput().
        

    def _gotDestroyEvent(this, event):
        # We're doing this just to figure out when the <Destroy> event is received.
#        print("TikiTerm._gotDestroyEvent()",file=sys.__stdout__)
        logger.debug("TikiTerm._gotDestroyEvent(): Running this (null) <Destroy> event handler.")

        #----------------------------------------------------------------------------------
        #   grab_stdout(), grab_stderr(), grab_stdouterr()      [instance public methods]
        #
        #       These methods allow the customer to reassign his system STDOUT
        #       and/or STDERR output streams to display on the present TikiTerm
        #       widget instead of to whatever file they went previously (with
        #       text in their respective colors).
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def  grab_stdout(this):
        sys.stdout = this.outstream
        this.has_stdout = True             # Remember that we've grabbed stdout.

    def  grab_stderr(this):
        sys.stderr = this.errstream
        this.has_stderr = True             # Remember that we've grabbed stderr.

    def  grab_stdin(this):
        sys.stdin = this.instream
        this.has_stdin = True              # Remember that we've grabbed stdin.

    def  grab_stdio(this):
        this.grab_stdout(); this.grab_stderr(); this.grab_stdin()

        #------------------------------------------------------------------------------
        #   amDriver()                                      [instance private method]
        #
        #       This little internal utility method just tells us whether
        #       we are currently in the output driver worker thread, as
        #       opposed to some other thread.
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def  amDriver(this):  return  current_thread() == this.outputDriver    

        #------------------------------------------------------------------------------
        #
        #   declareStyle()                                  [instance public method]
        #
        #       Declares that the given style is one that will be used in this
        #       app instance.  Adds it to styleDict if an equivalent style is
        #       not already present.  Although this method is public, normally
        #       this is done automatically and the user doesn't need to worry
        #       about it.  Note: This method may be called from any thread;
        #       it switches between threads as needed to accomplish its work.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def  declareStyle(inst, style:TikiTermTextStyle):

            #--------------------------------------------------------------
            #  The below if/elif/else construct divides up work to be done
            #  in different threads.  This first 'if' clause handles the
            #  work that needs to be done from within the guibot thread.
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        if  ambot():             # If we're in the guibot thread,

                #---------------------------------------------------------
                #  If the style's not already in our dictionary, switch
                #  temporarily to the output driver thread and add it to
                #  the dictionary.

            if style.tagName not in inst.styleDict:
                return outDriver.getResult(lambda: inst.declareStyle(style))

                #-----------------------------------------------------------
                # Configure the foreground color for this style's text tag.
                
            inst.tag_config(style.tagName, foreground=style.fgColor)

                #-----------------------------------------------------------
                #  Configure the background color (if any was provided) for
                #  this style's text tag.
                
            if style.bgColor != None:
                inst.tag_config(style.tagName, background=style.bgColor)

            #-------------------------------------------------------------------
            #  This 'elif' clause handles the work that needs to be done from
            #  within this terminal's console output driver thread.
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        elif  inst.amDriver():       # If we're in the console output driver thread,

                #------------------------------------------------------------------
                #  This temporary Boolean variable 'addIt' is to help us avoid
                #  a deadlock situation that could occur if we switched between
                #  threads while holding onto the TikiTerm object's instance lock.

            addIt = False   # We haven't yet determined that this is a newly-added style.

                #------------------------------------------------------------------
                #  Lock this TikiTerm instance while adding the new style to the
                #  dictionary (if needed), to ensure that this gets done as an
                #  atomic operation and the style doesn't end up getting added
                #  twice.  Remember whether this is a newly added style or not.
            
            with inst.lock:                                 # With instance lock,
                if style.tagName not in inst.styleDict:     # Not in style dictionary yet?
                    addIt = True                            # Remember we need to configure the tag still.
                    inst.styleDict[style.tagName] = style   # Add it.

                #-------------------------------------------------------------
                #  Now, if it turned out the style *was* newly added to the
                #  dictionary above, then we need to make sure that the
                #  TkInter tag is actually configured.  This must happen in
                #  the guibot thread.  (If it happens twice, no worries.)

            if addIt:   # If we're just now adding it to the style dictionary,
                
                # Switch into GUI thread for safety of .tag_config().
                if not ambot(): return guibot(lambda: inst.declareStyle(style))

            #----------------------------------------------------------------
            #  This final 'else' clause handles the case where this method
            #  might have been called from a thread other than the guibot
            #  thread or the terminal's output driver thread.  In that case,
            #  switch over to the output driver thread and continue there.
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        else:

            return outDriver.getResult(lambda: inst.declareStyle(style))
        
    #|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #|  End method TikiTerm.declareStyle().
    #|------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        #
        #   unprintable()                                   [class public function]
        #
        #       Return True if the given character does not have a unique
        #       graphical representation on this terminal using the default
        #       font.  Excepted are space (32), line feed (10), carriage
        #       return (13), and tab (9) - these all appear as whitespace,
        #       but that is what is desired.  Characters 2-8, 11-12, 14-27,
        #       and 161-255 are not standard 7-bit ASCII, but they do cause
        #       unique glyphs to be rendered in our TkInter environment.
        #       Thus the only truly unprintable characters are in our
        #       environment are code points 0, 1, 28-31, and 127-160.  (We
        #       ignore the possibility that we may be running in a Unicode
        #       environment.)
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        
    def unprintable(ch:str):
        byte = ord(ch)
        return ((0 <= byte <= 1) or
                (28 <= byte <= 31) or
                (127 <= byte <= 160))

        #--------------------------------------------------------------------------
        #
        #   putch()                                     [instance private method]
        #
        #       This method writes a single character to the display.
        #       Actually, it only buffers up the character for display;
        #       flush() must be called later to actually send the
        #       buffered text to the display.  putch() is not capable
        #       of setting the character style; for that, use put().
        #       putch() may be called efficiently from within any
        #       thread - it does not need the guibot or outputDriver
        #       workers.  (However, if you want to wait till a previous
        #       flush() is completed, use put() instead.)
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def putch(this, char:str):
        
        with this.lock:         # Lock the instance to ensure consistent state changes.

                #--------------------------------------------------------------
                #  The following if/elif/else construct handles certain
                #  types of characters specially.
                #
                #  Our semantics for handling carriage return / line feed is
                #  as follows:  Either carriage return or line feed will move
                #  the cursor to the start of the next line, except that if
                #  the previous character was the other kind (i.e., the first
                #  member of a CR/LF or LF/CR sequence), the current character
                #  (the second member of the pair) is ignored.
                #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
            
            if  char == '\r' or char == '\n':  # Carriage return or line feed?
                
                    # Compare it against the previous (just-printed) character.
                    
                if (char == '\r' and this.lastch != '\n' or     # Note: Correctness of this expression depends on
                    char == '\n' and this.lastch != '\r'):      # "and" having higher precedence than "or".
                        
                        # If the previous character was not the OPPOSITE line-end character (CR vs. LF), do newline.
                        
                    this.outbuf += "\n"
                    
                else:   # Consider this character the 2nd member of a CRLF/LFCR pair; ignore it.
                    
                    this.lastch = ""    # Clear <lastch> so an immediately following CR/LF will work.
                    return              # Return early so lastch doesn't get set by the line after the if/elif/else.
                        # (It's OK that this skips the long-buffer-flush check, because this
                        # case can't even happen more than once without other cases in between.)

                #--------------------------------------------------------------------
                #  Tab characters are now converted to spaces in flush(), so
                #  the clause below to handle tab specially is no longer necessary.
                
    # We still need to figure out how to properly handle tabs in output to ScrolledText.
    #        elif char == '\t':      # Horizontal Tab.
    #            # Move forward to next 8-column-wide tab stop position.
    #            self.col = (int(self.col / 8) + 1)*8

                #-----------------------------------------------------------------------------------
                #  Case for displaying unique representations of otherwise-unprintable characters.
    
            elif  TikiTerm.unprintable(char):            # For unprintable characters,
                this.outbuf += "[%02x]" % ord(char)         # print their hex codes in [brackets].

                #--------------------------------------------------------
                #  Default case, for all normal (printable) characters.
                
            else:       # Everything else, treat it as printable.
                
                this.outbuf += char     # Just add it to out output buffer.

            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # End of if/elif/else construct to dispatch on character type.
            #--------------------------------------------------------------

            this.lastch = char      # Remember that this character was the last one sent.

                #--------------------------------------------------------------------
                #  If the buffer is getting pretty big, then go ahead and output
                #  its contents early.  This prevents excessively long output
                #  delays in the case where a large contiguous block of text is
                #  sent to the terminal all at once.
            
            if len(this.outbuf) >= 128:     # Overhead for sending 2^7 chars is negligible.
                this.flush()                # So go ahead and flush them.

    # End method putch().
    #---------------------

        #----------------------------------------------------------------------
        #
        #   _raw_write()                            [instance private method]
        #
        #       This method does the actual raw, low-level work of
        #       writing buffered text to the underlying ScrollableText
        #       widget.  It does its work in the guibot worker thread.
        #       Users of TikiTerm should never call this method
        #       directly.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def _raw_write(this):
        if not ambot(): return guibot(this._raw_write())

        #------------------------------------------------------------------
        #
        #   _flush_to_stdio()                   [instance private method]
        #
        #       This method is called when an attempt is made to
        #       flush output to a terminal that is in the process
        #       of shutting down.  To avoid losing this output
        #       entirely, we redirect it to the system's default
        #       stdout/stderr streams instead.
        #
        #       WARNING: The method for deciding which text goes to
        #       stderr as opposed to stdout is kludgey.  Basically,
        #       if the tags list is (Red) - meaning red foreground
        #       color - then we send the output to stderr, otherwise
        #       we send it to stdout.  This might not be correct
        #       though if the user wrote some text in red for other
        #       reasons besides that it was stderr output.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def _flush_to_stdio(this, text, tags):

        #-------------------------------------------------------------
        #  We avoid using the current stdout/stderr globals in case
        #  they are still bound to the terminal streams.  Use system
        #  defaults instead.

        if tags == (Red):                               # If text is being printed in red,
#            logger.warn("%s: TikiTerm._flush_to_stdio(): Terminal is dying; flushing text [%s] to __stderr__ instead..."%(current_thread(),text))
            print(text, end='', file=sys.__stderr__)        # Send it to system stderr;
            sys.__stderr__.flush()                          # Make sure it's flushed.
            
        else:                                           # otherwise,
#            logger.warn("%s: TikiTerm._flush_to_stdio(): Terminal is dying; flushing text [%s] to __stdout__ instead..."%(current_thread(),text))
            print(text, end='', file=sys.__stdout__)        # Just send it to system stdout.
            sys.__stdout__.flush()                          # Make sure it's flushed.

    # End TikiTerm._flush_to_stdio().
    #--------------------------------

        #------------------------------------------------------------------------
        #
        #   flush()                                     [instance public method]
        #
        #       Flushes any buffered output to the display using the
        #       current text style.  Does the actual GUI work in the
        #       guibot thread, for thread-safety.  
        #
        #       NOTE: It is important that a "flush" task never be
        #       sent to the guibot other than by this method itself,
        #       which appropriately locks the tikiterm and clears
        #       the output buffer, to maintain a consistent state.
        #
        #       The <text> & <tags> arguments are only used by the
        #       outputDriver thread when sending text to be printed
        #       to the guibot thread from within this same method.
        #       No other callers should use those arguments.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def flush(this, text:str=None, tags:list=None):
#TMI        print(current_thread().name,": TikiTerm.flush(%s)"%text,file=sys.__stdout__)

            #----------------------------------------------------------------------------------------
            #  GUIBOT THREAD
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        
        if ambot():                 # In guibot thread?
#TMI            print("guibot: TikiTerm.flush(): Actually inserting [%s]..." % this.outbuf)

                #----------------------------------------------------------------
                #  Here's where we actually tell the widget to display the text.
                #  We would be REALLY well-advised to make sure the text widget
                #  has not been destroyed before we try doing this, to better
                #  handle cases where we are shutting things down due to an
                #  exception, but some of the exception-handling/exiting code
                #  has already sent messages to the TikiTerm console window
                #  which the guibot is in the middle of trying to process.

            if text==None or text=="": return   # Nothing to flush.
            if this.dying:                      # Is this widget in the process of being torn down?
#                logger.warn("guibot: TikiTerm.flush(): Warning: Terminal is dying; "
#                           "re-routing console log output back to default stdio...")
#                logger.warn("guibot: TikiTerm.flush(): Warning: Terminal is dying; "
#                           "sending output [%s] to stdio instead..." % text.strip())
#                print("guibot: TikiTerm.flush(): Warning: Terminal is dying; "
#                      "sending output [%s] to stdio instead..." % text,
#                      file=sys.__stdout__)
                this._flush_to_stdio(text, tags)
                return                          # Don't do the usual widget operation.
            this.insert(END_OUTPUT, text, tags);       # Output the text using the current tags.
                # We insert it at the end of the output area of the terminal.
            this.see(END)                       # Make sure text that was just output is visible.

            #  NOTE TO SELF:  We really need to do something above where we deal specially with any
            #  text that may be being manually typed by the user into the ScrollableText widget.
            #  For example, we should probably insert any new output BEFORE the line that the user
            #  is currently typing, so that we don't break up the line that the user is typing, and
            #  it all remains contiguous and at the end of the buffer.  But first, we also need to
            #  make sure that the user can't place the insertion point somewhere in the middle of
            #  the text already in the widget.  We only want to user to be able to type new text at
            #  the very end of the widget, or at least only within a line that he is currently
            #  editing.  When he hits return, the line typed should be locked into place and sent
            #  to the TikiTerm's input buffer, so that client threads can read it.  A flag should
            #  be raised when input is available to allow those threads to unblock.  Also the line
            #  just typed should probably be changed to a different color (say, from white to yellow)
            #  to denote that it has the status now of being locked-in input.

            #-------------------------------------------------------------------------------------------
            #  OUTPUT DRIVER THREAD
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
            
        elif current_thread() == this.outputDriver:     # In outputDriver thread?
#            print(current_thread(),": TikiTerm.flush(): Asking guibot to flush [%s]..." % this.outbuf)
            with this.lock:                         # Atomically for this tikiterm object,
                text = this.outbuf.expandtabs()         # Expand tabs to spaces
                tags = this.curtags                     # Get current buffer's tags
                this.outbuf = ""                        # Then clear the output buffer. (Consume text.)
                if text==None or text=="": return       # Nothing to print? Quit early.
                if this.dying:                          # If we're dying (can't print to terminal),
                    this._flush_to_stdio(text, tags)        # Print text to stdio instead.
                    return                                  # & quit early.

                    #-----------------------------------------------------------------------------
                    #  The reason we go ahead and send the text as an argument to the below
                    #  lambda, rather than having the guibot retrieve it directly from outbuf,
                    #  is so that we don't have to wait for the guibot to finish before we
                    #  release the instance lock - since that would deadlock in some situations,
                    #  such as when guibot raises an exception that causes error messages to be
                    #  sent via stderr back to the tikiterm, which then gets hung up trying to
                    #  get a response from the guibot.

                guibot.do(lambda:this.flush(text,tags))     # Have the GUI worker thread do the real work.

            #----------------------------------------------------------------------------------------------
            #  OTHER THREADS
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
                
        else:                       # In some other thread?
            
            with this.lock:             # This "with" is to avoid going thru outputDriver if 
                if this.dying:              # we can't really print to the terminal anyway cuz it's dying.
                    this._flush_to_stdio(this.outbuf,this.curtags)
                    this.outbuf = ""    # Clear buffer.
                    return

                #-------------------------------------------------------------------
                #  We need to ask the output driver thread to do the flush
                #  asynchronously in the background, so that the original caller
                #  (writer thread) doesn't block until flush completion - if it
                #  did, then guibot would be unable to trigger a flush of its own
                #  error messages.  So, flush() from other threads doesn't really
                #  mean "flush now", it means, "flush when you get around to it."
                #  BE AWARE THAT THIS IS DIFFERENT FROM THE SEMANTICS THAT FLUSH()
                #  MIGHT HAVE FOR OTHER TYPES OF STREAMS.
                
            try:
                this.outputDriver.do(this.flush)
                
            except  WorkerExiting:   # Output driver is in process of shutting down.
                
                    #-----------------------------------------------------------------------
                    #  OK, with the output driver dying, all that we can do is to flush
                    #  the data to the system console instead.  We don't really prefer
                    #  to do this in the calling thread, since output items from different
                    #  client threads might not get properly serialized, but there's not
                    #  much choice at this point.
                    
                with this.lock:     # Try our best to be thread-safe.  Hope it doesn't block!
                    this._flush_to_stdio(this.outbuf,this.curtags)
                    this.outbuf = ""    # Clear output buffer.
                    
    #|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #|  End method flush().
    #|-------------------------------------------------------------------------------------------

        #----------------------------------------------------------------------------------------
        #
        #   put_dying()                                             [instance private method]
        #
        #       This version of put() is used when the GUI is in the process
        #       of shutting down.  It redirects the output to system stdout/
        #       stderr instead of trying to use the doomed TikiTerm.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        
    def put_dying(this, text, style:TikiTermTextStyle = None):     # Call from guibot for consistency?

            #-----------------------------------------------------------------------------
            # If we're not in the guibot, and the guibot's not already exiting,
            # have it do the work, for purposes of consistent sequential ordering
            # of this output relative to surrounding log messages in TikiTerm.destroy(),
            # also output by the guibot thread.

        if not ambot():
            with guibot.lock:               # Need for atomicity.  Hope it doesn't block.
                if not guibot.exiting:                          
                    return guibot.do(lambda:this.put_dying(text,style))

            #-------------------------------------------------------------------
            # Otherwise, just go ahead and do it ourselves.  This might result
            # in overlapping lines in the output stream, but, oh well...

        if style.fgColor==Red:
#            print("TikiTerm.put_dying(): About to print text [%s] to real stderr." % text, file=sys.__stdout__)
            print(text, file=sys.__stderr__)
            
        else:
#            print("TikiTerm.put_dying(): About to print text [%s] to real stdout." % text, file=sys.__stdout__)
            print(text, file=sys.__stdout__)
            
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #  End method put_dying().
    #-------------------------------------------


        #--------------------------------------------------------------------------
        #   put()                                       [instance public method]
        #
        #       Displays the text <str> in the TikiTerm widget using
        #       text style <style>.  This is done atomically in the
        #       outputDriver thread, so that characters from multiple
        #       put() calls don't get mixed up with each other.
        #
        #       To prevent recursive inter-thread RPC deadlocks when
        #       guibot calls put(), the put() does not wait for the
        #       output operation to be completed before returning.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def put(this, text:str, style:TikiTermTextStyle = None):

#        print(current_thread(),"TikiTerm.put(): I'm inside the put() function, with argument [%s]" % text)

            #--------------------------------------------------------------
            #  Effectively switches temporarily to the outputDriver thread.
        
        if (current_thread() != this.outputDriver):
#            print(current_thread(), "TikiTerm.put(): Switching to outputDriver thread...")
            return this.outputDriver.do(lambda: this.put(text,style))
#        else:
#            print(current_thread(), "TikiTerm.put(): Already in outputDriver thread...")

            #--------------------------------------------------------------
            #  OK, we're already in the output driver thread, so just go
            #  ahead and do the work now.
        
        with this.lock:         # Make sure the following is done atomically.

#            print(current_thread(), ": TikiTerm.put(): Acquired the terminal lock...")

                #---------------------------------------------------------
                # Figure out the text style and correponding TkInter tag.
            
            tags = None                     # If no style is given, apply no new tags.
            if style != None:               # If a style is given,
                this.declareStyle(style)    #   make sure a tag is configured for it,
                tags = (style.tagName)      #   and make sure we'll use that tag.

                #---------------------------------------------------------
                # Remember style and tags for when we do a flush() later.
            
            this.curstyle = style;      this.curtags = tags

                #--------------------------------------------------------------
                #  Process all characters in the string.  This does some simple
                #  text transformations, such as for CR/LF sequences.
            
            for ch in text[:]:  # For each character in the string,
                this.putch(ch)      # process it into our output buffer.

                #--------------------------------------------------
                #  Flush the output buffer to the terminal display.
                #  This uses the current style/tags.
            
            this.flush()    

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #  End method TikiTerm.put().
    #------------------------------

        #--------------------------------------------------------------------------
        #   _carefulBS()                                [private instance method]
        #
        #       This method is a replacement for the TkInter Text widget's
        #       default handler for the <BackSpace> key press event, which
        #       checks to make sure we are beyond the start of the input
        #       region before allowing the deletion to occur.
        #
        #       Note:  There is a funny thing where we can't seem to override
        #       the default <BackSpace> behavior, so instead we prevent it from
        #       doing anything by inserting a dummy character for it to delete.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def  _carefulBS(this, event):

            #-----------------------------------------------------------------
            # See if we are in the area where we want to suppress the BS key
            # from doing anything - that is, at the start of the input area.
            
        if this.compare(INSERT + " + 0 indices", "<=", START_INPUT + " + 0 indices"):
            
                # This warning is for diagnostic purposes only; change it to INFO later.
                
            logger.warn("TikiTerm._carefulBS(): Ignoring backspace key at start of input area.");

                # Here, we suppress the backspace action by inserting a dummy
                # character for it to delete.  Which character doesn't matter.
            
            this.insert(INSERT,"#")     # Dummy character to delete


        #--------------------------------------------------------------------------
        #   _fixInsPt()                                 [private instance method]
        #
        #       Fix insertion point.  Makes sure that the insertion point
        #       is located within the insert area.  If it somehow got to
        #       a point before the insert area, move it fowards to the
        #       start of the insert area.
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def  _fixInsPt(this, event):                        # event is ignored
        if this.compare(INSERT, "<", START_INPUT + " + 0 indices"):
            this.mark_set(INSERT, START_INPUT + " + 0 indices")

        #--------------------------------------------------------------------------
        #
        #   set_title()                                 [public instance method]
        #
        #       Change the top-level window's title to the desired string.
        #       This task is completed asynchronously by the guibot thread.
        #       Does nothing if this same title was already the most recent
        #       one requested through this method.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        
    def  set_title(this, title:str):

            # As a minor optimization, we don't bother to queue up a title-
            # change request in the guibot's worklist if we previously
            # requested this very same title.
        
        if not hasattr(this, 'requested_title') or title != this.requested_title:
            this.requested_title = title
            
            guibot.do(lambda: this.winfo_toplevel().title(title))


        #--------------------------------------------------------------------------
        #
        #   closewin()                                  [public instance method]
        #
        #       Closes the entire top-level window within which this
        #       particular TikiTerm widget is embedded.  Warning: This
        #       action may destroy other widgets as well, if they are
        #       in the same top-level window.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def  closewin(this):
        logger.debug("TikiTerm.closewin(): Telling guibot to close terminal's toplevel window...")
        guibot.do(lambda: this.winfo_toplevel().destroy())  # Destroy its parent widget.
            # (Hopefully this is its window, but maybe we should make sure?)
        logger.debug("TikiTerm.closewin(): We're returning, trusting in the guibot to do its job...")           

    def _break(this, event):
        this.closewin()

        #--------------------------------------------------------------------------------
        #
        #   destroy()                                           [public instance method]
        #
        #       This TkInter widget-destructor method is called automatically
        #       by TkInter whenever this widget is being destroyed, directly
        #       or in the process of tearing down one of its ancestor widgets.
        #       We do our best to shut down neatly and clean up after ourselves.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def destroy(this):  # Need to make sure we're in the guibot thread before doing this.

#        print("%s entered TikiTerm.destroy()..." % current_thread(),file=sys.__stdout__)
        logger.debug("%s entered TikiTerm.destroy()..." % current_thread())

        if not ambot():     # Make sure we're in the worker thread.

                # Delegate job to guibot thread - but don't want for it (avoid deadlocks).

            guibot.do(this.destroy)

                # These messages are commented out b/c now we just delegate the task
                # to the worker thread instead.

#            print("TikiTerm.destroy(): Error: An attempt was made to call this method from\n"
#                  "\ta thread other than the guibot thread.  This is not yet supported.\n"
#                  "\tUse an expression like 'guibot(term.destroy)' instead.  Ignoring request.",
#                  file=sys.__stdout__)
#            logger.error("TikiTerm.destroy(): An attempt was made to call this method from\n"
#                  "\ta thread other than the guibot thread.  This is not yet supported.\n"
#                  "\tUse an expression like 'guibot(term.destroy)' instead.  Ignoring request.")

            return  # Task delegated; nothing left for us to do.

            #----------------------------------------------------------------------------
            #  Avoid duplicate calls to this function for the same widget.
            #  The assignment here is important to make sure that setting & checking the
            #  previous state of the "dying" flag is done as one atomic operation.

        wasAlreadyDying = this.dying.rise()     # Tell the world that we're dying.

            #-----------------------------------------------------------------------------
            #  This prevents us from going on to the rest of this function more than once
            #  for a given terminal instance.
        
        if wasAlreadyDying:
#            print("TikiTerm.destroy(): Warning: This method was called after the "
#                  "terminal was already dying.  Ignoring request.", file=sys.__stdout__)
            logger.info("TikiTerm.destroy(): Note: This method was called after the "
                        "terminal was already dying.  Ignoring request.")
            return

            #-------------------------------------------------------------------------
            #  Make sure that this widget hasn't already been destroyed!  If so, then
            #  there's nothing for us to do.

        if this.destroyed:
#            print("TikiTerm.destroy(): This terminal has already been destroyed!  Ignoring request.\n",file=sys.stderr)
            logger.warn("TikiTerm.destroy(): This terminal has already been destroyed!  Ignoring request.")
            return

            #--------------------------------------
            # Close the user input buffer stream.

        if hasattr(this, 'instream'):
            this.instream.close()       # Tells any stream waiters we're at "end of file"
        
            #------------------------------------------------------------
            #  Change system stdout/stderr back to their default values
            #  if they had been reassigned to this TikiTerm.

#        print("TikiTerm.destroy(): Restoring system stdout/stderr...",file=sys.__stdout__)

        if hasattr(this, 'has_stdout') and this.has_stdout:                     # hasattr() in case attribute is uninitialized
            logger.debug("TikiTerm.destroy(): Restoring system stdout...")
            sys.stdout = sys.__stdout__

        if hasattr(this, 'has_stderr') and this.has_stderr:
            logger.debug("TikiTerm.destroy(): Restoring system stderr...")            
            sys.stderr = sys.__stderr__

        if hasattr(this, 'has_stdin') and this.has_stdin:
            logger.debug("TikiTerm.destroy(): Restoring system stdin...")

            #--------------------------------------------------------------------
            #  Change our our outstream/errstream writer methods to just use
            #  stdout/stderr instead.

#        print("TikiTerm.destroy(): Redirecting terminal outstream/errstream to stdout/stderr...",file=sys.__stdout__)
        logger.debug("TikiTerm.destroy(): Redirecting terminal outstream/errstream to stdout/stderr...")
        this.outstream.write = sys.stdout.write
        this.errstream.write = sys.stderr.write
        this.instream.readline = sys.stdin.readline

            #------------------------------------------------------------------------------------
            # Change our own put() method to one that just uses stderr instead of outputDriver.

#        print("TikiTerm.destroy(): Reprogramming our put() method...",file=sys.__stdout__)
        logger.debug("TikiTerm.destroy(): Reprogramming our put() method...")
        this.put = this.put_dying

            #-------------------------------------------------------
            # Tell our output driver not to accept any new output.
            
#        print("TikiTerm.destroy(): Closing outputDriver queue...",file=sys.__stdout__)
        logger.debug("TikiTerm.destroy(): Closing outputDriver queue...")
        this.outputDriver.close()

            #-------------------------------------------------------------------------------
            #  Commented this out b/c there could still be important messages in the output
            #  queue (including, if console debugging is on, the debug messages above!) 
            #  that we need to process.  If we exit the output driver too early, they will
            #  never get printed.  Instead, we let the output driver go ahead and process
            #  them, but send the messages to stderr instead of to the console.
            
#       # Tell the existing output driver to exit; its not to try processing any more items.
#       this.outputDriver.exitRequested.rise()

            #-------------------------------------------------------------------------------
            #  The following is commented out because it caused deadlocks; outputDriver
            #  might be waiting for guibot at the moment, but the .join() below causes us
            #  (in guibot) to in turn wait for outputDriver.  Instead of doing it this way,
            #  now we just let outputDriver asynchronously finish processing its requests,
            #  but send them to the "real" system stdout/stderr instead of the TikiTerm.

#        print("TikiTerm.destroy(): Flushing queued output to real stdout",file=sys.__stdout__)
#        
#        # Wait for our output driver to finish.
#        if this.outputDriver.todo!=None:
#            print("TikiTerm.destroy(): About to do outputDriver.todo.join() with qsize()=%d" % this.outputDriver.todo.qsize(),file=sys.__stdout__)
#            this.outputDriver.todo.join()

            #-----------------------------------------------------------------------------
            #  Here we dispatch the destroy() method to our ScrolledText superclass so
            #  that it can do whatever cleanup it needs to do.

#        print("TikiTerm.destroy(): Destroying underlying ScrolledText widget...",file=sys.__stdout__)
        logger.debug("TikiTerm.destroy(): Destroying underlying ScrolledText widget...")
        ScrolledText.destroy(this)

            #---------------------------------------------------------------------------
            #  At this point, we're done destroying ourselves, and we can go ahead and
            #  tell anyone who was waiting for that to happen that they can breathe a
            #  sigh of relief.

#        print("TikiTerm.destroy(): Announcing that this terminal has been destroyed...",file=sys.__stdout__)
        logger.debug("TikiTerm.destroy(): Announcing that this terminal has been destroyed...")
        this.destroyed.rise()   # Announce we have been destroyed.

    #|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #|  End method TikiTerm.destroy().
    #|----------------------------------------------------------------------------------------------------------

# I don't think the below is really needed, and it just creates extra
# superfluous destroy events in the log.  Thus it's commented out.
#
##            #===================================================================
##            #   Destructor method.                  [special instance method]
##            #
##            #       Handles object destruction (just before memory for
##            #       the object is deallocated).
##            #
##            #       Note: This does not get called at a predictable time,
##            #       unfortunately, because python does not guarantee the
##            #       order of object deletion - it happens whenever the
##            #       last reference to this object goes away.
##
##    def __del__(this):
##
##        this.destroy()  # Destroy the widget, if not already destroyed.
##
##            # Go ahead and do superclass deletion. (The other superclass,
##            # Terminal, doesn't have anything to do.)
##            
##        ScrolledText.__del__(this)

#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#|  End TikiTerm class.
#|================================================================================================================================

    #------------------------------------------------------------
    #  Install TikiTerm as the default implementation class for
    #  the Terminal class's factory function.

Terminal.defImplClass = TikiTerm

    #-------------------------------------------------------
    #  Old testing stuff below here.  Uncomment if needed.

##def doTest(term:TikiTerm):
##    print("I created the new terminal.  Pausing 5 secs before I start using it...\n")
##    sleep(5)
##    print("Here goes the first put() attempt...\n")
##    term.put("Thread [%s]:  In 5 seconds, I'm going to do a series of tests...\n" % current_thread().name)
##    print("Returned from the first put().\n")
##    sleep(5)
##
##    term.put("Hello world.  This is a light blue on gray string ending in CR.\r",
##           style(Blue,DarkGray))
##
##    sleep(0.5)
##
##    term.put("Hello world.  This is a light green string ending in LF.\n",
##           style(Green))
##
##    sleep(0.5)
##
##    term.put("Hello world.  This is a light red string ending in CRLF.\r\n",
##           style(Red))
##
##    sleep(0.5)
##
##    term.put("Hello world.  This is a light magenta string ending in LFCR.\n\r",
##           style(Magenta))
##
##    sleep(0.5)
##
##    term.put("Hello world.  Here are two newlines generated by CRLFCRLF:[\r\n\r\n]\n")
##
##    sleep(0.5)
##
##    term.put("Hello world.  Here are some strings with tabs:\n")
##    sleep(0.5)
##    term.put("0\t[\n")
##    sleep(0.5)
##    term.put("01\t[\n")
##    sleep(0.5)
##    term.put("012\t[\n")
##    sleep(0.5)
##    term.put("0123\t[\n")
##    sleep(0.5)
##    term.put("01234\t[\n")
##    sleep(0.5)
##    term.put("012345\t[\n")
##    sleep(0.5)
##    term.put("0123456\t[\n")
##    sleep(0.5)
##    term.put("01234567\t[\n")
##    sleep(0.5)
##    term.put("012345678\t[\n")
##    sleep(0.5)
##    term.put("0123456789\t[\n")
##    sleep(0.5)
##
##    term.put("Here is a dim white line exactly 80 characters long:\n")
##    sleep(0.5)
##    term.put("01234567890123456789012345678901234567890123456789012345678901234567890123456789", style(LightGray))
##    sleep(0.5)
##    term.put("Here's what happens if we add text without a CR/LF.\n")
##    sleep(0.5)
##    term.put("Here is a 'light black' line exactly 80 characters long:\n")
##    sleep(0.5)
##    term.put("01234567890123456789012345678901234567890123456789012345678901234567890123456789", style(DarkGray))
##    sleep(0.5)
##    term.put("\nHere's what happens if we add text WITH a newline.\n\n")
##    sleep(0.5)
##    term.put("\nHere are all character codes 0-255:\n")
##    sleep(0.5)
##    for byte in range(0,256):
##        term.put("Character #%d: [%s]\n" % (byte, chr(byte)))
###        sleep(0.05)
##    term.put('\r')
##
##    term.put("The "); sleep(0.5)
##    term.put("last "); sleep(0.5)
##    term.put("line "); sleep(0.5)
##    term.put("is "); sleep(0.5)
##    term.put("not "); sleep(0.5)
##    term.put("always "); sleep(0.5)
##    term.put("blank "); sleep(0.5)
##    term.put("either!\n"); sleep(0.5)
##
##    term.put("Now accepting user input!\n")
##    term.put("Type away (hit Esc to exit): ")
##
##t1 = None
##t3 = None
##
##def foo(n:int=1):
##    global t1, t3
##
##    doTest(t1)
##
###    sleep(15)    
##    t2 = TikiTerm(title="%s: TikiTerm Self-Test #2" % current_thread().name)
##
##    doTest(t2)
##    doTest(t3)
##
##
##if __name__ == "__main__":      # If this script is the main program,
##    # Do a little self-test.
##
##    t1 = TikiTerm(title="%s: TikiTerm Self-Test #1" % current_thread().name)
##
##    otherThread = Thread(target=foo)
###    otherThread.daemon = True
##    otherThread.start()
##
##    t3 = TikiTerm(title="%s: TikiTerm Self-Test #3" % current_thread().name)
##
##    sleep(7)
##    print("MAIN THREAD WAKING UP FROM SLEEP...\n")
##    doTest(t1)
##
##    foo(2)
##
##    


#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#|  END FILE tikiterm.py.
#|******************************************************************************************************************************************
