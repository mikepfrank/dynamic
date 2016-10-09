#===========================================================================
#   guiapp.py                                   [python module source code]
#
#       Module for driving multithreaded GUI applications.
#
#       The point of this module is to make it easier for multithreaded
#       applications to drive a GUI, when using a GUI toolkit (currently
#       TkInter) that requires all (or certain) GUI operations to be done
#       from within the main thread.  (Apparently, in TkInter, only the
#       main thread is able to use Tk() to initialize the embedded Tcl/Tk
#       interpreter and open the main window, and perhaps most other GUI
#       operations as well.)
#
#       We'd prefer to have an interface that lets us do whatever we want
#       with the GUI without first having to worry about what thread we
#       are in.  This module provides (the beginnings of) such an interface.
#
#       As long as this interface, rather than the main TkInter interface,
#       is used consistently to open all top-level windows (and do all
#       other TkInter operations that need to be done from within the main
#       thread), everything should be copacetic.
#
#       Usage:
#           mainWin = TopWin(title="First Window")
#               # - Creates the main toplevel window.  Also starts Tcl/Tk.
#           guigo()     # Start the GUI main loop in the guibot thread.
#           ...
#           newWin = TopWin(title="Second Window")      # Open another toplevel window.
#           ...
#
#============================================================================


    #============================================================================
    #
    #   1.  Module and name imports.
    #
    #============================================================================

import sys, traceback
import _thread
from tkinter import *       # TkInter, for Tcl/Tk Interpreter, is the GUI toolkit that comes with python.
from threading import *     # High-level interface for working with threads.

# Custom
from .flag import *          # Waitable boolean condition variables, useful as signals between threads.
from .worklist import *      # Worklists are queues providing an inter-thread RPC (remote procedure call) capability.
from logmaster import *

logger = getLogger(appName + ".gui")    # Consider the gui part of the app, for logging purposes.

    #===========================================================================
    #
    #   2.  Initialization of global variables.
    #
    #           Special:    __all__
    #
    #           Public:     guibot:Worker   - For running GUI functions.
    #
    #           Private:    lock, mainWinExists, mainloopRunning, theMainWin
    #
    #===========================================================================

# Here are the names we export to a module that does "from guiapp import *".

__all__ = ['guibot', 'theMainWin',                              # Public globals.
           'OnlyOneMainWin', 'NoMainWindow', 'WrongThread',     # Exception classes.
           'MainWin', 'TopWin', 'guigo', 'ismain', 'ambot',     # Module functions.
           'shutdown', 'initGuiApp',
           ]

# Declare the following identifiers as always global within this module.
global lock, mainWinExists, mainLoopRunning, theMainWin, guibot

        #--------------------------------------------------------------------
        #   lock                                    [module private global]
        #
        #       This re-entrant lock allows us to enforce atomicity
        #       of updates to our module globals within a multi-
        #       threaded environment.  A "with lock:" should be used
        #       around code that modifies module state. 

lock = RLock()      # Create mutex lock on guiapp module state.

with lock:  # Go ahead and acquire the lock while initializing the remaining globals.

        #----------------------------------------------------------------
        #   mainWinExists                       [module private global]
        #
        #       This waitable Boolean condition variable indicates
        #       whether the application's main window currently
        #       exists or not.  Initially False.

    mainWinExists = Flag()      # Create flag for announcing main window.


        #----------------------------------------------------------------
        #   mainloopRunning                     [module private global]
        #
        #       This flag (waitable Boolean condition variable)
        #       indicates whether the TkInter main event loop is
        #       currently running or not.  Initially False.

    mainloopRunning = Flag()    # Create flag for announcing main loop state.


        #----------------------------------------------------------------
        #   theMainWin                          [module public global]
        #
        #       The application's main toplevel window, if it has
        #       been created yet, otherwise None.
    
    theMainWin = None           # The main window does not yet exist.


        #----------------------------------------------------------------
        #   guibot                              [module public global]
        #
        #       This Worker thread is responsible for carrying out
        #       all changes to the TkInter GUI that must be done by
        #       the thread running the TkInter main loop.  (This
        #       includes, apparently, opening all toplevel windows.
        #       To be safe, use it for ALL TkInter operations.)
        #
        #       Before using the guibot, it must be created by
        #       calling guiapp.initGuiApp().
        #
        #       To have any desired window operation done by the
        #       guibot (e.g., if it's not thread-safe), simply use:
        #
        #           result = guibot(callable)
        #
        #       Where callable may be any callable object (function
        #       or lambda, or anything supporting the __call__
        #       method).

    guibot = None       # Not created yet.  Done in initGuiApp().

