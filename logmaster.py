#|==============================================================================
#|   logmaster.py                                        [python source]
#|
#|       Module providing a customized logger based on python's
#|       general logging facility.  The intent of putting this
#|       code into its own module is to enable its definitions
#|       to be accessed from within any number of other modules
#|       in the application, so they all can do logging in a
#|       consistent way.  This is particularly important when
#|       debugging.
#|
#|       The specific logging functionality we provide is:
#|
#|           1.  A new logging level called "NORMAL" is added
#|               (in between INFO and WARNING).  Its purpose
#|               is to enable messages that are ordinarily
#|               printed on stdout to be simultaneously logged
#|               to the log file as NORMAL-level messages.
#|
#|           2.  Another new logging level called "UWSERR" is
#|               added (between ERROR and CRITICAL) to convey
#|               low-level UWScript scripting-language errors
#|               transmitted to use from individual sensor nodes.
#|
#|           3.  Ultra-convenient logging functions are exported
#|               (debug(), info(), etc.) that do not require
#|               specifying the logger.
#|
#|           4.  The logger can be configured (via global bools)
#|               to display or not display various "optional"
#|               levels of log messages (warning, info, debug)
#|               to the console (stderr), and, separately, to
#|               save them or not save them in the log file.
#|
#|           5.  The logging formats for the file loghandlers
#|               include the time, down to the millisecond.
#|
#|           6.  All formats include the log level (except for
#|               NORMAL messages to stdout).
#|
#|           7.  All log messages (again except normal messages
#|               to the console) are always prefixed with the
#|               thread name, to facilitate debugging of
#|               multithreaded programs.
#|
#|       Work in progress:
#|
#|           [ ] Create a structure (class object?) that lets us
#|               avoid making each using module refresh its copies
#|               of our globals whenever they change.
#|
#|           [/] Give each thread a logging context.
#|
#|           [/] Have each module use a LoggerAdapter, which uses
#|               the logging context.
#|
#|           [/] Let each module use its own logger, a descendant
#|               of the root logger "" in the logging hierarchy.
#|
#|           [/] Create a child logger for each node.
#|           
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    #==================================================================
    #   Module imports.                             [code section]
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        # Imports of standard python modules.

import os           # Used in calculating _srcfile
import sys          # For stdout/stderr, for console loghandler & internal debugging of logmaster.
import io           # For TextIOBase, which we subclass in NullOut.
import logging      # General python logging facility.
    # - Don't import names from within it, b/c we redefine some of them.
import threading    # Used for our threading.local LoggingContext
import traceback    # Used for ...

        # Imports of lower-level custom modules.

global systemName, appName
    # The initial values of these defined later in this file are
    # placeholders that should never be used.
    
import appdefs
from appdefs import *   # Sets systemName, appName for this application.
sysName = systemName    # Shorter synonym for systemName

    #==================================================================
    #   Global variables & constants.               [code section]
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #==============================================================
        #   Special globals.                        [code subsection]
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            #==========================================================
            #   __all__                             [special global]
            #
            #       List of explicitly exported public names.
            #
            #       These are the names we provide that will
            #       get imported into another module when it
            #       does:
            #
            #           from logmaster import *
            #
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
            
__all__ = ['NORMAL_LEVEL',                          # Public global variables.
           'LOG_FILENAME', 'LOG_FORMATSTR',
           'CONS_WARN', 'CONS_INFO', 'CONS_DEBUG',
           'LOG_INFO', 'LOG_DEBUG',
           'systemName', 'sysName', 'appName',
           'theLoggingContext', 'mainLogger',       # Public global objects.
           'sysLogger', 'appLogger',
           'logFormatter',
           'LoggedException', 'InfoException',      # Public exception classes.
           'ExitException', 
           'WarningException', 'ErrorException',
           'CriticalException', 'FatalException',
           'LoggingContext', 'ThreadActor',         # Public regular classes.
           'AbnormalFilter', 'NormalLogger',
           'NormalLoggerAdapter',
           'initLogMaster', 'configLogMaster',      # Public functions.
           'normal', 'debug', 'info', 'error',
           'warning', 'warn', 'error', 'exception',
           'critical', 'lvlname_to_loglevel',
           'byname', 'getLogger', 'testLogging',
           'updateStderr', 'setThreadRole', 'setComponent',
           ]


        #=============================================================
        #   Public globals.
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            #=========================================================
            #   Public global constants.
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global NORMAL_LEVEL, NORMAL, LOG_FILENAME, LOG_FORMATSTR
global CONS_WARN, CONS_INFO, CONS_DEBUG, LOG_INFO, LOG_DEBUG

                #============================================================
                #   New logging levels.         [public global constants]
                #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global NORMAL_LEVEL, NORMAL

NORMAL_LEVEL = 25       # For normal output.  Between INFO and WARNING.
NORMAL = NORMAL_LEVEL   # A more concise synonym.
    #- initLogMaster() will actually add this new level.

                #=============================================================================
                #   systemName,appName:str              [public global constants]
                #
                #       Name of the overall system we are a part of, and the
                #       specific application within that system.  They can be
                #       modified if needed for another application by assigning
                #       to logmaster.systemName, etc., any time before
                #       logmaster.configLogMaster() is called, or as optioal
                #       arguments to it.  These are important for setting up the
                #       logger (logging channel) hierarchy.
                #
                #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

if not "systemName" in dir():           # If appdefs did not already define systemName,
    sysName = systemName = "(Unknown System)"         # Define it (placeholder value).
if not "appName" in dir():              # If appdefs did not already define systemName,
    appName = systemName + ".(Unknown App)"    # The name of this application program (child of system).    
else:
    LOG_FILENAME = appName + ".log"     # Default log file name.

                #===========================================================
                #   LOG_FILENAME                [public global constant]
                #
                #       Actually this is not really constant, but can be
                #       modified for other applications if needed before
                #       configLogMaster() is called, or as an optional
                #       argument to configLogMaster().
                #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

if not "LOG_FILENAME" in dir():     # If not already defined above,
    LOG_FILENAME = "script.log"         # Set it to a generic default log file name.

                #============================================================
                #   LOG_FORMATSTR               [public global constant]
                #
                #       Default format for the main log file.  Actually,
                #       this "constant" can be modified if needed before
                #       initLogMaster() is called, or as an optional
                #       argument to initLogMaster().
                #
                #       IMPORTANT NOTE:  The fields named 'threadrole' and
                #       'component' below are only meaningful because these
                #       keys are defined in the dictionary of the thread-local
                #       (but lexically global) LoggingContext object that
                #       gets passed into the constructor for the LoggerAdapter
                #       that is used for doing the actual logging.
                #
                #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global LOG_FORMATSTR
