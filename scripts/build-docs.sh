#!/bin/bash
set -e

# Configuration
WIDOCO_VERSION="1.4.25"
WIDOCO_JAR="widoco-${WIDOCO_VERSION}-jar-with-dependencies_JDK-17.jar"
WIDOCO_URL="https://github.com/dgarijo/Widoco/releases/download/v${WIDOCO_VERSION}/${WIDOCO_JAR}"
INPUT_FILE="scimantic-core/ontology/scimantic.ttl"
OUTPUT_FOLDER="public"
CONF_FILE="scimantic-core/ontology/widoco.conf"

# Find suitable Java
JAVA_CMD="java"
if [ -x "/opt/homebrew/opt/openjdk@17/bin/java" ]; then
    JAVA_CMD="/opt/homebrew/opt/openjdk@17/bin/java"
elif [ -x "/usr/local/opt/openjdk@17/bin/java" ]; then
    JAVA_CMD="/usr/local/opt/openjdk@17/bin/java"
fi

# Download Widoco if missing
if [ ! -f "$WIDOCO_JAR" ]; then
    echo "Downloading Widoco v${WIDOCO_VERSION}..."
    curl -L -o "$WIDOCO_JAR" "$WIDOCO_URL"
fi

# 1. Regenerate Artifacts (Source of Truth)
if [ "$SKIP_GEN_ALL" != "true" ]; then
    echo "Regenerating artifacts from schema..."
    (cd scimantic-core && uv run gen-all)
else
    echo "Skipping gen-all (SKIP_GEN_ALL=true)..."
fi

# 2. Clean Public Folder
echo "Cleaning output folder..."
rm -rf "$OUTPUT_FOLDER"/*
mkdir -p "$OUTPUT_FOLDER"


# Run Widoco
echo "Generating documentation..."
"$JAVA_CMD" -jar "$WIDOCO_JAR" \
    -ontFile "$INPUT_FILE" \
    -outFolder "$OUTPUT_FOLDER" \
    -confFile "$CONF_FILE" \
    -uniteSections \
    -rewriteAll \
    -webVowl \
    -lang en

# Match CI workflow post-processing
# Flatten doc folder
if [ -d "$OUTPUT_FOLDER/doc" ]; then
    echo "Flattening content from $OUTPUT_FOLDER/doc to $OUTPUT_FOLDER"
    # Use rsnyc to merge or move safely
    cp -R "$OUTPUT_FOLDER/doc/"* "$OUTPUT_FOLDER/"
    rm -rf "$OUTPUT_FOLDER/doc"
fi

echo "Applying CI post-processing..."
# Rename index-en.html to index.html if needed
if [ -f "${OUTPUT_FOLDER}/index-en.html" ]; then
    cp "${OUTPUT_FOLDER}/index-en.html" "${OUTPUT_FOLDER}/index.html"
else
    echo "No index-en.html found. Skipping rename."
fi

echo "Build complete."
