"""
Head Pose Extraction Pipeline
Extracts head rotation angles from portrait photos using MediaPipe Face Mesh
Outputs JSON in format compatible with x6ud search-photos-by-model-tool
"""

import cv2
import mediapipe as mp
import numpy as np
import json
import os
from pathlib import Path
from typing import List, Dict, Optional

# MediaPipe Face Mesh setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


def estimate_head_pose(image_path: str) -> Optional[Dict]:
    """
    Extract head pose (pitch, yaw, roll) and face crop data from image.

    Returns dict with:
    - rx: pitch (rotation around x-axis, degrees)
    - ry: yaw (rotation around y-axis, degrees)
    - rz: roll (rotation around z-axis, degrees)
    - cx, cy: face crop center
    - cs: face crop size (square)
    - w, h: original image dimensions
    - url: image path/filename
    - tags: ["human"]
    """

    # Read image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to read: {image_path}")
        return None

    h, w, _ = image.shape

    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process with MediaPipe
    results = face_mesh.process(image_rgb)

    if not results.multi_face_landmarks:
        print(f"No face detected: {image_path}")
        return None

    # Get face landmarks (using first face)
    face_landmarks = results.multi_face_landmarks[0]

    # Convert normalized landmarks to pixel coordinates
    landmarks_px = []
    for landmark in face_landmarks.landmark:
        x_px = int(landmark.x * w)
        y_px = int(landmark.y * h)
        landmarks_px.append([x_px, y_px])

    landmarks_px = np.array(landmarks_px, dtype=np.float32)

    # Calculate bounding box for crop data
    x_min = int(np.min(landmarks_px[:, 0]))
    x_max = int(np.max(landmarks_px[:, 0]))
    y_min = int(np.min(landmarks_px[:, 1]))
    y_max = int(np.max(landmarks_px[:, 1]))

    # Calculate crop center and size (square)
    cx = (x_min + x_max) // 2
    cy = (y_min + y_max) // 2
    cs = max(x_max - x_min, y_max - y_min)

    # Estimate head pose using solvePnP
    # Key facial landmarks for pose estimation (indices from MediaPipe Face Mesh)
    # Nose tip, chin, left eye left corner, right eye right corner, left mouth corner, right mouth corner
    landmark_indices = [1, 152, 33, 263, 61, 291]

    # 2D image points
    image_points = np.array([
        landmarks_px[idx] for idx in landmark_indices
    ], dtype=np.float32)

    # 3D model points (generic face model in cm)
    model_points = np.array([
        (0.0, 0.0, 0.0),          # Nose tip
        (0.0, -8.0, -3.0),        # Chin
        (-5.0, 3.0, -2.0),        # Left eye left corner
        (5.0, 3.0, -2.0),         # Right eye right corner
        (-3.5, -4.0, -2.0),       # Left mouth corner
        (3.5, -4.0, -2.0)         # Right mouth corner
    ], dtype=np.float32)

    # Camera matrix (generic, assuming focal length ~= image width)
    focal_length = w
    center = (w / 2, h / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype=np.float32)

    # Assume no lens distortion
    dist_coeffs = np.zeros((4, 1))

    # Solve PnP to get rotation and translation vectors
    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points,
        image_points,
        camera_matrix,
        dist_coeffs,
        flags=cv2.SOLVEPNP_ITERATIVE
    )

    if not success:
        print(f"PnP failed: {image_path}")
        return None

    # Convert rotation vector to rotation matrix
    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

    # Extract Euler angles (in degrees)
    # Reference: https://learnopencv.com/rotation-matrix-to-euler-angles/
    sy = np.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2)
    singular = sy < 1e-6

    if not singular:
        pitch = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
        yaw = np.arctan2(-rotation_matrix[2, 0], sy)
        roll = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    else:
        pitch = np.arctan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
        yaw = np.arctan2(-rotation_matrix[2, 0], sy)
        roll = 0

    # Convert to degrees
    pitch_deg = int(np.degrees(pitch))
    yaw_deg = int(np.degrees(yaw))
    roll_deg = int(np.degrees(roll))

    # Check blur quality (Laplacian variance)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Skip blurry images (threshold ~50, adjust as needed)
    if blur_score < 50:
        print(f"Too blurry ({blur_score:.1f}): {image_path}")
        return None

    filename = os.path.basename(image_path)

    return {
        "rx": pitch_deg,
        "ry": yaw_deg,
        "rz": roll_deg,
        "url": f"./pipeline/input/{filename}",  # Relative path
        "cx": cx,
        "cy": cy,
        "cs": cs,
        "w": w,
        "h": h,
        "tags": ["human"]
    }


def check_blur(image_path: str, threshold: float = 100.0) -> float:
    """Calculate blur score using Laplacian variance."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return 0.0
    return cv2.Laplacian(image, cv2.CV_64F).var()


def process_directory(input_dir: str, output_json: str):
    """
    Process all images in directory and generate JSON index.
    """
    input_path = Path(input_dir)
    results = []

    # Supported image formats
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}

    # Get all image files
    image_files = [
        f for f in input_path.iterdir()
        if f.suffix.lower() in image_extensions
    ]

    print(f"Found {len(image_files)} images in {input_dir}")

    for i, image_file in enumerate(image_files, 1):
        print(f"Processing {i}/{len(image_files)}: {image_file.name}")

        pose_data = estimate_head_pose(str(image_file))

        if pose_data:
            results.append(pose_data)
            print(f"  OK - rx={pose_data['rx']}, ry={pose_data['ry']}, rz={pose_data['rz']}")

    print(f"\nSuccessfully processed: {len(results)}/{len(image_files)}")

    # Write JSON output
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Saved to: {output_json}")

    # Print angle distribution summary
    if results:
        print("\n=== Angle Distribution ===")
        pitches = [r['rx'] for r in results]
        yaws = [r['ry'] for r in results]
        rolls = [r['rz'] for r in results]

        print(f"Pitch (rx): min={min(pitches)}, max={max(pitches)}, avg={sum(pitches)/len(pitches):.1f}")
        print(f"Yaw (ry):   min={min(yaws)}, max={max(yaws)}, avg={sum(yaws)/len(yaws):.1f}")
        print(f"Roll (rz):  min={min(rolls)}, max={max(rolls)}, avg={sum(rolls)/len(rolls):.1f}")


if __name__ == "__main__":
    # Default paths
    input_dir = "./pipeline/input"
    output_json = "./pipeline/output/human.json"

    if not os.path.exists(input_dir):
        print(f"Error: Input directory not found: {input_dir}")
        print("Please create it and add portrait images.")
        exit(1)

    process_directory(input_dir, output_json)