LOG_FORMATSTR = ("%(asctime)s | %(name)-20s | " +                               # Time & logger name.
                 "%(threadName)10s:  %(component)9s  %(threadrole)-16s  | " +   # Thread & its logging context (role & component).
                 "%(module)18s.py:%(lineno)4d:%(funcName)-19s | " +             # Source code file, line #, and function/method name.
                 "%(levelname)8s: %(message)s")                                 # Log level and log message.

                #=============================================================
                #   Logging options.            [public global constants]
                #
                #       Change these Booleans to modify how the logging
                #       levels for the console and the main log file are
                #       set up.  Normally the console will show warnings
                #       and higher, and the log file will show info-level
                #       messages and higher.  For more flexible control,
                #       you can always just set the log level explicitly.
                #
                #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global CONS_WARN, CONS_INFO, CONS_DEBUG, LOG_INFO, LOG_DEBUG

CONS_WARN = True    # Default value: True.
    # - Change this to False before initialization to suppress warnings from console.
CONS_INFO = False   # Default value: False.
    # - Change this to True before initialization if you want verbose information on console.
CONS_DEBUG = False  # Default value: False.
    # - Change this to True before initialization if you want detailed debug info on console.
    #   Overrides CONS_WARN.

LOG_INFO = True     # Default value: True.
    # - Change this to False before initialization to suppress verbose info from log file.
LOG_DEBUG = False   # Default value: False.
    # - Change this to True before initialization to log detailed debugging information in log file.
    #   Overrides CONS_INFO.

                #=============================================================
                #   Log level settings.         [public global constants]
                #
                #       These keep track of what logging level we are
                #       using for both the main log file and the console.
                #       Change these indirectly using configLogMaster().
                #
                #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global log_level, console_level
log_level = logging.INFO            # By default, log file records messages at INFO level and higher.
console_level = logging.WARNING     # By default, console displays messages at WARNING level & higher.

            #=========================================================
            #   Public global objects.
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

                #=======================================================================
                #   logFormatter:LogFormatter               [public global object]
                #
                #       This is the default LogFormatter used by logmaster for
                #       the main application log file.  It is based on the format
                #       string LOG_FORMATSTR above.  It is created in initLogMaster().
                #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global logFormatter
logFormatter = None

                #=============================================================================
                #   theLoggingContext:LoggingContext       [public global thread-local object]
                #
                #       A single (but thread-local) LoggingContext object, to be shared by
                #       all modules (but different for each thread), for passing to their
                #       module-specific loggerAdapter objects that they will use for logging.
                #       This object is created in this module, (in init_logging()), it gets
                #       initialized separately within each thread, and then it is updated
                #       dynamically, if needed, as the thread progresses.
                #
                #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global theLoggingContext       # A single global (but thread-local) LoggingContext object.
theLoggingContext = None       # To be properly initialized later.

                #=============================================================================
                #   mainLogger:Logger                           [module public global object]
                #
                #       This is the main logger for the application.  It is the logger
                #       that should be used in modules that don't bother to define their
                #       own logger (but most modules should define a logger, either based
                #       on the systemName, the appName, or at least the module's own name).
                #
                #       We don't initialize this when the module is first loaded, but
                #       wait until logmaster.initLogMaster() is called, which should be done
                #       only once in the program, before using any logging capabilities.

global mainLogger
mainLogger = None           # Initialized later.

    # Some more loggers.
global sysLogger, appLogger
sysLogger = None
appLogger = None

        #======================
        #   Private Globals.            [code subsection]
        #======================

            #========================================================================
            #   initialized:bool                    [module private global variable]
            #
            #       This bool is set to True once the logmaster module has been
            #       initialized.  It is used to prevent the module from being
            #       initialized more than once.  Use the initLogMaster() function
            #       to initialize the module.  (We didn't use a flag here because
            #       nobody else will get the opportunity to wait for it anyway.)

global initialized
initialized = False     # Initially false; this module has not yet been initialized.
        
       
            #===============================================================
            #   moduleLogger:Logger          [module private global object]
            #
            #       This logger (which is not publicly exported) is
            #       to be used, from within this module only, for log
            #       messages generated by this module.  This is also a
            #       model for what other non-application-specific
            #       modules that use logmaster should do to get their
            #       own module-local loggers.

global moduleLogger
moduleLogger = None     # Initialize in init_logging()


            #=================================================================
            #   _srcfile                    [module private global variable]
            #
            #       Copied from logging/__init__.py.  This code had to be
            #       copied into this module in order for it to get the value
            #       of __file__ that we want to use here.

global _srcfile
#
# _srcfile is used when walking the stack to check when we've got the first
# caller stack frame.
#
if hasattr(sys, 'frozen'): #support for py2exe                  # This part is inappropriate for us,
    _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])  # not sure how to fix yet. -mpf
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)


    #==================================================================
    #   Class definitions.                          [code section]
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #==============================================================
        #   Exception classes.                      [code subsection]
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            #==========================================================
            #   LoggedException             [public exception class]
            #
            #       A LoggedException is an exception such that,
            #       when it is first constructed, a log message
            #       of an appropriate level is automatically
            #       generated and sent to a specified logger.
            #
            #       The constructor for a LoggedException takes
            #       a logger and a message.  The logging level for
            #       the message is determined by the subclass of
            #       LoggedException that is used (see subclasses
            #       below).
            #
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class LoggedException(Exception):

        #=========================================================
        #   .defLogger                          [class variable]
        #
        #       The default logger to use for exceptions of a
        #       given (subclass) type.  NOTE: This value is
        #       just a placeholder for this attribute in this
        #       abstract base class.  All concrete derived
        #       classes (ones for which a constructor will
        #       actually be called) MUST override this class
        #       variable, or it will cause an exception to be
        #       thrown (before the one you want gets thrown)!
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    defLogger = None    # Default logger.  None defined for this base class.

        #---------------------------------------------------------
        #   .loglevel                            [class variable]
        #
        #       The logging level of the exception.  We set
        #       its default value to NOTSET as a placeholder
        #       in this abstract class.  Subclasses should
        #       override this value with the value that is
        #       appropriate for their purposes.  This is done
        #       in the subclasses defined below.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    loglevel = logging.NOTSET

        #----------------------------------------------------------
        #   .__init__()                 [special instance method]
        #
        #       The instance initializer for a LoggedException
        #       creates a default log message for the exception
        #       (if none is provided), and then goes ahead and
        #       logs the occurrence of the exception to the
        #       provided logger.  Note that this initial logging
        #       of the exception will generally occur *before*
        #       the exception is actually raised, in the raising
        #       routine wherever the exception's constructor is
        #       called.  The entity that catches the exception
        #       may of course do additional logging, such as a
        #       logger.exception() call which will also display
        #       a traceback.  We avoid printing tracebacks here,
        #       since that may not be needed for exceptions that
        #       are caught and handled appropriately somewhere
        #       in the calling (i.e., catching) code.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
    def __init__(inst, msg:str=None, level=None, logger:logging.Logger=None):
        if logger==None:
            logger = inst.defLogger  # This should get the value of this
                # class variable for the object's actual class (not from
                # this abstract base class LoggedException).
        if logger==None:
            moduleLogger.error("LoggedException.__init__(): No default logger "
                               "provided for this class of LoggedException.")
            traceback.print_stack()  # goes to sys.stderr
            raise TypeError("LoggedException.__init__(): No default logger "
                               "provided for this class of LoggedException.")
        if level==None:
            level = inst.loglevel   # Get derived class's log level.
        if msg==None:
            msg = ('Creating a LoggedException at level %s.' %
                   logging._levelNames[level])