# Commented this out b/c too drastic - main could have life after GUI death...
#    guibot = RPCWorker(onexit=_thread.interrupt_main)
#        # - When the guibot exits its main thread run() method,
#        #   for any reason, we have it send Ctrl-C to the main thread.


#===========================================
#
#   3.  Declaration of exception classes.
#
#===========================================


    #--------------------------------------------------------------
    #   OnlyOneMainWin                      [module public class]
    #
    #       This exception is raised by MainWin() if it is
    #       called a second time before the previous main
    #       window has been destroyed.  (Only one main
    #       TkInter window is able to exist at a time
    #       within a given application process, apparently.)

class OnlyOneMainWin(Exception): pass


    #--------------------------------------------------------------
    #   NoMainWindow                        [module public class]
    #
    #       This exception is raised by go() if no main window
    #       has been created yet.

class NoMainWindow(Exception):pass


    #--------------------------------------------------------------
    #   WrongThread                         [module public class]
    #
    #       This exception is raised by methods if they are
    #       called from the wrong thread.  However, most of
    #       our methods automatically route their work to the
    #       correct thread (guibot in most cases), so this
    #       one is rarely used.

class WrongThread(Exception):pass


#===========================================
#
#   4.  Internal class definitions.
#
#===========================================


    #-------------------------------------------------------------------
    #   _MainWin                                [module private class]
    #
    #       This subclass of Tk represents a TkInter main window
    #       within the context of a guiapp-based application.  It
    #       is special in that it arranges for the guibot worker
    #       to be invoked periodically to check for commands that
    #       may be sent to the GUI main loop from other threads.

