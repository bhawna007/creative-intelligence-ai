
import cv2
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

"""
Computer Vision Module
----------------------
Analyzes advertisement images using:
1. Visual design scoring
2. Colour diversity analysis
3. Saliency detection
4. Combined design intelligence metrics
"""

def calculate_design_score(image):
    """Calculate heuristic brightness, contrast and resolution scores."""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height, width = image.shape[:2]

    brightness = np.mean(gray)
    contrast = np.std(gray)
    resolution = width * height

    brightness_score = max(
        0, 100 - abs(brightness - 140) * 0.7
    )

    contrast_score = min(100, contrast * 1.5)

    resolution_score = min(
        100, (resolution / (1080 * 1920)) * 100
    )

    final_score = (
        brightness_score * 0.35
        + contrast_score * 0.35
        + resolution_score * 0.30
    )

    return {
        "Brightness Score": float(round(brightness_score, 2)),
        "Contrast Score": float(round(contrast_score, 2)),
        "Resolution Score": float(round(resolution_score, 2)),
        "Design Score": float(round(final_score, 2))
    }


def calculate_color_diversity(image):
    """Calculate normalized Shannon colour diversity."""

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (150, 150))

    pixels = resized.reshape(-1, 3)

    kmeans = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(pixels)

    counts = np.bincount(labels)
    percentages = counts / len(labels) * 100
    probabilities = percentages / 100

    entropy = -np.sum(
        probabilities * np.log2(probabilities + 1e-10)
    )

    diversity_score = (entropy / np.log2(5)) * 100

    return round(diversity_score, 2)


def calculate_saliency(image):
    """Calculate image-based computational saliency statistics."""

    detector = cv2.saliency.StaticSaliencySpectralResidual_create()

    success, saliency_map = detector.computeSaliency(image)

    if not success:
        raise RuntimeError("Saliency detection failed.")

    return {
    "Average Saliency Score": float(round(float(np.mean(saliency_map) * 100), 2)),
    "Maximum Saliency": float(round(float(np.max(saliency_map)), 4)),
    "Minimum Saliency": float(round(float(np.min(saliency_map)), 4))
    }


def analyze_advertisement(image):
    """Generate a consolidated heuristic and saliency report."""
    if image is None:
        raise ValueError("Invalid image. Please provide a valid advertisement image.")

    results = calculate_design_score(image)

    diversity = calculate_color_diversity(image)
    results["Colour Diversity Score"] = float(diversity)

    updated_score = (
        results["Brightness Score"] * 0.25
        + results["Contrast Score"] * 0.25
        + results["Resolution Score"] * 0.25
        + diversity * 0.25
    )

    results["Updated Design Score"] = float(round(float(updated_score), 2))

    results.update(calculate_saliency(image))

    return results

def analyze_multiple_ads(images):
    """
    Performs batch analysis of multiple advertisement images.

    Args:
        images (dict): Dictionary containing category names
                       and corresponding OpenCV images.

    Returns:
        pd.DataFrame: Structured analysis report containing
                      design scores, colour diversity,
                      and saliency metrics for each image.

    Raises:
        ValueError: If no images are provided or an image is invalid.
    """

    # Step 1: Validate input
    if not isinstance(images, dict):
        raise TypeError("Input must be a dictionary of advertisement images.")

    if not images:
        raise ValueError("No advertisement images provided.")

    # Step 2: Initialize results list
    results = []

    # Step 3: Analyze each advertisement
    for category, image in images.items():

        # Validate individual image
        if image is None:
            raise ValueError(
                f"Invalid image in category: {category}"
            )

        # Perform computer vision analysis
        analysis = analyze_advertisement(image)

        # Add advertisement category
        analysis["Category"] = category

        # Store analysis results
        results.append(analysis)

    # Step 4: Convert results into DataFrame
    report = pd.DataFrame(results)

    # Step 5: Return final report
    return report