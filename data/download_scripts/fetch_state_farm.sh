#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -e

RAW_DIR="../../data/raw/state_farm"
MANIFEST_DIR="../../data/manifests/driver"

echo "[PilotWatch] Initiating State Farm dataset download..."

# 1. Dependency Check
if ! command -v kaggle &> /dev/null; then
    echo "ERROR: Kaggle CLI could not be found. Please install it via 'pip install kaggle'"
    echo "Ensure your ~/.kaggle/kaggle.json credentials are set up."
    exit 1
fi

# 2. Directory Setup
mkdir -p "$RAW_DIR"
mkdir -p "$MANIFEST_DIR"

# 3. Download & Extract
echo "[PilotWatch] Downloading from Kaggle..."
kaggle competitions download -c state-farm-distracted-driver-detection -p "$RAW_DIR"

echo "[PilotWatch] Extracting archive..."
unzip -q "$RAW_DIR/state-farm-distracted-driver-detection.zip" -d "$RAW_DIR"
rm "$RAW_DIR/state-farm-distracted-driver-detection.zip"

# 4. Generate Initial Manifest
echo "[PilotWatch] Generating train_split.csv manifest..."
# The dataset comes with driver_imgs_list.csv. We copy it to our manifest folder 
# so the data loaders can read it without touching the raw directory.
cp "$RAW_DIR/driver_imgs_list.csv" "$MANIFEST_DIR/train_split.csv"

# 5. Create Class Map
cat <<EOF > "$MANIFEST_DIR/class_map.json"
{
  "c0": "safe driving", "c1": "texting - right", "c2": "talking on the phone - right",
  "c3": "texting - left", "c4": "talking on the phone - left", "c5": "operating the radio",
  "c6": "drinking", "c7": "reaching behind", "c8": "hair and makeup", "c9": "talking to passenger"
}
EOF

echo "[PilotWatch] State Farm data ready in $RAW_DIR"
