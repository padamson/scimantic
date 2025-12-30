#!/bin/bash

# Ensure build script acts as source of truth
BUILD_SCRIPT="./scripts/build-docs.sh"
OUTPUT_FOLDER="public"

# Initial build
$BUILD_SCRIPT

# Clean up background process on exit
trap "kill 0" EXIT

# Start server in background
echo "--------------------------------------------------------"
echo "Starting local server at http://localhost:8000"
echo "Monitoring scimantic-core/schema for changes..."
echo "--------------------------------------------------------"
python3 -m http.server 8000 --directory "$OUTPUT_FOLDER" &

# Watch for changes
# Exclude public folder to avoid infinite loops if generic watch used
fswatch -o scimantic-core/schema | while read num; do
    echo "Change detected. Rebuilding..."
    $BUILD_SCRIPT
    echo "Refreshed. (Note: You still need to manually refresh the browser)"
done
