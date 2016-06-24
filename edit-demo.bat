::|============================================================================
::|
::|		edit-demo.bat								[MS Windows batch file]
::|
::|			This batch file just brings up Python 3.5's IDLE editor
::|			editing the top-level source file of the Dynamic demo.
::|
::|			It assumes that Python 3.5.1 is in %PATH% and also that
::|			it's installed in the following folder under the user's
::|			home folder:
::|
::|				AppData\Local\Programs\Python\Python35\
::|
::|----------------------------------------------------------------------------

@echo off

echo In batch file %0...
echo.

set PYDIR=%APPDATA%\..\Local\Programs\Python\Python35
set PYLIB=%PYDIR%\Lib
set DEMO_SCRIPT=dynamic-demo.py

echo Editing demo script %DEMO_SCRIPT%...
start pythonw %PYLIB%\idlelib\idle.pyw %DEMO_SCRIPT%

echo.
echo Batch file is terminating...
timeout 5

::pause
::set /p bye=Press enter to exit: 