#        print("About to log message [%s] at level %s." % (msg, str(level)),
#              file=sys.stdout)
        logger.log(level, msg)
 
# End class LoggedException

            #==========================================================
            #   InfoException               [public exception class]
            #
            #       An InfoException, when it is raised at all, is
            #       simply a way to indicate in which of several
            #       normal ways a routine is returning, in cases
            #       where this information is worth reporting in
            #       the log file at INFO level.  An InfoException
            #       should be immediately caught by the caller &
            #       not re-raised.
            #
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class InfoException(LoggedException):
    loglevel = logging.INFO
# End class InfoException

            #==========================================================
            #   ExitException               [public exception class]
            #
            #       An ExitException is like an InfoException in
            #       that it is reported at INFO level; however, it
            #       is intended to cause the entire thread in which
            #       it takes place to terminate.  (Use FatalException
            #       to cause the entire application PROCESS to
            #       terminate.)
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
class ExitException(LoggedException):
    loglevel = logging.INFO
# End class ExitException


            #==========================================================
            #   WarningException            [public exception class]
            #
            #       These exceptions, when they are raised at all,
            #       are simply used as a way to exit early from a
            #       routine with some indication as why we are
            #       exiting early, due to some harmless but unex-
            #       pected circumstance that is worth reporting at
            #       WARNING level, as a sort of alternate return
            #       code; they should be caught (and not re-raised)
            #       at a high level, before they have a chance to
            #       interfere significantly with overall program
            #       flow.  Basically, for any routine that might
            #       throw a WarningException, all callers of that
            #       routine should handle it.
            #
            #       Creating a WarningException automatically generates
            #       log message at WARNING level.
            #
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class WarningException(LoggedException):
     loglevel = logging.WARNING
# End class WarningException.


            #=========================================================
            #   ErrorException              [public exception class]
            #
            #       An ErrorException indicates a fairly serious
            #       problem, one that might prevent us from doing
            #       (or doing properly) a fairly signifcant task.
            #
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class ErrorException(LoggedException):
    loglevel = logging.ERROR
# End class ErrorException.


            #=========================================================
            #   CriticalException           [public exception class]
            #
            #       A CriticalException indicates a very serious
            #       problem, one that might prevent us from doing
            #       a very important task.
            #
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class CriticalException(LoggedException):
    loglevel = logging.CRITICAL
# End class CriticalException


            #==========================================================
            #   FatalException              [public exception class]
            #
            #       Like a CriticalException, but even worse.
            #       When this exception is raised, it generally
            #       causes the application to exit.
            #
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class FatalException(LoggedException):
    loglevel = logging.FATAL    # This is actually the same as CRITICAL.
# End class FatalException
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        #   End of exception classes.
        #==============================================================


        #==============================================================
        #   LoggingContext                      [module public class]
        #
        #       An object of this thread-local class serves as a
        #       dictionary on which each thread can store & track
        #       context information which will be passed to the
        #       LoggerAdapter for any given module, enabling the
        #       log records to be augmented with extra information
        #       printed by the top-level COSMICi format string.
        #
        #       A single global LoggingContext object tracks
        #       context information throughout the application -
        #       although its attributes have different values in
        #       different threads.
        #
        #       Each time a new thread is created, the attributes
        #       of the global loggingContext should be updated
        #       to reflect the context information specific to
        #       that thread.  Some of this is handled automatically
        #       by LoggingContext's __init__ method.
        #
        #       In the scope of the COSMICi application, important
        #       pieces of context information include:
        #
        #           threadname = The name of the current thread,
        #               helpful for debugging threading problems.
        #
        #           threadrole = The role for which the current
        #               thread was created. E.g. "MainSock.listener",
        #               "Node1Main.reader", "Node1Main.consDriver",
        #               "guibot", and so forth.
        #
        #           component = The system component that the thread
        #               is associated with, e.g., "server", "node #0",
        #               "node #1", etc.
        #
        #           nodenum = The numeric ID of the sensor node
        #               (if any) associated with this action.
        #               None if no sensor node is related.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class LoggingContext(threading.local):

            #--------------------------------------------------------------
            #   .__init__()                         [class special method]
            #
            #       The initializer of the global loggingContext will
            #       get called once for each thread, when the global
            #       is first accessed from within that thread.  We
            #       simply initialize its members based on thread
            #       attributes.  Every thread that wants to use the
            #       logmaster module for logging should be a ThreadActor,
            #       or at least have a .role attribute.  The value to
            #       which the "component" dictionary key is assigned
            #       should be changed to "node0", "node1", etc., for
            #       errors being reported on behalf of specific nodes.
            #
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    defComp = "(unsetComp)"    # By default, we don't know which system component this thread is being created to manage.
    defRole = "(unsetRole)"    # By default, we don't know what role this thread is supposed to be playing.
    
    def __init__(inst, myrole=None, who=None, **kwargs):

            # First, do the default initialization for thread.local
            # objects, so that subsequent operations on this object
            # in this initializer will treat it as thread-local.

        threading.local.__init__(inst, **kwargs)
            #\_ Do the default thread.local initialization.

            # Initialize local copies of the role and component from args or defaults.

        if (who == None):       who = inst.defComp
        if (myrole == None):    myrole = inst.defRole

            # Figure out which thread we're in.
        thread = threading.current_thread()

