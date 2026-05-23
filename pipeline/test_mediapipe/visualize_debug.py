"""
MediaPipe Face Detection Debug Visualizer
Shows landmarks, crop box, rotation angles on images
"""

import cv2
import mediapipe as mp
import numpy as np
import os
from pathlib import Path

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)


def visualize_face_detection(image_path: str, output_dir: str):
    """Process image and create debug visualization"""

    # Read image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to read: {image_path}")
        return

    h, w, _ = image.shape
    debug_image = image.copy()

    # Convert to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if not results.multi_face_landmarks:
        print(f"No face detected: {image_path}")
        return

    face_landmarks = results.multi_face_landmarks[0]

    # Convert landmarks to pixel coords
    landmarks_px = []
    for landmark in face_landmarks.landmark:
        x_px = int(landmark.x * w)
        y_px = int(landmark.y * h)
        landmarks_px.append([x_px, y_px])

    landmarks_px = np.array(landmarks_px, dtype=np.float32)

    # Draw all face mesh landmarks (light blue dots)
    for lm in landmarks_px:
        cv2.circle(debug_image, (int(lm[0]), int(lm[1])), 1, (255, 200, 100), -1)

    # Calculate bounding box
    x_min = int(np.min(landmarks_px[:, 0]))
    x_max = int(np.max(landmarks_px[:, 0]))
    y_min = int(np.min(landmarks_px[:, 1]))
    y_max = int(np.max(landmarks_px[:, 1]))

    # Draw tight bbox (RED)
    cv2.rectangle(debug_image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)
    cv2.putText(debug_image, "Face BBox", (x_min, y_min - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Calculate crop with padding
    face_width = x_max - x_min
    face_height = y_max - y_min
    padding_factor = 1.4

    cx = (x_min + x_max) // 2
    cy = (y_min + y_max) // 2
    cs = int(max(face_width, face_height) * padding_factor)

    # Draw crop box (GREEN)
    crop_x1 = cx - cs // 2
    crop_y1 = cy - cs // 2
    crop_x2 = cx + cs // 2
    crop_y2 = cy + cs // 2

    cv2.rectangle(debug_image, (crop_x1, crop_y1), (crop_x2, crop_y2), (0, 255, 0), 3)
    cv2.circle(debug_image, (cx, cy), 5, (0, 255, 0), -1)
    cv2.putText(debug_image, f"Crop Center ({cx},{cy})", (cx + 10, cy),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(debug_image, f"Crop Size: {cs}px", (crop_x1, crop_y1 - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Key landmarks for pose estimation (YELLOW circles)
    key_indices = [1, 152, 33, 263, 61, 291]  # nose, chin, eyes, mouth
    key_names = ["Nose", "Chin", "L Eye", "R Eye", "L Mouth", "R Mouth"]

    for idx, name in zip(key_indices, key_names):
        pt = landmarks_px[idx]
        cv2.circle(debug_image, (int(pt[0]), int(pt[1])), 4, (0, 255, 255), -1)
        cv2.putText(debug_image, name, (int(pt[0]) + 5, int(pt[1]) - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

    # Calculate rotation angles
    image_points = np.array([landmarks_px[idx] for idx in key_indices], dtype=np.float32)

    model_points = np.array([
        (0.0, 0.0, 0.0),          # Nose tip
        (0.0, -8.0, -3.0),        # Chin
        (-5.0, 3.0, -2.0),        # Left eye
        (5.0, 3.0, -2.0),         # Right eye
        (-3.5, -4.0, -2.0),       # Left mouth
        (3.5, -4.0, -2.0)         # Right mouth
    ], dtype=np.float32)

    focal_length = w
    center = (w / 2, h / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype=np.float32)

    dist_coeffs = np.zeros((4, 1))

    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points,
        image_points,
        camera_matrix,
        dist_coeffs,
        flags=cv2.SOLVEPNP_ITERATIVE
    )

    if success:
        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

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

        # Original angles
        pitch_deg = int(np.degrees(pitch))
        yaw_deg = int(np.degrees(yaw))
        roll_deg = int(np.degrees(roll))

        # Negated angles
        pitch_neg = -pitch_deg
        yaw_neg = -yaw_deg

        # Draw rotation info (WHITE background)
        info_y = 30
        cv2.rectangle(debug_image, (10, 10), (400, 160), (255, 255, 255), -1)
        cv2.putText(debug_image, f"Original Angles:", (20, info_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        info_y += 25
        cv2.putText(debug_image, f"  Pitch (rx): {pitch_deg}", (20, info_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        info_y += 20
        cv2.putText(debug_image, f"  Yaw   (ry): {yaw_deg}", (20, info_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        info_y += 20
        cv2.putText(debug_image, f"  Roll  (rz): {roll_deg}", (20, info_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        info_y += 30
        cv2.putText(debug_image, f"Negated Angles (current):", (20, info_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        info_y += 25
        cv2.putText(debug_image, f"  Pitch: {pitch_neg}  Yaw: {yaw_neg}", (20, info_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Save debug image
    filename = Path(image_path).stem
    output_path = os.path.join(output_dir, f"{filename}_debug.jpg")
    cv2.imwrite(output_path, debug_image)
    print(f"Saved debug: {output_path}")


if __name__ == "__main__":
    input_dir = "../input"
    output_dir = "./output"

    os.makedirs(output_dir, exist_ok=True)

    input_path = Path(input_dir)
    image_files = [f for f in input_path.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]

    print(f"Processing {len(image_files)} images...")

    for img_file in image_files:
        print(f"\nProcessing: {img_file.name}")
        visualize_face_detection(str(img_file), output_dir)

    print(f"\nDone! Check {output_dir}/ for debug images")
