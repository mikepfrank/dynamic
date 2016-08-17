::|============================================================================
::|
::|		edit-demo.bat								[MS Windows batch file]
::|
::|			This batch file simply runs the Dynamic demo script.
::|			It assumes that an appropriate version of Python
::|			(currently version 3.5.x) is in the user's %PATH%.
::|
::|----------------------------------------------------------------------------
@echo off

set DEMO_SCRIPT=dynamic-demo.py

python %DEMO_SCRIPT%

echo.
echo Batch file will terminate in 10 seconds...
timeout 10
