from flask import Blueprint, render_template, request, jsonify
import os
import json
from datetime import datetime
from .utils import extract_keypoints, draw_keypoints
from .config import DATASET_DIR, SIGNS, LABELS_FILE, METADATA_FILE
import base64
import numpy as np
import cv2

main_bp = Blueprint('main', __name__)

# Ensure dataset directories exist
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

# Load labels
if not os.path.exists(LABELS_FILE):
    labels_dict = {sign: idx for idx, sign in enumerate(SIGNS)}
    with open(LABELS_FILE, 'w') as f:
        json.dump(labels_dict, f)
else:
    with open(LABELS_FILE, 'r') as f:
        labels_dict = json.load(f)

# Metadata file
if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'w') as f:
        f.write('filename,sign,label_id,timestamp\n')

@main_bp.route('/')
def index():
    return render_template('index.html', signs=SIGNS)


@main_bp.route('/capture_image', methods=['POST'])
def capture_image():
    data = request.get_json()
    image_data = data.get('image')
    sign = data.get('sign')

    if not image_data or not sign:
        return jsonify({'message': 'Invalid data'}), 400

    try:
        # Decode the base64 image
        header, encoded = image_data.split(',', 1)
        image_bytes = base64.b64decode(encoded)

        # Convert bytes to OpenCV image
        nparr = np.frombuffer(image_bytes, np.uint8)
        image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image_np is None:
            return jsonify({'message': 'Failed to decode image'}), 400

        # Extract keypoints
        keypoints = extract_keypoints(image_np)
        if keypoints:
            # Create annotated image
            annotated_image_base64 = draw_keypoints(image_np.copy(), keypoints)
        else:
            annotated_image_base64 = None
            print("No hands detected.")

        response = {
            'message': 'Image processed',
            'keypoints_saved': keypoints is not None
        }

        if annotated_image_base64:
            response['annotated_image'] = f"data:image/jpeg;base64,{annotated_image_base64}"
            response['original_image'] = f"data:image/jpeg;base64,{encoded}"  # Send original image as well
            response['keypoints'] = keypoints  # Send keypoints for saving if confirmed

        return jsonify(response), 200

    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'message': 'An error occurred during processing.'}), 500


@main_bp.route('/save_image', methods=['POST'])
def save_image():
    data = request.get_json()
    annotated_image_data = data.get('annotated_image')
    original_image_data = data.get('original_image')
    sign = data.get('sign')
    keypoints = data.get('keypoints')

    if not annotated_image_data or not original_image_data or not sign or not keypoints:
        return jsonify({'message': 'Invalid data'}), 400

    try:
        # Decode the original image
        header_orig, encoded_orig = original_image_data.split(',', 1)
        original_image_bytes = base64.b64decode(encoded_orig)

        # Decode the annotated image
        header_ann, encoded_ann = annotated_image_data.split(',', 1)
        annotated_image_bytes = base64.b64decode(encoded_ann)

        # Create sign directories if they don't exist
        sign_dir_original = os.path.join(DATASET_DIR, sign, 'original_images')
        sign_dir_annotated = os.path.join(DATASET_DIR, sign, 'annotated_images')
        annotations_dir = os.path.join(DATASET_DIR, sign, 'annotations')

        os.makedirs(sign_dir_original, exist_ok=True)
        os.makedirs(sign_dir_annotated, exist_ok=True)
        os.makedirs(annotations_dir, exist_ok=True)

        # Create a unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename_original = f"{sign}_{timestamp}_original.jpg"
        filename_annotated = f"{sign}_{timestamp}_annotated.jpg"
        filepath_original = os.path.join(sign_dir_original, filename_original)
        filepath_annotated = os.path.join(sign_dir_annotated, filename_annotated)

        # Save the original image
        with open(filepath_original, 'wb') as f:
            f.write(original_image_bytes)

        # Save the annotated image
        with open(filepath_annotated, 'wb') as f:
            f.write(annotated_image_bytes)

        # Save keypoints to annotation file
        annotation = {
            'filename_original': filename_original,
            'filename_annotated': filename_annotated,
            'sign': sign,
            'keypoints': keypoints
        }
        annotation_file = os.path.join(annotations_dir, f"{sign}_{timestamp}.json")
        with open(annotation_file, 'w') as f:
            json.dump(annotation, f)

        # Update metadata
        label_id = labels_dict.get(sign, -1)
        with open(METADATA_FILE, 'a') as f:
            f.write(f"{filename_original},{sign},{label_id},{timestamp}\n")
            f.write(f"{filename_annotated},{sign},{label_id},{timestamp}\n")

        return jsonify({'message': f'Images saved as {filename_original} and {filename_annotated}'}), 200

    except Exception as e:
        print(f"Error saving images: {e}")
        return jsonify({'message': 'An error occurred while saving the images.'}), 500


@main_bp.route('/capture_video', methods=['POST'])
def capture_video():
    data = request.get_json()
    video_data = data.get('video')
    sign = data.get('sign')

    if not video_data or not sign:
        return jsonify({'message': 'Invalid data'}), 400

    # Decode the base64 video
    header, encoded = video_data.split(',', 1)
    video_bytes = base64.b64decode(encoded)


    # Create sign directory if it doesn't exist
    sign_dir = os.path.join(DATASET_DIR, sign, 'videos')
    if not os.path.exists(sign_dir):
        os.makedirs(sign_dir)

    # Create a unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{sign}_{timestamp}.webm"
    filepath = os.path.join(sign_dir, filename)

    # Save the video
    with open(filepath, 'wb') as f:
        f.write(video_bytes)

    return jsonify({'message': f'Video saved as {filename}'}), 200