class _MainWin(Tk):


        #------------------------------------------------------------------
        #   Initializer.                        [instance special method]
        #
        #       Initialize this (supposedly unique existing) instance
        #       of a main TkInter window.  We check to make sure that
        #       a main window does not already exist, and raise an
        #       exception if it does.  We make sure the title always
        #       includes the phrase "Main Window" so that the user can
        #       clearly distinguish it from other application windows.

    def __init__(inst, title=None, width=800, height=600):
        
        global lock, mainWinExists, theMainWin  # Use these module globals.

            # Make sure we're in the guibot thread; if not, raise an exception.
        
        if not ambot():
            raise WrongThread(("[%s] " % current_thread().name) +
                              "In guiapp._MainWin.__init__():\n\tCalling this " +
                              "method directly from threads other than " +
                              ("guibot (%s)\n\tis not supported.  Use " % guibot.name) +
                              "guiapp.MainWin() instead.")

        with lock:      # Lock the guiapp module while we make it.

                # Make sure that another main window does not already exist.
            
            if mainWinExists:
                raise OnlyOneMainWin("Creating more than one main window is not allowed.")

                # Assign our global "guiapp.theMainWin" as an accessible-everywhere
                # reference to this new main-window instance.  (This reference gets
                # unlinked in our __del__ method if the window is ever destroyed.)
                # (Except that doesn't seem to work yet for some reason.)

            theMainWin = inst

                # Create a flag to keep track of whether this main window has been
                # destroyed yet.

            inst.destroyed = Flag()

                # Set the title of the window, based on our new "title" optional
                # argument.  If no title was specified, use a generic one that
                # makes it clear what this window is, in general.
            
            if title==None:
                title = "TkInter GUI Application"

                # Add the phrase "Main Window" to the title, in brackets.  This
                # is done UNCONDITIONALLY for all main windows, to make sure the
                # user can visually identify that this is the main window of the
                # app.  (However, the user can always change the title string to
                # something else later on.)
            
            title += " [Main Window]"

                # Perform regular initialization that applies to all TkInter main
                # window widgets.  (Among other things, this initializes the Tcl
                # interpreter.)
            
            Tk.__init__(inst)

                # Now that the basic widget framework is established, go ahead and
                # actually set the window title to the string we composed earlier.
                # (Note the window is not actually displayed until someone calls
                # our go() method.)
            
            inst.title(title)

                # Set the window width and height.
            
            inst.config(width=width, height=height)

                # Raise the guiapp.mainWinExists flag to announce that the main
                # window exists now - in case some other thread has been hanging
                # around just waiting for that to happen.
            
            mainWinExists.rise()

                # Ask TkInter to have the main window check the guibot worklist
                # for new things to do as soon as the GUI mainloop is running
                # & idle (waiting for events).
                
            inst.after_idle(inst.check_worklist)

    # End _MainWin.__init__()
    #---------------------------------------------


        #-----------------------------------------------------------------
        #   go()                                [instance public method]
        #
        #       Start the TkInter GUI application's main loop, if
        #       it's not already started.  This method can be called
        #       from any thread, but it always delegates its work to
        #       the guibot worker thread, because TkInter doesn't 
        #       support being called from within multiple threads.

    def go(inst):
        global lock, guibot, mainloopRunning
        if ambot():        # If we're already in the guibot thread,

            # Raise the flag to announce the mainloop is running.
            
            if not mainloopRunning.rise():  # If it wasn't running already,

                logger.debug("_MainWin.go(): About to enter TkInter main loop...")

                    # Go ahead and start the mainloop, but catch any exceptions.
                
                try:                        
                    inst.mainloop()             # Start the TkInter main loop.

                    # Here's an Exception we may throw sometimes in our callbacks
                    # when our thread is being asked to exit.  However, I'm not sure
                    # if this exception will actually make it through TkInter.

                except ExitingByRequest:
                    logger.debug("_MainWin.go(): Exited from TkInter mainloop by request.")
                    raise   # Pass the exception on to our caller (probably Worker.run()).

                except:     # If TkInter gives us an exception,
                    logger.exception("_MainWin.go(): TkInter mainloop exited with an exception.")
                    raise   # Pass the exception on to our caller (probably Worker.run()).

                finally:                    # If we ever exit the main loop,
                    logger.debug("_MainWin.go(): in finally clause after TkInter main loop")
                    mainloopRunning.fall()      # Turn off mainloopRunning flag.

                    logger.debug("_MainWin.go(): About to destroy main window")
                    inst.destroy()          # Delete the _MainWin object (& all its descendant widgets).
                    logger.debug("_MainWin.go(): Destroyed main window")
                    logger.debug("_MainWin.go(): guibot's task of running the TkInter mainloop is now complete.")

            else:
                logger.debug("_MainWin.go(): TkInter mainloop is already running; request ignored.")

            # If the main loop was already running, we get here and just
            # do nothing & return.  Consider the "go" a success by default.
            # Or we might get here because of an exception.  Either way,
            # the "go" task is now completed.

            logger.debug("_MainWin.go(): Returning from _MainWin.go().")
            
        else:                   # We're in the wrong thread...
            guibot.do(inst.go)      # Re-call this method, in the background,
                # in the guibot thread.  (Don't wait for it to finish!)

    # End _MainWin.go().
    #---------------------------

        #------------------------------------------------------------------
        #   check_worklist()                    [instance private method]
        #
        #       This method should only be called from within the
        #       guibot thread.  When guibot is in the TkInter mainloop,
        #       it arranges for TkInter to call this callback
        #       periodically, to ensure that guibot can still check for
        #       more tasks to do while within the context of the fact
        #       that it is already in the middle of doing the "go"
        #       (run mainloop) task).  Needless to say, all tasks done
        #       by the guibot within here need to finish quickly, so
        #       that the GUI don't become unresponsive.
        

    def check_worklist(self):
        global guibot

        if not ambot():
            raise WrongThread(("[%s] " % current_thread().name) +
                              " guiapp._MainWin.check_worklist():\n\tCalling this " +
                              "method directly from threads other than " +
                              ("guibot (%s)\n\tis not supported.  Use " % guibot.name) +
                              "guigo() instead to start guibot's TkInter mainloop processing.")
        
            # If we get here, we're in the guibot thread.
            # Try doing any tasks that might be waiting in our worklist queue.
            # (But catch exceptions while doing so.)

        try:

                # The point of this loop is that if multiple tasks for us 
                # got queued up since the last time we woke up, we go ahead
                # and do them all now (clear the queue) rather than going
                # to sleep for another tenth of a second after each item.
                # This loop is only exited when do1job() throws an Empty
                # exception (which it can do in nonblocking mode).
            
            while True:
                    # If someone asked us to exit, comply by throwing ExitingByRequest.
                guibot.check_exitflag()

                    # Retrieve and do 1 item from our queue, if available.
                try:
                    guibot.do1job(block=False)  # block=False says: if worklist is empty, don't wait for tasks.
                except WarningException:
                    logger.warn("_MainWin.check_worklist(): guibot job exited by throwing a WARNING-level exception; ignoring...")
                        #\The idea here being that mere warning-level exceptions shouldn't prevent processing of subsequent jobs.

                    # Commented out b/c this happens too often to be worth including in debug output.
