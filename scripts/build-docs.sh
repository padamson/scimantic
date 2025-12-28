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
echo "Applying CI post-processing..."
# Rename index-en.html to index.html if needed
if [ -f "${OUTPUT_FOLDER}/index-en.html" ]; then
    mv "${OUTPUT_FOLDER}/index-en.html" "${OUTPUT_FOLDER}/index.html"
fi

# Create /ontology redirect for local testing
mkdir -p "${OUTPUT_FOLDER}/ontology"
cp "${OUTPUT_FOLDER}/index.html" "${OUTPUT_FOLDER}/ontology/index.html"

echo "Build complete."
