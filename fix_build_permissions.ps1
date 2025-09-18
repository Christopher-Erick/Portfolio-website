# PowerShell script to fix build script permissions and line endings

# Convert line endings to Unix format and make executable
(Get-Content build_fixed) -replace "`r`n", "`n" | Set-Content build_fixed -Force

# Make the file executable (this is more for documentation as Windows doesn't use chmod)
Write-Host "Build script line endings fixed for Unix compatibility!"