#               logger.debug('After do1job, queue size = %d' % guibot.todo.qsize())

                    # Make sure our main window hasn't disappeared; if so, quit.

                if self.destroyed:  # Did that task result in the window getting torn down?

                        # There's no need to run the TkInter mainloop any more if the
                        # main window (and therefore all other windows?) no longer exist.

                    logger.debug("_MainWin.check_worklist(): Widget destroyed out from under us; quitting main loop.")
                    self.quit()     # Tells TkInter to quit its main loop.
                    return          # Return from this routine without scheduling an "after" callback.

                    # In between guibot tasks, let TkInter check for common events
                    # like resize, etc., for better overall responsiveness of the GUI.
                    
                self.update_idletasks()

            # If worklist is empty now, there's nothing else to do; just return.

        except Empty:                   # Is the worklist queue empty?
            pass                            # That's our normal way out of the loop.

            # If someone asked the guibot to exit, then exit TkInter's mainloop also.

        except ExitingByRequest:        # Are we exiting check_worklist() b/c someone asked guibot to exit?
            self.quit()                     # Then, tell TkInter to quit its main loop as well.
            # Don't re-raise because TkInter may print an unwanted traceback for this exception.
            return                          # This avoids rescheduling callback to this method.

        except:                         # Did some other exception happen?
            logger.exception("_MainWin.check_worklist(): A guibot job threw an exception...")
                #-We don't re-raise the exception here, because we want the
                # last line of this function (rescheduling this callback) to
                # still be executed.  If we didn't do that, guibot would get
                # stuck in the mainloop and be unable to execute any more tasks.
                # One alternative would be to quit the whole mainloop here,
                # but that might be a little too drastic.  (Really, we should
                # look for fatal vs. non-fatal classes of exceptions, and
                # respond accordingly.)

                # This is commented out because it seemed too drastic.
#            print("_MainWin.check_worklist(): A guibot job threw an exception...",file=sys.stderr)
#            traceback.print_exc(file=sys.stderr)
#            self.destroy()  # Destroy _MainWin widget and all subwidgets.  Bad idea to do it this early?
#            raise       # Re-raise that exception. Or does TkInter just swallow it up?

        # If we exited the above queue-consumption loop normally, or because of an
        # un-handled exception, then ask TkInter to call this routine again in not
        # less than 100 milliseconds.  This effectively gives us our own main loop,
        # inside of TkInter's mainloop.  The delay prevents excessive polling while
        # remaining reasonably responsive.  
        
        self.after(100, self.check_worklist)    # 100 ms = 1/10th sec.  Decently responsive.

    # End _MainWin.check_worklist().
    #----------------------------------------

        #---------------------------------------------------------------------
        #   destroy()                               [instance public method]
        #
        #       This overrides the default destroy method from our
        #       superclass Tk.  (However, we call it internally.)
        #
        #       Basically, we just set some flags to track our state.
        #

    def destroy(this):
        logger.debug("%s in _MainWin.destroy()..." % current_thread())  #real stdout

            # We also need to kill the guiapp thread (or at least
            # clear out its event queue, since those events probably
            # all refer to widgets that are being destroyed) but I'm
            # not quite sure how/when to best do this.
            
        with lock:
            if this.destroyed:
                logger.warn("_MainWin.destroy(): Main window has already been destroyed; ignoring request.")
                return
            theMainWin = None           # Unlink the global reference to this instance.
            mainloopRunning.fall()      # If it was still running, it's dead by now.
            mainWinExists.fall()        # Announce that we no longer exist.
            
        Tk.destroy(this)

        this.destroyed.rise()

    # End _MainWin.destroy().
    #-------------------------

        #----------------------------------------------------------------------
        #   __del__()                               [instance special method]
        #
        #       Destructor.  I thought this was supposed to get called
        #       when the main window was closed, but this doesn't seem
        #       to be happening.  Look into this sometime.  I think it's
        #       because of reference counts keeping it alive and all that.

    def __del__(inst, *args):
        global lock
        logger.debug("%s in _MainWin.__del__()..." % current_thread())
        Tk.__del__(*args)           # Do the usual Tk delete stuff.

