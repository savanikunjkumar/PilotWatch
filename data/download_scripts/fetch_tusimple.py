import os
import urllib.request
import zipfile
import hashlib
import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw" / "tusimple"
MANIFEST_DIR = BASE_DIR / "data" / "manifests" / "lane"

# TuSimple Train set (Mock/Mirror URL for demonstration)
TUSIMPLE_URL = "https://s3.us-east-2.amazonaws.com/tusimple/train_set.zip"
EXPECTED_HASH = "mock_hash_value_replace_in_production"

def calculate_sha256(filepath):
    """Calculates SHA256 to ensure data integrity."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def transform_to_manifest(raw_json_paths, output_manifest):
    """Combines TuSimple's scattered JSONs into one unified manifest."""
    unified_data = []
    for json_path in raw_json_paths:
        with open(json_path, 'r') as f:
            for line in f:
                unified_data.append(json.loads(line))
                
    with open(output_manifest, 'w') as out:
        json.dump(unified_data, out, indent=2)
    print(f"[PilotWatch] Unified manifest created at {output_manifest}")

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = RAW_DIR / "tusimple_train.zip"

    if not zip_path.exists():
        print(f"[PilotWatch] Downloading TuSimple dataset to {zip_path}...")
        urllib.request.urlretrieve(TUSIMPLE_URL, zip_path)
    else:
        print("[PilotWatch] Archive already exists. Skipping download.")

    print("[PilotWatch] Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(RAW_DIR)
        
    # Find all label data json files
    label_files = list(RAW_DIR.glob("label_data_*.json"))
    manifest_out = MANIFEST_DIR / "tusimple_train.json"
    
    transform_to_manifest(label_files, manifest_out)
    print("[PilotWatch] TuSimple dataset successfully provisioned.")

if __name__ == "__main__":
    main()
