#*****************************************************************************
#                               TOP OF FILE
#   dyngui.py                                 [python module source code]
#
#       GUI elements specific to the Dynamic system.
#
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

import sys

import tkinter          #   _setLogoImage()  uses    PhotoImage

from logmaster import appName, doInfo, doNorm, setComponent, updateStderr

from appdefs import appName

from . import guiapp, tikiterm    #   _setLogoImage()  uses    ambot(), guibot

from . import _logger

__all__ = [
        'initGui',
        'waitGuiEnd'
    ]

# Private globals are:
#   _splashFilename
#   _guibot
#   _console

    # Select the splash logo image file, and scale factor.

#_splashFilename = "dynamic-logo.ppm"; _subsampleFactor = 3
#_splashFilename = "DYNAMIXXXX.ppm"; _subsampleFactor = 6
_splashFilename = "dynamic-splash-subtitled.ppm"; _subsampleFactor = 4

        #=========================================================
        #   setLogoImage()              [public module function]
        #
        #       Loads the COSMICi project logo from the file
        #       COSMICi-logo.ppm (binary portable pixmap file),
        #       and puts it in the main server console window,
        #       which must be passed in as an argument.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def _setLogoImage(console):
    global _logoimage

        # Make sure we're in the guibot thread.

    if not guiapp.ambot():              # If not in the guibot thread,
        _guibot(setLogoImage)         # re-call this function in it.
        return                              # Work is done.

        # Create the TkInter image object for our logo.

    _logoimage = tkinter.PhotoImage(file="images/"+_splashFilename).subsample(_subsampleFactor)
            # Easiest way to create .ppm (portable pixmap) files is with GIMP.

        # Insert the image (like a large character of text)
        # on the console.
        
    console.image_create("endout", image=_logoimage)


def initGui():
    global _guibot, _console
    
            #|====================================================
            #|  The following code initializes the GUI framework.

        #-------------------------------------------------------------
        # Declares (in the log file) that we are now working on behalf
        # of the GUI component.

    setComponent('GUI')

        #-------------------------------------------------------------
        # Create & start the guiapp module's guibot worker thread.
        # (This is done after the above b/c it may produce debug log
        # messages.)

    if doInfo:
        _logger.info("Starting the GUI application's worker thread...")

    guiapp.initGuiApp()         # This creates the guibot, in guiapp.guibot.
    _guibot = guiapp.guibot     # Private global copy in this module.

        #-------------------------------------------------------------    
        # Create our main terminal window for interactive standard I/O
        # to user.  This must be done after the call to initGuiApp().

    if doInfo:
        _logger.info("Creating new GUI-based console window...")

    _console = tikiterm.TikiTerm(title="Dynamic Demo Console",
                                 width=120, height=35)
        # Note the window size of 90x30 chars is a bit bigger than a
        # standard 80x24 console.  This is big enough to show our
        # splash logo and some text below it.

    if doInfo:
        _logger.info("Redirecting stdout & stderr streams to "
                     "GUI-based console...")

        #|--------------------------------------------------------------------------
        #|  Display a message in the default console window to explain to the
        #|  user the status of this now mostly-superfluous window.  Note this
        #|  is the last thing that is done before stdout is redirected.

    if doNorm:        
        print("\n"
              "You may now minimize this console window; "
              "it's no longer needed.\n"
              "NOTE: Closing this window will kill the %s application.\n"
              % appName)

        #-------------------------------------------------------------
        # Before we actually reassign stdin/stdout/stderr streams to 
        # use our new console, we first make sure we have a record of
        # our original stdin/stdout/stderr streams (if any), so we can
        # restore them later if/when the console window closes.

    # If the default stdout is not already set (e.g. we're running under IDLE),
    if sys.__stdout__ == None:   
        sys.__stdout__ = sys.stdout     # Set it to our actual current stdout.
        
    if sys.__stderr__ == None:          # Likewise with stderr.
        sys.__stderr__ = sys.stderr
        
    if sys.__stdin__  == None:          # And also stdin.
        sys.__stdin__  = sys.stdin


        #-------------------------------------------------------------
        # Have our new console take over the stdin, stdout and stderr
        # stream functions.       

    _console.grab_stdio()
    updateStderr()  # Tells logmaster we have a new stderr now.
        # ^- Without this, we could not see abnormal log messages on
        #    our new console.

        #----------------------------------------------
        # Display splash logo image in console window.
        
    _guibot(lambda:_setLogoImage(_console))
    print() # This just ends the line that the image is on.

        # OK, GUI-related initial setup is done.  

def waitGuiEnd():      # Wait for the user to exit the GUI.
    _guibot.join()



#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   End cosmogui.py
#==============================================================================