# End class _MainWin.
#---------------------


#===========================================
#
#   5.  Public function definitions.
#
#===========================================


    #---------------------------------------------------------------------
    #   MainWin()                               [module public function]
    #
    #       Creates and returns the application's main window object.
    #       The actual work is done within the guibot worker thread.
    
def MainWin(title=None, width=800, height=600):
    global guibot
    if ambot():    # If we ARE the guibot thread,
        win = _MainWin(title, width=width, height=height)
        logger.debug("MainWin(): The new main window is %r", win)
        return win                   # Just go ahead and open the main window.
    else:
        return guibot(lambda:_MainWin(title, width=width, height=height))     # Have the guibot worker thread open the main window.


    #---------------------------------------------------------------------
    #   TopWin()                                          [module function]
    #
    #       Creates and returns a new top-level window object.
    #       If there is no main window yet, the top-level window that
    #       gets created will be the main window.  (A main window is
    #       a window such that, when it is closed, all the windows in
    #       the application will automatically be closed.)

def TopWin(title=None, width=800, height=600):
    global lock, guibot
    logger.debug("%s entering TopWin()..." % current_thread())
    if ambot():    # If we ARE the guibot thread,
        with lock:
            if mainWinExists:
                win = Toplevel(width=width, height=height)
                win.title(title)
                return win   # Return a new TkInter Toplevel window object.
            else:
                win = MainWin(title=title, width=width, height=height)
                logger.debug("%s: TopWin(): MainWin() returned %r" % (current_thread(), win))
                return win    # Create and return a new main window instead.
    else:
        win = guibot(lambda:TopWin(title, width=width, height=height))
        return win       # Have the guibot worker thread re-call this function.

    #----------------------------------------------------------------------
    #   guigo()                                            [module function]
    #
    #       Tells the guibot worker thread to start running the
    #       TkInter main loop.  Although this task will itself
    #       not finish until the application exits, in the course
    #       of running this task, the guibot will continue to
    #       receive and process other work items arriving on its
    #       worklist.

def guigo():
    logger.debug("%s entered guiapp.guigo()..." % current_thread())
    if mainWinExists:
        guibot.do(theMainWin.go)    # Run main loop in "background"
            # (guibot will become tied up with it, but it will still
            # process requests via the check_worklist() callback).
    else:
        raise NoMainWindow("Can't start GUI because no main window has been created yet.")
    logger.debug("%s exiting guiapp.guigo()..." % current_thread())

    #----------------------------------------------------------------------
    #   ismain()                                        [module function]
    #
    #       Returns True if the given object is the main toplevel
    #       window of the entire guiapp application, False otherwise.

def ismain(x:object):
    return isinstance(x, _MainWin)

    #-----------------------------------------------------------------------
    #   ambot()                                         [module function]
    #
    #       Returns True if the current thread is the guibot worker
    #       thread; False otherwise.

def ambot():
    return current_thread() == guibot

    #--------------------------------------------------------------
    #   shutdown()                              [module function]
    #
    #       Destroys the main window (if any) and stops the
    #       guibot from accepting any more tasks.  Only call
    #       this from within guibot.  (Warning: The guibot
    #       may still try to continue executing tasks already
    #       in its queue.  If these )

