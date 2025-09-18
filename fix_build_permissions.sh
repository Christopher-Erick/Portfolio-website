#!/bin/bash
# Script to fix build script permissions and line endings

# Convert line endings to Unix format and make executable
sed -i 's/\r$//' build_fixed
chmod +x build_fixed

echo "Build script permissions fixed!"