@echo off
REM Script to set correct permissions for build scripts

echo Setting execute permissions for build scripts...

REM On Windows, we don't need to set execute permissions the same way
REM But we can ensure the files exist and display a message

if exist "build.sh" (
    echo ✅ build.sh exists
) else (
    echo ❌ build.sh not found
)

if exist "build.bat" (
    echo ✅ build.bat exists
) else (
    echo ❌ build.bat not found
)

echo.
echo For Unix/Linux/Mac systems (including Render), run:
echo   chmod +x build.sh
echo.
echo For Windows systems, the batch file should work directly.
echo.
echo All build scripts are ready for deployment!