#        print("Initializing logging context in thread %s." % thread,
#              file=sys.stderr)

            # Set up the loggingContext's dictionary of context items.
            
        inst.dict = {}  # Start with empty dictionary.

            # If thread has no role/component attributes defined, set them based on our local values.

        if not hasattr(thread, 'role'):         thread.role = myrole
        if not hasattr(thread, 'component'):    thread.component = who

            # These next two lines use the property setters defined after
            # the current method.
            
        inst.threadrole = thread.role      # Set the role of this thread.
        inst.component = thread.component  # What system component does it involve?

#        print("The dictionary is: [%s]." % inst.dict, file=sys.stderr)

    # End method __init__()

            #-------------------------------------------------------------
            #   .threadrole                    [instance public property]
            #
            #       This property is used to keep track of the current
            #       thread's current role string within the dictionary
            #       structure required for logging context objects.
            #
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    @property
    def threadrole(inst): return inst.dict['threadrole']

    @threadrole.setter
    def threadrole(inst, role:str):
        inst.dict['threadrole'] = role

            #-------------------------------------------------------------
            #   .component                    [instance public property]
            #
            #       This property is used to keep track of the current
            #       thread's component string within a dictionary
            #       structure, as logging context objects must have.
            #
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    @property
    def component(inst): return inst.dict['component']

    @component.setter
    def component(inst, who:str):
        inst.dict['component'] = who

            # Pass these methods to support "dictionary-like" behavior directly
            # to the underlying dictionary.

    def iter(inst):         # If someone asks for an interator on us,
        inst.dict.iter()        # give them an iterator on our dictionary.

#    def keys(): 

    def __getitem__(inst, name):                # __getitem__ on us goes to
        return inst.dict.__getitem__(name)      #   our dictionary instead.

    def __iter__(inst):                         # __iter__ on us goes to
        return inst.dict.__iter__()             #   our dictionary instead.

#^^^^^^^^^^^^^^^^^^^^^^^^^^^
# End class LoggingContext
#===========================

        #==============================================================
        #   ThreadActor                         [module public class]
        #
        #       This subclass of Thread (which can be used as a
        #       mixin class) simply adds an extra initialization
        #       keyword argument role=<str>, which simply sets
        #       the .role attribute of the thread, as separate
        #       from the .name argument (this lets us keep the
        #       .name argument as an automatic sequence counter,
        #       Thread-1, Thread-2, etc.).
        #
        #       The 'role' attribute is used by loggingContext
        #       when it gets initialized later on, when the thread
        #       uses it.  The purpose of that is so that the thread
        #       role is available as a field that can be displayed
        #       as specified in the logging format string.
        #
        #       Oh, and in addition to 'role', there's another one
        #       called 'component'.  The idea of which is to identify
        #       which system component a given thread is currently
        #       working on behalf of.
        #
        #       This class is not itself dependent on the rest of
        #       the logmaster module, and so it should probably be
        #       moved out to its own module.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        
class ThreadActor(threading.Thread):

        # Default role and component for ThreadActor objects when not
        # otherwise specified.  Subclasses should override
        # this class variable.

    defaultRole      = 'actor'       # The role of a ThreadActor is that it is an actor that has a role.
    defaultComponent = 'logdapp'     # By default, new ThreadActors will be operating on behalf of a "logged application".
    defaultTarget    = None          # By default, just use the class's run() method, no other target.
    
        #-----------------------------------------
        # Override the default Thread initializer.
        
    def __init__(inst, *args, role:str=None, component:str=None, target=None, **kwargs):

            # If the parent thread has role and component attributes,
            # use them (instead of class defaults) as the default values
            # for this new thread.  Unless, that is, the subclass overrides
            # the parent class's role/component.

        parent = threading.current_thread()
        if hasattr(parent, 'role') and (inst.defaultRole == 'actor'):                 inst.defaultRole = parent.role
        if hasattr(parent, 'component') and (inst.defaultComponent == 'logdapp'):     inst.defaultComponent = parent.component

            # This allows subclasses to define their thread's role
            # by simply overriding the .defaultRole class variable.
            # Same for component.  And target.

        if       role==None:          role = inst.defaultRole
        if  component==None:     component = inst.defaultComponent
        if     target==None:        target = inst.defaultTarget
            
        inst.role       = role          # Initialize our .role instance attribute.
        inst.component  = component     # Initialize our .component instance attribute.

        moduleLogger.debug("ThreadActor.__init__(): Initialized ThreadActor with role [%s] for component [%s]..."
                     % (inst.role, inst.component))
            # - NOTE: We can't actually update the thread-local logging context at
            #   this point, because we're not actually running within the newly-created
            #   thread yet!
        
            # Do default Thread initialization.
        threading.Thread.__init__(inst, *args, target=target, **kwargs)

    # end def

        # Override the default run() method to initialize the thread's logging context before doing anything else.
        
    def run(self, *args, **kwargs):                         # Run this only from within the newly-created thread itself.
        self.starting();                                    # ThreadActor-specific initialization to be done at start of run().
        return threading.Thread.run(self,*args, **kwargs)   # Dispatch to the default run() method for superclass threading.Thread().

        # Update the thread-local logging context to reflect changes in thread attributes.

    def starting(self):
        if self != threading.current_thread():
            moduleLogger.warn("ThreadActor.starting(): Can't execute starting() method of thread %s "
                              "from within a different thread %s!  Ignoring request." % (self, threading.current_thread()))
            return
        self.update_context()                                # Update the logging context for this new thread

    def update_context(self):           # Run this only from within the newly-created thread itself.
        if self != threading.current_thread():
            moduleLogger.warn("ThreadActor.update_context(): Can't update logging context for thread %s "
                              "from within a different thread %s!  Ignoring request." % (self, threading.current_thread()))
            return

        moduleLogger.debug("ThreadActor.update_context(): Updating logging context to role [%s] & component [%s]..."
                           % (self.role, self.component))
        
        theLoggingContext.threadrole = self.role             
        theLoggingContext.component = self.component   
            # - NOTE: loggingContext is a thread.local global, so it differs for each thread.
            #   Why not just leave this information in thread attributes?  Because LoggerAdapter
            #   wants an object that supports a dict-like interface.  I suppose we could have
            #   stored such an object as a single thread attribute, instead of a thread-local
            #   global.  'Cuz you can always get hold of it through threading.current_thread().
            #   Oh well. Que sera sera.

    def set_role(self, role):
        if self != threading.current_thread():
            moduleLogger.warn("ThreadActor.set_role(): Can't update logging context for thread %s "
                              "from within a different thread %s!  Ignoring request." % (self, threading.current_thread()))
            return
        moduleLogger.debug("ThreadActor.set_role(): Setting role to [%s] for this thread & its logging context." % role)
        self.role                 = role        # Provides for easy access.
        theLoggingContext.threadrole = self.role   # Also store it in the thread-local global LoggingContext.

    def set_component(self, comp):
        if self != threading.current_thread():
            moduleLogger.warn("ThreadActor.set_component(): Can't update logging context for thread %s "
                              "from within a different thread %s!  Ignoring request." % (self, threading.current_thread()))
            return
        moduleLogger.debug("ThreadActor.set_component(): Setting component to [%s] for this thread & its logging context." % component)
        self.component           = comp             # Provides for easy access.
        theLoggingContext.component = self.component   # Also store it in the thread-local global LoggingContext.

        #----------------------------------------------------------------
        # Overrides the default __str__ string converter to display both
        # the thread name and the thread role.
        
    def __str__(inst):
        if hasattr(inst, 'role'):   # So this method will work for non-ThreadActor classes also.
            return "%s (%s)" % (inst.name, inst.role)
        else:
            return inst.name

