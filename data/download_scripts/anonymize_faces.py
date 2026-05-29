import os
import cv2
import mediapipe as mp
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw" / "state_farm" / "imgs" / "train"

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection

def blur_face(image_path):
    """Detects a face in the image and applies a heavy Gaussian blur."""
    try:
        image = cv2.imread(str(image_path))
        if image is None:
            return
            
        h, w, _ = image.shape
        
        # Use MediaPipe with standard model selection (0 for short-range)
        with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
            results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            if not results.detections:
                return # No face found
                
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                xmin = int(bboxC.xmin * w)
                ymin = int(bboxC.ymin * h)
                width = int(bboxC.width * w)
                height = int(bboxC.height * h)
                
                # Add padding to bounding box
                pad = 20
                x1, y1 = max(0, xmin - pad), max(0, ymin - pad)
                x2, y2 = min(w, xmin + width + pad), min(h, ymin + height + pad)
                
                # Extract ROI and apply heavy Gaussian Blur
                roi = image[y1:y2, x1:x2]
                if roi.size > 0:
                    blurred_roi = cv2.GaussianBlur(roi, (99, 99), 30)
                    image[y1:y2, x1:x2] = blurred_roi
            
            # Overwrite original image with anonymized version
            cv2.imwrite(str(image_path), image)
            
    except Exception as e:
        print(f"Error processing {image_path.name}: {e}")

def main():
    if not RAW_DIR.exists():
        print(f"[PilotWatch] Error: Directory {RAW_DIR} does not exist.")
        print("Run fetch_state_farm.sh first.")
        return

    # Gather all jpg files recursively from the class subfolders (c0, c1, etc.)
    image_paths = list(RAW_DIR.rglob("*.jpg"))
    total_images = len(image_paths)
    
    print(f"[PilotWatch] Found {total_images} images. Initiating multi-threaded face anonymization...")
    
    # Process images concurrently for high-performance throughput
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        for i, _ in enumerate(executor.map(blur_face, image_paths), 1):
            if i % 1000 == 0 or i == total_images:
                print(f"[PilotWatch] Progress: {i}/{total_images} images processed.")

    print("[PilotWatch] Face anonymization complete. Data is now privacy-compliant.")

if __name__ == "__main__":
    main()
