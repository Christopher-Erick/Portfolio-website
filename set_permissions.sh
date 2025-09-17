#!/bin/bash
# Script to set correct permissions for build scripts

echo "Setting execute permissions for build scripts..."

# Make build scripts executable
chmod +x build.sh
echo "✅ Made build.sh executable"

if [ -f "build.bat" ]; then
    chmod +x build.bat
    echo "✅ Made build.bat executable"
fi

echo "✅ All build scripts now have execute permissions"
echo "You can now deploy to Render without permission issues"