def shutdown():     # run within guibot only
    if not ambot():
        logger.error("guiapp.shutdown(): Not in guibot thread. Aborting.")
        raise WrongThread("Not in guibot thread.  Aborting shutdown().")
        
    logger.debug("In guiapp.shutdown().")
    if theMainWin:
        logger.debug("guiapp.shutdown(): Destroying main window...")
        theMainWin.destroy()     # If the main window exists, destroy it.

        # Originally we just had guibot.stop() below, but that seemed to create
        # a danger that there might still be GUI tasks lying around in the queue
        # that will never get executed - these could include some harmless log
        # message flush requests which are harmless enough because we could always
        # just redirect them to stdio.  However, there may also be arbitrary
        # TkInter calls in guibot's queue which might crash with ugly errors
        # because the main window has been destroyed.  However, if guibot's still
        # running in the check_worklist recurrent callback, that one will check if
        # the window's been destroyed and exit the TkInter mainloop() if it is.
        # Then, once the mainloop exits, the guibot's Worker.run() method will be
        # back in control.  OK, so we still need a way to avoid doing actual GUI
        # requests which might cause crashing problems.  Maybe a special attribute
        # added to GUI work items (initialized using an optional argument to do()
        # and getResult() with signature "needsTk:bool=True") which says whether
        # we should check that the main window still exists first.  But, more
        # generally, the tasks given to guibot might need specific sub-widgets
        # that might not still exist even if the main window does still exist.
        # To deal with this, really all commands given to guibot ought to make
        # sure that the necessary widgets still exist before they do anything.
        # I know, this makes programming more complicated, but I'm not sure how
        # else to deal with things without risking missing some console log messages,
        # which could be worse, if the lost messages were critical errors the user
        # really needs to know about.  Anyway, by changing this from .stop() to
        # .close() below, at least we offer the HOPE that guibot might still be
        # able to finish up its last items.  If not, that can be debugged later.

    logger.debug("guiapp.shutdown(): Closing guibot to new tasks...")
    guibot.close()  # Tell guibot not to accept any new items on its worklist
        # and just to finish up doing the items that are already on there,
        # and exit when those are done.
        
#    guibot.stop()   # Makes guibot stop as soon as he's done with this current task.


    #===============================================================
    #   initGuiApp()                            [module function]
    #
    #       Initialize this GUI-based application.
    #
    #       Initializes the guiapp module.  Currently, all this
    #       does is create and start the guibot worker thread.
    #       The guibot iteself will do all other initialization
    #       as necessary, as it receives work orders.
    #
    #       NOTE: This does not work on MacOS X, because TkAqua
    #       insists on running in the main thread.  To fix this
    #       we need to rearchitect things to have the main thread
    #       become a guibot, while some other thread can be created
    #       to do whatever the main thread does currently.

def initGuiApp():   # Initialization for this module.

        # The trickiest, most annoying thing about Python is the 
        # need to remember to put in these explicit "global"
        # declarations everywhere that a given global is assigned!

    global guibot

# The following code isn't working yet, so just do things the old way for now.
#
##
##        # Here we are trying a new approach to try to get this
##        # module to work in Mac OS X.  We enlist the current
##        # thread (which we assume is the main thread) as a worker
##        # thread, then set it be an RPCWorker type thread, i.e.,
##        # to wait for return values from tasks by default.  Thus,
##        # the current thread is transformed into the guibot.
##
##    mainThread = current_thread()              # Assume current thread is main thread.
##    HireThread(mainThread)                     # Recruit it as a new Worker.
##    mainThread.waitByDefault = True            # Have it wait for return values by default, like an RPCWorker would.
##    setThreadRole("guibot")                    # Rename its role to "guibot"
##    guibot = mainThread                        # Set guibot to be it.
##
##        # The following fails on MacOS X because TkAqua insists
##        # on running in the main thread.  Comment this out for
##        # now in lieu of the above.
    
        # Create and start the GUI thread.

    logger.debug("guiapp.initGuiApp(): Creating guibot worker thread...")
    guibot = RPCWorker(role="guibot", component="GUI")
    
        # - Note: Because we made guibot be an RPCWorker, this
        #   means that when users call it directly (like this:)
        #
        #       guibot(callable),
        #
        #   it waits for a result from the worker thread and
        #   returns it to the caller.  In places where this
        #   feature is not needed (or would cause problems),
        #   instead use:
        #
        #       guibot.do(callable)
        #
        #   for reduced latency (it does not wait for completion).
        #   If you need to wait for completion later, you can go
        #   ahead and bundle the callable into a WorkItem, and
        #   then wait for the workitem's completion:
        #
        #       task = WorkItem(callable)   # Create the new task object.
        #       guibot.do(task)             # Tell the guibot to start doing the task.
        #       ...                         # We do some other stuff in the meantime.
        #       task.wait()                 # Wait for work on the task to halt.
        #       if task.done:               # If it completed successfully,
        #           ...                     #   do something else...

    logger.debug("guiapp.initGuiApp(): guibot is: %s" % guibot)

# End initGuiApp().
#---------------------

if __name__ == "__main__":
    foo = _MainWin()        # Test: Should throw WrongThread exception.
    
