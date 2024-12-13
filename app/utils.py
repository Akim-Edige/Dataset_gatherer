import base64
import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


def extract_keypoints(image_np):
    """Extract hand keypoints from an image using Mediapipe."""
    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    keypoints = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            hand_keypoints = []
            for lm in hand_landmarks.landmark:
                hand_keypoints.append({
                    'x': lm.x,
                    'y': lm.y,
                    'z': lm.z
                })
            keypoints.append(hand_keypoints)
    return keypoints


def draw_keypoints(image_np, keypoints):
    """Draw keypoints on the image and return the annotated image."""
    for hand in keypoints:
        for point in hand:
            x = int(point['x'] * image_np.shape[1])
            y = int(point['y'] * image_np.shape[0])
            cv2.circle(image_np, (x, y), 5, (0, 255, 0), -1)  # Green dots
    # Encode annotated image to Base64
    _, buffer = cv2.imencode('.jpg', image_np)
    annotated_image_base64 = base64.b64encode(buffer).decode('utf-8')
    return annotated_image_base64
