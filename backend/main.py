
import cv2
import numpy as np

from fastapi import FastAPI, UploadFile, File, HTTPException
from src.features.computer_vision import analyze_advertisement

app = FastAPI(
    title="Creative Intelligence AI",
    description="AI-Powered Advertisement Analysis and Design Intelligence Platform",
    version="1.0.0"
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@app.get("/")
def home():
    return {
        "message": "Welcome to Creative Intelligence AI!",
        "status": "Backend is running successfully",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Creative Intelligence AI",
        "message": "All systems operational"
    }


@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):

    allowed_types = ["image/jpeg", "image/png", "image/webp"]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG and WEBP images are allowed."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty."
        )

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Image file is too large. Maximum allowed file size is 10 MB."
        )

    image_array = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted image file."
        )

    height, width = image.shape[:2]

    if width < 100 or height < 100:
        raise HTTPException(
            status_code=400,
            detail="Image is too small. Minimum allowed dimensions are 100 x 100 pixels."
        )

    if width > 6000 or height > 6000:
        raise HTTPException(
            status_code=400,
            detail="Image is too large. Maximum allowed dimensions are 6000 x 6000 pixels."
        )

    try:
        analysis_results = analyze_advertisement(image)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Image analysis failed: {str(error)}"
        )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(contents),
        "image_width": width,
        "image_height": height,
        "validation": "Image is valid",
        "analysis": analysis_results,
        "message": "Image uploaded and analyzed successfully!"
    }


print("Creative Intelligence AI Backend Initialized!")
