@echo off
REM build_inno.bat — builds installer exe
where iscc.exe >nul 2>&1
if %errorlevel% neq 0 (
  if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
  if exist "C:\Program Files\Inno Setup 6\ISCC.exe" set ISCC="C:\Program Files\Inno Setup 6\ISCC.exe"
) else set ISCC=iscc.exe
echo Building with %ISCC%...
%ISCC% katzos_prime_inno.iss
%ISCC% katzos_minimal.iss
dir KatzOS-Prime-*.exe
pause
