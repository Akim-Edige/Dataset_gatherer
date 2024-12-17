import json
import pytest
from app import create_app

with open('sample_photo.txt', 'r') as f:
    sample_image = f.read()

with open('sample_photo.txt', 'r') as f:
    sample_video = f.read()

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test the main index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Sign Language Data Collector' in response.data


def test_capture_image(client):
    """Test image capture functionality."""
    test_image_data = {
        "image": sample_image,
        "sign": "hello"
    }

    response = client.post('/capture_image', json=test_image_data)
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert 'message' in response_json
    assert response_json['message'] == 'Image processed'
    assert 'keypoints_saved' in response_json


def test_save_image(client):
    """Test saving the image with annotations."""
    test_save_data = {
        "annotated_image": sample_image,
        "original_image": sample_image,
        "sign": "hello",
        "keypoints": [{"x": 0.1, "y": 0.2, "z": 0.3}]
    }

    response = client.post('/save_image', json=test_save_data)
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert 'message' in response_json
    assert 'Video saved' not in response_json


def test_capture_video(client):
    """Test video capture functionality."""
    test_video_data = {
        "video": sample_video,
        "sign": "yes"
    }

    response = client.post('/capture_video', json=test_video_data)
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert 'message' in response_json
    assert 'Video saved as' in response_json['message']

if __name__ == "__main__":
    client()
