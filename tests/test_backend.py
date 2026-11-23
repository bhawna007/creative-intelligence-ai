
from fastapi.testclient import TestClient
from pathlib import Path
from backend.main import app

import cv2
import numpy as np

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"].startswith(
        "Welcome to Creative Intelligence AI"
    )


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["application"] == "Creative Intelligence AI"


def test_upload_rejects_invalid_file_type():
    response = client.post(
        "/upload-image",
        files={
            "file": (
                "test.txt",
                b"This is not an image",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert "Only JPG, PNG and WEBP" in response.json()["detail"]


def test_upload_rejects_empty_file():
    response = client.post(
        "/upload-image",
        files={
            "file": (
                "empty.jpg",
                b"",
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded image is empty."





def test_upload_valid_image():
    image_path = (
        Path(__file__).parent.parent
        / "data"
        / "sample_ads"
        / "product_advertisement.jpg"
    )

    assert image_path.exists(), "Sample advertisement image not found"

    with open(image_path, "rb") as image_file:
        response = client.post(
            "/upload-image",
            files={
                "file": (
                    "product_advertisement.jpg",
                    image_file,
                    "image/jpeg"
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["validation"] == "Image is valid"
    assert data["message"] == "Image uploaded and analyzed successfully!"
    assert "analysis" in data
    assert "Updated Design Score" in data["analysis"]

def test_upload_rejects_small_image():
    small_image = np.zeros((80, 80, 3), dtype=np.uint8)

    success, encoded_image = cv2.imencode(".jpg", small_image)

    assert success

    response = client.post(
        "/upload-image",
        files={
            "file": (
                "small_image.jpg",
                encoded_image.tobytes(),
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Image is too small. Minimum allowed dimensions are 100 x 100 pixels."
    )


def test_upload_rejects_large_dimensions():
    large_image = np.zeros((6001, 100, 3), dtype=np.uint8)

    success, encoded_image = cv2.imencode(".jpg", large_image)

    assert success

    response = client.post(
        "/upload-image",
        files={
            "file": (
                "large_image.jpg",
                encoded_image.tobytes(),
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Image is too large. Maximum allowed dimensions are 6000 x 6000 pixels."
    )


def test_upload_rejects_oversized_file():
    oversized_content = b"x" * (10 * 1024 * 1024 + 1)

    response = client.post(
        "/upload-image",
        files={
            "file": (
                "oversized.jpg",
                oversized_content,
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Image file is too large. Maximum allowed file size is 10 MB."
    )
