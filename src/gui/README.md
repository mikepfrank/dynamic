# Dynamic GUI package (`dynamic/src/gui/`).

This directory defines the `gui` package of the Dynamic system, 
which implements the graphical user interface.  At this time it
is still experimental and very much under construction.

## 1. Module hierarchy.

The dependency diagram of modules within this package is roughly as follows
(indirect dependencies may not all be shown):

                 _______________
    Package     /               \
    module:     |      gui      |
                | (__init__.py) |
                \_______________/
    Modules in      |       |   
    package:        V       V 
              dyngui.py   tikiterm.py
                     |     |    |   |
                     V     V    |   V
                    guiapp.py   |  terminal.py
                        |       |
                        V       V
                    +--worklist.py--+   
                    |       |       |
                    V       V       V
              desque.py  flag.py  utils.py

The `gui` package uses the top-level module `logmaster.py`.

The `gui` package is used by the main application script `dynamic-demo.py`.

## 2. Working modules.

The following modules have been tested and are part of the
current system.  Below, they are presented in order from 
lowest-level to highest-level (later ones depend on earlier 
ones.)

### 2.1. Utilities module (`utils.py`).

This module defines miscellaneous utilities, only one of which 
is actually used by the GUI package.  It could be simplified.
It is referenced by the `worklist` module.

### 2.2. Flag module (`flag.py`).

This module defines classes for waitable, checkable condition
variables.  These are useful for inter-thread coordination and 
are a little more flexible than Python's built-in conditions.
The `flag` module is referenced by the `worklist` module.

### 2.3. Desque module (`desque.py`).

This module defines a class for double-ended synchronous 
queues.  These are like ordinary synchronous queues except
that items can be inserted at the front of the queue as well 
as at the back.  They are useful for inter-thread communication.
The `desque` module is referenced by the `worklist` module.

### 2.4. Worklist module (`worklist.py`).

This module defines classes for Worker threads that execute
queues ("worklists") of tasks sent to them by other threads.
Depends on the `utils`, `flag`, and `desque` modules.

### 2.5. GUI application module (`guiapp.py`).

This module defines classes that facilitate implementing 
multithreaded GUI applications.

### 2.6. Terminal module (`terminal.py`).

Generic class for terminal implementations.  Barely used at present.

### 2.7. Tikiterm module (`tikiterm.py`).

This module implements a graphical terminal emulator using TkInter's Text widget.

### 2.8. Dynamic-specific GUI module (`dyngui.py`).

This module defines GUI elements specific to the Dynamic application.

### 2.9. Package initialization module (`__init__.py`).

This module is automatically loaded when the package is first accessed,
and it performs initialization operations associated with the package.
