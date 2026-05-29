#!/usr/bin/env bash
set -e

RAW_DIR="../../data/raw/culane"
MANIFEST_DIR="../../data/manifests/lane"
ANNOTATION_URL="https://drive.google.com/uc?export=download&id=1tSNGKGA52v0z5X23oW7_hTjQ4KIfiCst" # Mirror example

echo "[PilotWatch] Setting up CULane dataset structure..."

mkdir -p "$RAW_DIR/driver_23_30frames"
mkdir -p "$RAW_DIR/driver_161_90frames"
mkdir -p "$RAW_DIR/driver_182_30frames"
mkdir -p "$MANIFEST_DIR"

echo "[PilotWatch] Note: Full CULane image files require manual download via the official Baidu/Google Drive links due to licensing."

echo "[PilotWatch] Downloading annotations and list files..."
# Download annotations zip to raw directory
curl -L "$ANNOTATION_URL" -o "$RAW_DIR/annotations.zip" || echo "Warning: URL may be expired. Update link in script."

if [ -f "$RAW_DIR/annotations.zip" ]; then
    echo "[PilotWatch] Extracting annotations..."
    unzip -q "$RAW_DIR/annotations.zip" -d "$RAW_DIR/annotations"
    
    # Move split files to our manifest directory
    cp "$RAW_DIR/annotations/list/train_gt.txt" "$MANIFEST_DIR/culane_train.txt"
    cp "$RAW_DIR/annotations/list/val_gt.txt" "$MANIFEST_DIR/culane_val.txt"
    
    echo "[PilotWatch] Annotations mapped to $MANIFEST_DIR"
else
    echo "[PilotWatch] Skipping annotation extraction."
fi

echo "[PilotWatch] CULane setup complete."
