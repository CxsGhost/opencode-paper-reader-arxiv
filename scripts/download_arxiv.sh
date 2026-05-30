#!/bin/bash
# download_arxiv.sh
# Helper script to download arXiv paper LaTeX source
# Usage: ./download_arxiv.sh <arxiv_id> [output_dir]

set -e

ARXIV_ID="$1"
OUTPUT_DIR="${2:-.}"

if [ -z "$ARXIV_ID" ]; then
    echo "Usage: $0 <arxiv_id> [output_dir]"
    echo "Example: $0 2512.15745 ./my_papers"
    exit 1
fi

# Validate arXiv ID format (basic check)
if ! echo "$ARXIV_ID" | grep -qE '^[0-9]+(\.[0-9]+)?$'; then
    echo "Error: Invalid arXiv ID format: $ARXIV_ID"
    echo "Expected format: XXXX.XXXXX or XXXX"
    exit 1
fi

DOWNLOAD_URL="https://arxiv.org/src/${ARXIV_ID}"
ARCHIVE_NAME="arxiv_${ARXIV_ID}.tar.gz"

echo "Downloading arXiv source for ID: $ARXIV_ID"
echo "URL: $DOWNLOAD_URL"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# Download the source archive
echo "Downloading..."
if ! curl -L -o "$ARCHIVE_NAME" "$DOWNLOAD_URL"; then
    echo "Error: Failed to download from $DOWNLOAD_URL"
    exit 1
fi

# Check if download was successful (arXiv returns HTML error page on failure)
if file "$ARCHIVE_NAME" | grep -q "HTML"; then
    echo "Error: arXiv returned an error page. The paper ID may be invalid or source is not available."
    rm "$ARCHIVE_NAME"
    exit 1
fi

# Create extraction directory
EXTRACT_DIR="paper_${ARXIV_ID}"
mkdir -p "$EXTRACT_DIR"

# Extract the archive
echo "Extracting..."
if ! tar -xzf "$ARCHIVE_NAME" -C "$EXTRACT_DIR"; then
    echo "Error: Failed to extract archive"
    rm "$ARCHIVE_NAME"
    exit 1
fi

# Remove the archive after extraction
rm "$ARCHIVE_NAME"

# Create analysis_report directory
mkdir -p "$EXTRACT_DIR/analysis_report"

echo "Success! Paper source extracted to: $OUTPUT_DIR/$EXTRACT_DIR"
echo "Analysis reports should be placed in: $OUTPUT_DIR/$EXTRACT_DIR/analysis_report/"

# List extracted files
echo ""
echo "Extracted files:"
find "$EXTRACT_DIR" -maxdepth 2 -type f | head -20
