@echo off
REM Script to set permissions on all build scripts for Windows

echo Setting permissions on build scripts...

REM Set permissions on build scripts
icacls build /grant Everyone:F
icacls build.sh /grant Everyone:F
icacls build.bat /grant Everyone:F

echo Permissions set successfully!