from PIL import Image
from pathlib import Path


def predict_disease(image_path: Path):
    image = Image.open(image_path).convert("RGB")
    image = image.resize((64, 64))

    pixels = list(image.getdata())
    total_red = sum(pixel[0] for pixel in pixels)
    total_green = sum(pixel[1] for pixel in pixels)
    total_blue = sum(pixel[2] for pixel in pixels)

    avg_red = total_red / len(pixels)
    avg_green = total_green / len(pixels)
    avg_blue = total_blue / len(pixels)

    # Lightweight heuristic engine for MVP demo responses.
    if avg_green > avg_red and avg_green > avg_blue:
        disease = "Healthy Leaf"
        confidence = 91.5
        advice = "Crop looks healthy. Continue routine monitoring and irrigation."
    elif avg_red > avg_green and avg_red > avg_blue:
        disease = "Leaf Blight"
        confidence = 88.4
        advice = "Remove infected leaves and apply a copper-based fungicide."
    else:
        disease = "Leaf Spot"
        confidence = 84.7
        advice = "Prune affected leaves, improve airflow, and apply neem-based treatment."

    return {
        "disease": disease,
        "confidence": round(confidence, 1),
        "advice": advice,
    }