# Modify the real Thread class's .__str__() method to take advantage
# of the role attribute even for non-ThreadActor classes, as long
# as the attribute exists.

threading.Thread.__str__ = ThreadActor.__str__

# Functions for setting the global, thread-local "threadrole" and "component" attributes.

def setThreadRole(role:str):
    thread = threading.current_thread()
    thread.role = role
    theLoggingContext.threadrole = role

def setComponent(component:str):
    thread = threading.current_thread()
    thread.component = component
    theLoggingContext.component = component

        #==============================================================
        #   AbnormalFilter                      [module public class]
        #
        #       Subclass of Filter that only allows through log
        #       messages that are not at NORMAL level.
        #
        #       This is used by our ConsoleHandler because NORMAL-
        #       level messages appear anyway in the normal output
        #       stream (on stdout) so it would be redundant to
        #       display them again to stdout in the form of log
        #       messages.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class AbnormalFilter(logging.Filter):
    # Override the filter() method.
    def filter(inst, record:logging.LogRecord):   # Decide whether log record gets through this filter.
        return record.levelno != NORMAL_LEVEL      # Evaluates as nonzero iff level is not NORMAL.


        #==============================================================
        #   NormalLogger                        [module public class]
        #
        #       NormalLogger extends Logger with a new logging
        #       method normal(), which prints the given message to
        #       sys.stdout as well as logging it.
        #
        #       Note that since loggers are instantiated by getLogger,
        #       rather than by specifying the class explicitly, this
        #       new method has to be manually copied into the newly
        #       created logger if we want to be able to use it.
        #
        #       We also replace the Logger._log() method with a
        #       version that allows the caller to pass the
        #       findCaller() result in directly.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class NormalLogger(logging.Logger):

    # Extend Logger with new normal() method for printing normal-level messages.
    
    def normal(inst, message:str, *args, caller=None, **kwargs):
        print(message)              # Print the message to stdout.
        if inst.isEnabledFor(NORMAL):
            if caller==None:                                
                caller = mainLogger.logger.findCaller()
            inst.log(NORMAL, message, *args, caller=caller, **kwargs)  # Also log it via the active LogHandlers.

    # Override Logger's standard logging methods to also find caller information.
    
    def debug(self, msg, *args, caller=None, **kwargs):
        if self.isEnabledFor(DEBUG):
            if caller==None:                                
                caller = mainLogger.logger.findCaller()
            self._log(DEBUG, msg, args, caller=caller, **kwargs)

    def info(self, msg, *args, caller=None, **kwargs):
        if self.isEnabledFor(INFO):
            if caller==None:                                
                caller = mainLogger.logger.findCaller()
            self._log(INFO, msg, args, caller=caller, **kwargs)

    def warning(self, msg, *args, caller=None, **kwargs):
        if self.isEnabledFor(WARNING):
            if caller==None:                                
                caller = mainLogger.logger.findCaller()
            self._log(WARNING, msg, args, caller=caller, **kwargs)

    def error(self, msg, *args, caller=None, **kwargs):
        if self.isEnabledFor(ERROR):
            if caller==None:                                
                caller = mainLogger.logger.findCaller()
            self._log(ERROR, msg, args, caller=caller, **kwargs)

    def critical(self, msg, *args, caller=None, **kwargs):
        if self.isEnabledFor(CRITICAL):
            if caller==None:                                
                caller = mainLogger.logger.findCaller()
            self._log(CRITICAL, msg, args, caller=caller, **kwargs)

    # Modify Logger's _log() method to take an additional kwarg "caller".
    def _log(self, level, msg, args, exc_info=None, extra=None, caller=None):
        global _srcfile
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        if caller != None:
            fn, lno, func, *rest_ignored = caller
        else:
            if _srcfile:
                #IronPython doesn't track Python frames, so findCaller throws an
                #exception. We trap it here so that IronPython can use logging.
                try:
                    fn, lno, func = self.findCaller()
                except ValueError:
                    fn, lno, func = "(unknown file)", 0, "(unknown function)"
                    if hasattr(appdefs,'topFile'): fn = appdefs.topFile
            else:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
                if hasattr(appdefs,'topFile'): fn = appdefs.topFile
#        print("logging/__init__.py/Logger._log(): Got function: " + func.__str__() + "()",file=sys.stderr)
        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(self.name, level, fn, lno, msg, args, exc_info, func, extra)
        self.handle(record)
    # End method NormalLogger._log().
# End class NormalLogger.

    # Here, we actually modify the existing Logger class by adding our
    # new normal() and _log() methods to it.  We have to do it this way
    # since we can't as easily change the fact the logging.getLogger()
    # returns a Logger, not a NormalLogger.

logging.Logger.normal = NormalLogger.normal
logging.Logger._log = NormalLogger._log

    # The point of this mess is to also modify logging's getframe() method
    # to work in our situation (i.e., go back 1 fewer stack frames).

# next bit filched from 1.5.2's inspect.py
def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame

