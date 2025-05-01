# image_validator/core.py
import cv2
from .face_detection import check_face_detection
from .image_quality_check import is_fake_image
from .text_extraction import extract_text_from_image

def analyze_image(image_path):
    result = {
        "path": image_path,
        "fake": False,
        "reasons": []
    }

    img = cv2.imread(image_path)
    # if img is None:
    #     result["fake"] = True
    #     result["reasons"].append("Unreadable image")
    #     return result

    if extract_text_from_image(image_path):
        result["fake"] = True
        result["reasons"].append("Text detected on image")

    if not check_face_detection(image_path):
        result["fake"] = True
        result["reasons"].append("No face detected")

    quality_check = is_fake_image(image_path)
    if quality_check:
        result["fake"] = True
        result["reasons"].append("image quality is bad")

    return result
