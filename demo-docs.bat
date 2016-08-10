::|============================================================================
::|
::|		demo-docs.bat								[MS Windows batch file]
::|
::|			This batch file uses pydoc3 to generate documentation
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
set PYSCR=%PYDIR%\Tools\scripts

echo Starting Python documentation server...
echo Enter 'b' at the prompt to view docs in default web browser.
echo.

:: The following serves up documentation on http://localhost:1234.
:: Hit 'b' at the prompt to start the default browser pointing to there.
python %PYSCR%\pydoc3.py -p 1234

echo.
echo Batch file is terminating...
timeout 5

::pause
::set /p bye=Press enter to exit: 