if hasattr(sys, '_getframe'): currentframe = lambda: sys._getframe(2)
# done filching

logging.currentframe = currentframe     # Reprogram logging's currentframe() method.


        #==============================================================
        #   NormalLoggerAdapter                 [module public class]
        #
        #       Does for LoggerAdapter what NormalLogger does
        #       for Logger.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class NormalLoggerAdapter(logging.LoggerAdapter):
    
    def normal(inst, msg:str, *args, caller=None, **kwargs):
        msg, kwargs = inst.process(msg, kwargs)
        if caller==None:                                
            caller = mainLogger.logger.findCaller()
        inst.logger.normal(msg, *args, caller=caller, **kwargs)

    # Override LoggerAdapter's standard logging methods to also find caller information.
    
    def debug(self, msg, *args, caller=None, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        if caller==None:                                
            caller = mainLogger.logger.findCaller()
        self.logger.debug(msg, *args, caller=caller, **kwargs)

    def info(self, msg, *args, caller=None, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        if caller==None:                                
            caller = mainLogger.logger.findCaller()
        self.logger.info(msg, *args, caller=caller, **kwargs)

    def warning(self, msg, *args, caller=None, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        if caller==None:                                
            caller = mainLogger.logger.findCaller()
        self.logger.warning(msg, *args, caller=caller, **kwargs)

    def error(self, msg, *args, caller=None, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        if caller==None:                                
            caller = mainLogger.logger.findCaller()
        self.logger.error(msg, *args, caller=caller, **kwargs)

    def critical(self, msg, *args, caller=None, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        if caller==None:                                
            caller = mainLogger.logger.findCaller()
        self.logger.critical(msg, *args, caller=caller, **kwargs)

    def exception(self, msg, *args, caller=None, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        if caller==None:                                
            caller = mainLogger.logger.findCaller()
        self.logger.exception(msg, *args, caller=caller, **kwargs)

    def FATAL(self, msg, *args, caller=None, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        if caller==None:                                
            caller = mainLogger.logger.findCaller()
        self.logger.fatal(msg, *args, caller=caller, **kwargs)

    # Set up a handy shorter name for the warning method.
NormalLoggerAdapter.warn = NormalLoggerAdapter.warning

    
    #==========================================================================
    #   NullOut                                         [module public class]
    #
    #       This class implements an output stream similar to Unix's
    #       "/dev/null" stream; it just silently does nothing with text
    #       that is written to it.
    #
    #       We use this as a temporary implementation of sys.stdout and
    #       sys.stderr in contexts where these streams have not been
    #       defined, such as when starting the script by double-clicking
    #       the ".pyw" version of the program icon.
    #
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class NullOut(io.TextIOBase):  # A simple class implementing a "null" output stream (i.e., bit-bucket).

    # Are these two methods enough, or do we need to implement a full set
    # of the empty abstract methods defined in io.TextIOBase or some such?

    def write(inst, s:str = "", *args, **kwargs):
        # Just return the length of the string, as if all characters were written.
        return len(s)
    
    def flush(inst, *args, **kwargs): pass   # Flushing the stream?  Do nothing.


    #===============================================================
    #   Function definitions.
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #==================================================================
        #   getLogger()                         [module public function]
        #
        #       Gets a Logger (or LoggerAdapter) object for use by
        #       the using module.  Makes sure the logger obtained has
        #       the normal() method.  Wraps a NormalLoggerAdapter around
        #       it, including the extra thread-local information from
        #       loggingContext.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def getLogger(name:str = appName):
    logger = logging.getLogger(name)    # Use the ordinary logging facility
        # to get the underlying logger.

    # Wraps a NormalLoggerAdapter with the extra LoggingContext information
    # around the logger returned by logging.getLogger().  Remember,
    # loggingContext is thread-local.
    wrapped_logger = NormalLoggerAdapter(logger, theLoggingContext)
    
    return wrapped_logger   # Return the wrapped-up logger.

    
        #==================================================================
        #   Concise logging functions.          [module public functions]
        #
        #       For modules that use the mainLogger for logging,
        #       these functions provide for logging more concisely
        #       than by explicitly invoking the logger.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        
def normal(msg:str, *args, **kwargs):
    caller = mainLogger.logger.findCaller()
    mainLogger.normal(msg, *args, caller=caller, **kwargs)
    
def debug(msg:str, *args, **kwargs):
    caller = mainLogger.logger.findCaller()
#    print("Got caller: (%s, %d, %s)" % caller, file=sys.stdout)
    mainLogger.debug(msg, *args, caller=caller, **kwargs)

def info(msg:str, *args, **kwargs):
    caller = mainLogger.logger.findCaller()
#    print("Got caller: (%s, %d, %s)" % caller, file=sys.stdout)
    mainLogger.info(msg, *args, caller=caller, **kwargs)

def warning(msg:str, *args, **kwargs):
    caller = mainLogger.logger.findCaller()
    mainLogger.warning(msg, *args, caller=caller, **kwargs)

warn = warning      # Serves as a shorter synonym.

def error(msg:str, *args, **kwargs):
    caller = mainLogger.logger.findCaller()
    mainLogger.error(msg, *args, caller=caller, **kwargs)

def exception(msg:str, *args, **kwargs):
    caller = mainLogger.logger.findCaller()

        # We surround the traceback above and below with "vvvv", "^^^^"
        # delimiter lines, to set it off from other output.
    
    print("v"*70,file=sys.stderr)       
    mainLogger.exception(msg, *args, caller=caller, **kwargs)
    print("^"*70,file=sys.stderr)
            #- WARNING:  The above code may do weird things (specifically,
            #   print the delimiters in one place and the traceback in
            #   another) if the console is shutting down and logging is being
            #   temporarily redirected to somewhere other than sys.stderr.
# End function exception().


def critical(msg:str, *args, **kwargs):
    caller = mainLogger.logger.findCaller()
    mainLogger.critical(msg, *args, caller=caller, **kwargs)


        #==================================================================
        #   lvlname_to_loglevel()               [module public function]
        #
        #       This function simply converts the string name of a
        #       given logging level to its numeric equivalent.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def lvlname_to_loglevel(lvlname):
    # We use the logging._levelNames dictionary b/c it already
    # has the reverse mappings as well as the forward ones.
    if lvlname in logging._levelNames.keys():   
        return logging._levelNames[lvlname]
    else:
        localLogger.error("There is no logging level named '%s'." % lvlname)
        return NOTSET


        #=====================================================
        #   byname()                [module public function]
        #
        #       This simply generates a log message using
        #       the main logger and the string name of the
        #       desired logging level.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def byname(lvlname, msg):
    caller = mainLogger.logger.findCaller()
    loglevel = lvlname_to_loglevel(lvlname)
    mainLogger.log(loglevel, msg, caller=caller)
    

        #==================================================================
        #   testLogging()                       [module public function]
        #
        #       Tests the logging facility for various message types.
        #       initLogMaster(), below, should already have been called.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def testLogging():
    moduleLogger.debug('This message just verifies that debug-level log output is enabled for this stream.')
    moduleLogger.info('This message just verifies that info-level log output is enabled for this stream.')
    moduleLogger.normal('This message just verifies that normal-level log output is enabled for this stream.')
    moduleLogger.warning('This message just verifies that warning-level log output is enabled for this stream.')    
    # Maybe shouldn't test these two b/c they look unnecessarily panicky & are always enabled anyway.
    moduleLogger.error('This message just verifies that error-level log output is enabled for this stream.')
    moduleLogger.critical('This message just verifies that critical-level log output is enabled for this stream.')


        #==================================================================
        #   updateStderr()                      [module public function]
        #
        #       In case the definition of sys.stderr changes, this
        #       function retrieves its new definition for use by the
        #       console output log handler (if that is defined).
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global consHandler
consHandler = None
def updateStderr():
    # The locking here prevents another thread from putting some
    # more output to the console handler after we flush it, and
    # before we redirect its stream.  Or from nulling out the
    # consHandler global after we check it and before we use it.
    logging._acquireLock()  
    if consHandler:
        consHandler.flush()
        consHandler.stream = sys.stderr
    logging._releaseLock()
    

        #==================================================================
        #   setLogLevels()                      [module public function]
        #
        #       Sets the file and console logging levels based on
        #       various configuration Booleans.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def setLogLevels(verbose=False):
    global console_level, log_level
    
        # Set the log level for the console based on whether we want to see warnings or not,
        # and whether the console is in debug mode.
        
    console_level = logging.WARNING     # Default setting.
    if CONS_DEBUG:
        if verbose:
            print("logmaster.setLogLevels(): Turning on detailed debug messages on console...",
                  file=sys.stderr)
        console_level = logging.DEBUG
    else:
        if not CONS_WARN:
            if verbose:
                print("logmaster.setLogLevels(): Suppressing warnings from console...",
                      file=sys.stderr)
            console_level = logging.ERROR
    if verbose:
        print("logmaster.setLogLevels(): Console log level is set to %d (%s)." %
              (console_level, logging.getLevelName(console_level)),
              file=sys.stderr)

        # Set the log level for the log file based on whether we want to log verbose info or not,
        # and whether the main logger is in debug mode.

    log_level = logging.INFO    # Default setting.
    if LOG_DEBUG:
        if verbose:
            print("logmaster.setLogLevels(): Turning on detailed debug messages in log file...",
                  file=sys.stderr)
        log_level = logging.DEBUG
        if not LOG_INFO:
            if verbose:
                print("logmaster.setLogLevels(): Suppressing verbose info from log file...",
                      file=sys.stderr)
            log_level = logging.NORMAL
    if verbose:
        print("logmaster.setLogLevels(): File log level is set to %d (%s)." %
              (log_level, logging.getLevelName(log_level)),
              file=sys.stderr)

# End setLogLevels().

        #=================================================================
        #   setDefaultRole()                            [public function]
        #
        #       If the current thread has no "role" attribute assigned,
        #       or if its role is "None", give it a default role called
        #       "general".  This is appropriate for the main thread.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def setDefaultRole():
    thread = threading.current_thread()                             # Get the current thread.
    if thread.name == "MainThread":                                 # If we're in the main thread,
        if not hasattr(thread, "role") or thread.role == None:           # and it has no role assigned yet,
            thread.role = "general"                                         # assign it a generic role.
        # The main thread's __str__() method also does something
        # ugly.  Fix it up by replacing it with ThreadActor's method.
        thread.__str__ = lambda: ThreadActor.__str__(thread)
    

        #==================================================================
        #   initLogMaster()                             [public function]
        #
        #       Basic initialization of the logmaster facility,
        #       called whenever this module is first loaded.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def initLogMaster():
    global logFormatter, theLoggingContext, mainLogger     # In python, we have to declare
    global consHandler, moduleLogger, initialized       # the globals that we'll reassign.
    global sysLogger, appLogger

        # Pretend the main thread is a ThreadActor by giving it a "role"
        # attribute.  This is descriptive, for debugging purposes.    

    setDefaultRole()

        # If we have no stdout/stderr streams yet (which will be the case
        # if the program was started by, for example, just double-clicking
        # on a script.pyw icon), temporarily assign them to null output
        # streams, just to make sure we won't crash if someone tries
        # to send log messages to the console before more effective values
        # of stdout/stderr have been set up.

    if sys.stdout == None:   sys.stdout = NullOut()
    if sys.stderr == None:   sys.stderr = NullOut()
        
        # Define a new logging level for "normal" messages that should be
        # echoed (without decoration) to standard output.  The level of this
        # is in between ERROR and WARNING, so that warnings can be suppressed
        # without suppressing normal output.

    logging.addLevelName(NORMAL_LEVEL,'NORMAL')
    logging.NORMAL = NORMAL_LEVEL

        # Create our main log file formatter.  This may be useful for
        # creating file log handlers in subordinate loggers that use
        # the same file format as the main file log handler.  This can
        # be changed if needed in a later call to configLogMaster().
        # (Note: Changing the logFormatter is not yet implemented.)

    logFormatter = logging.Formatter(LOG_FORMATSTR)
            # - LOG_FORMATSTR will be our normal log message format.

        # Set the default console and file logging levels based on the
        # module defaults.  (Don't print debug info since this is just
        # the default setting anyway.)

    setLogLevels(verbose=False)        

        # Set the default log file name, and its log level & format.
        # With the initial defaults, the log file will just contain
        # messages at INFO level or higher (no DEBUG).  To change
        # this, use configLogMaster().
        
    logging.basicConfig(filename=LOG_FILENAME,
                        level=log_level,
                        format=LOG_FORMATSTR)

        # Create the global loggingContext object.  This is thread-local, and
        # does not get initialized for a given thread until it is actually
        # first accessed within that thread.

    theLoggingContext = LoggingContext()   

        # Get the main (root) logger object for this environment.  Note this
        # uses our special getLogger() method defined above, which actually
        # creates a NormalLoggerAdapter wrapped around a Logger that is
        # mutated to look like a Normal Logger.  We don't use appName as the
        # logger name here, because we want modules that are not even
        # application-specific to still go through this logger.
    
    mainLogger = getLogger('')

        # Add a console log handler for messages (other than NORMAL messages)
        # that are (typically) at warning level or higher.  This will ensure
        # that these messages also appear on the stdout/stderr console.
    
    consHandler = logging.StreamHandler()      # The default stream handler uses stderr.
    consHandler.addFilter(AbnormalFilter())    # Add a filter to ignore NORMAL-level messages.
    consHandler.setLevel(console_level)        # Set console to log level we determined earlier.

        # Console log messages will just have the simple format showing the log
        # level name and the actual log message.  Look at the log file to see
        # more details such as thread, module, and function.

    consHandler.setFormatter(logging.Formatter("%(levelname)8s: %(message)s"))

        # Add the console log handler to the main logger adapter's underlying logger.

    mainLogger.logger.addHandler(consHandler)

        # Create a subordinate logger that is the top-level logger for system components.
    
    sysLogger = getLogger(sysName)

        # Create a subordinate logger that is the top-level logger for application components.

    appLogger = getLogger(appName)        

        # Get a subordinate logger for use by routines in this module.

    moduleLogger = getLogger('logmaster')    # For messages produced by this module only.

        # Remember that this module has already been initialized, to
        # make sure we don't try to initialize it again.

    initialized = True

# End initLogMaster().
        

        #==================================================================
        #   configLogMaster()                   [module public function]
        #
        #       Configure the logmaster facility.  Optional
        #       arguments can be used to modify various logmaster
        #       parameters from their preprogrammed defaults.
        #
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

# Rename this configLogMaster
def configLogMaster(sysname:str = None, appname:str = None, filename:str = None,
                  formatstr = None, conswarn:bool = None, consdebug:bool = None,
                  consinfo:bool = None, loginfo:bool = None, logdebug:bool = None,
                    component:str = None, role:str = None):

        # Do I really need to re-declare all these globals despite the
        # global statements at top level above?
    
    global NORMAL_LEVEL, UWSERR_LEVEL
    global LOG_FILENAME, LOG_FORMATSTR
    global CONS_WARN, LOG_INFO, LOG_DEBUG, CONS_DEBUG, CONS_INFO
    global systemName, sysName, appName
    global logFormatter, theLoggingContext, mainLogger, moduleLogger
    global initialized, consHandler
    global sysLogger, appLogger

        # Reinitialize some globals, if requested, in optional args.
        
    if sysname:
        sysName = systemName = sysname
        appdefs.systemName = sysname  # In case someone imports appdefs later.
            #-Warning: Other modules that have already imported
            # names from appdefs will still have the old value of
            # systemName in their module's copy of this global.

    if appname:
        appName = appname
        appdefs.appName = appname   # In case someone imports appdefs later.
            #-Warning: Other modules that have already imported
            # names from appdefs will still have the old value of
            # appName in their module's copy of this global.
        LOG_FILENAME = appName + ".log"
        
    if filename:            LOG_FILENAME                    = filename
    if formatstr:           LOG_FORMATSTR                   = formatstr
    if conswarn  != None:   CONS_WARN                       = conswarn        # Note:  False != None.
    if consinfo  != None:   CONS_INFO                       = consinfo
    if consdebug != None:   CONS_DEBUG                      = consdebug
    if loginfo   != None:   LOG_INFO                        = loginfo
    if logdebug  != None:   LOG_DEBUG                       = logdebug
    if component != None:   theLoggingContext.component     = component
    if role      != None:   theLoggingContext.threadrole    = role

    print("logmaster.configLogMaster(): The top-level log file is %s." % LOG_FILENAME,
          file=sys.stderr)

        # Start by appending a header to the log file for better human-readability.

    with open(LOG_FILENAME,'a') as tmp_file:
        tmp_file.write("========================+======================+============================================+================================================+===========================================================================================\n" +
                       "YYYY-MM-DD hh:mm:ss,msc | SysName.appName      | ThreadName:  Component   role              |      srcmodulename.py: ln#:functionName        | loglevel: Text\n"+
                       "------------------------+----------------------+--------------------------------------------|------------------------------------------------|-------------------------------------------------------------------------------------------\n")

        # Figure out the file and console log levels based on user selections.
        # (Verbose in this call is turned on for now, to confirm the final
        # post-config level settings to stderr.)
        
    setLogLevels(verbose=True)
    
        # Update the root log file name, logging level, and format.
        # NOTE: So far this only changes the logging level.  More
        # research into guts of logging module needed to figure out
        # how to surgically alter the log file name and log format
        # after the main root log file handler has already been
        # created.
        
    mainLogger.logger.setLevel(log_level)

# The following was our earlier attempt to change the logging
# parameters, which is commented out b/c it doesn't work! (b/c
# the root logger isn't affected, apparently).
#
#        # WARNING: I'm not sure this actually changes the root logger,
#        # which has already been created by this point!  So, if
#        # the log file or format changes, this might not be enough,
#        # we might have to go into the root logger and change its
#        # settings more surgically.
#
#    logging.basicConfig(filename=LOG_FILENAME, level=log_level, format=LOG_FORMATSTR)
            # - Eventually, we may want to change this to use a rotating file handler.

        # Update the console log handler's logging level.

    consHandler.setLevel(console_level)        # Set console to log level we determined earlier.

#    testLogging()      # Don't do this normally.

# End configLogMaster().
        

    #=================================================================================
    #   Module initialization.                                  [code section]
    #
    #       In this section, we have initialization code for the logmaster
    #       module, which is supposed to be executed whenever this module
    #       is first loaded.  Normally, a given module will only be loaded
    #       once anyway per python interprer session.  But, we check and
    #       set our "initialized" flag anyway,to make extra sure we don't
    #       accidentally re-initialize the module.  (To intentionally
    #       reinitialize it, users can explicitly call
    #       logmaster.initLogMaster().)
    #
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

if not initialized:     # If the module is not already initialized,
#    if hasattr(sys, "stderr") and sys.stderr != None:   # Needed b/c in some environments, it's not defined!
#        print("logmaster.py: Initializing logmaster module...", file=sys.stderr)
    initLogMaster()         # then initialize it.

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   End of logmaster.py module.
#=================================================================================
