#!/bin/bash
set -e

# Run build script
./scripts/build-docs.sh

# Serve
echo "--------------------------------------------------------"
echo "Documentation generated in public/"
echo "Starting local server at http://localhost:8000"
echo "Press Ctrl+C to stop."
echo "--------------------------------------------------------"
python3 -m http.server 8000 --directory "public"
