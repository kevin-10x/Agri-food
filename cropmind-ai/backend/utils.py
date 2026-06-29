import numpy as np
import tensorflow as tf
from PIL import Image
from pathlib import Path

# Use the official legacy Keras wrapper to safely load Keras 2 models in TF 2.16+
try:
    import tf_keras as keras
except ImportError:
    import tensorflow.keras as keras

# Automatically resolves the path to the model file inside the backend folder
MODEL_PATH = Path(__file__).parent / "cropmind_model.h5"

# Load using the legacy engine to avoid positional argument crashes
MODEL = keras.models.load_model(str(MODEL_PATH), compile=False)

# PlantVillage class labels in the exact alphabetical order they were trained
CLASS_NAMES = [
    "Apple_Black_rot", "Apple_Cedar_apple_rust", "Apple_healthy", "Apple_scab",
    "Cherry_healthy", "Cherry_Powdery_mildew",
    "Corn_Cercospora_leaf_spot_Gray_leaf_spot", "Corn_Common_rust", "Corn_healthy", "Corn_Northern_Leaf_Blight",
    "Grape_Black_rot", "Grape_Esca_Black_Measles", "Grape_healthy", "Grape_Leaf_blight_Isariopsis_Leaf_Spot",
    "Peach_Bacterial_spot", "Peach_healthy",
    "Potato_Early_blight", "Potato_healthy", "Potato_Late_blight",
    "Strawberry_healthy", "Strawberry_Leaf_scorch",
    "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_healthy", "Tomato_Late_blight",
    "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot", "Tomato_Spider_mites_Two-spotted_spider_mite",
    "Tomato_Target_Spot", "Tomato_Tomato_mosaic_virus", "Tomato_Tomato_Yellow_Leaf_Curl_Virus"
]

ADVICE_DATABASE = {
    "Apple_Black_rot": "Remove and destroy infected plant parts. Apply protective fungicides containing captan or mancozeb.",
    "Apple_Cedar_apple_rust": "Remove nearby cedar trees if possible or plant resistant varieties. Apply fungicides containing myclobutanil.",
    "Apple_healthy": "Maintain good orchard hygiene, proper pruning, and balanced fertilization.",
    "Apple_scab": "Prune trees to improve air circulation. Apply preventative fungicides such as dodine or chlorothalonil early in the season.",
    "Cherry_healthy": "Continue regular watering and appropriate pruning to maintain canopy health.",
    "Cherry_Powdery_mildew": "Apply sulfur-based fungicides or horticultural oils. Avoid overhead irrigation to reduce humidity.",
    "Corn_Cercospora_leaf_spot_Gray_leaf_spot": "Use resistant crop hybrids. Consider applying fungicides like strobilurins if spots appear early.",
    "Corn_Common_rust": "Plant rust-resistant corn varieties. Fungicides like azoxystrobin can be used if infection becomes severe.",
    "Corn_healthy": "Ensure proper plant spacing and optimal nitrogen nutrient management.",
    "Corn_Northern_Leaf_Blight": "Practice crop rotation. Utilize resistant hybrids and apply preventative fungicides if necessary.",
    "Grape_Black_rot": "Prune out diseased canes during dormancy. Apply protective fungicides like mancozeb at critical early growth stages.",
    "Grape_Esca_Black_Measles": "No direct chemical cure available; focus on minimizing vine stress and practicing good vineyard sanitation.",
    "Grape_healthy": "Provide adequate trellis support and maintain a regular canopy pruning schedule.",
    "Grape_Leaf_blight_Isariopsis_Leaf_Spot": "Maintain good air circulation through leaf thinning. Copper-based sprays can help manage spread.",
    "Peach_Bacterial_spot": "Avoid excessive nitrogen fertilization. Apply protective copper sprays during dormancy and early blossom phases.",
    "Peach_healthy": "Continue routine strategic pruning, balanced fertilization, and localized pest management.",
    "Potato_Early_blight": "Maintain adequate plant vigor with proper fertilization. Apply protective fungicides containing chlorothalonil.",
    "Potato_healthy": "Continue standard crop rotation cycles, proper soil management, and uniform irrigation tracking.",
    "Potato_Late_blight": "High danger! Apply systemic fungicides immediately. Ensure field drainage is optimized to reduce ambient soil moisture.",
    "Strawberry_healthy": "Continue regular drip irrigation, proper weed management, and routine health scanning.",
    "Strawberry_Leaf_scorch": "Remove heavily infected leaves. Avoid overhead watering. Apply protective fungicides during severe outbreaks.",
    "Tomato_Bacterial_spot": "Eliminate infected crop residues. Apply copper-based bactericides mixed with mancozeb for optimal protection.",
    "Tomato_Early_blight": "Prune lower leaves to avoid soil-splash inoculations. Apply fungicides containing chlorothalonil or copper.",
    "Tomato_healthy": "Crop conditions are optimal. Continue routine monitoring, balanced watering, and staking support.",
    "Tomato_Late_blight": "High risk environment. Apply targeted systemic fungicides immediately and destroy heavily infected plants.",
    "Tomato_Leaf_Mold": "Improve greenhouse ventilation and lower relative humidity levels. Apply preventative chlorothalonil sprays.",
    "Tomato_Septoria_leaf_spot": "Avoid working in wet patches. Remove infected lower leaves and apply copper-based organic sprays.",
    "Tomato_Spider_mites_Two-spotted_spider_mite": "Release natural predatory mites. Treat hotspot areas using targeted horticultural oils or insecticidal soaps.",
    "Tomato_Target_Spot": "Maintain good field sanitation. Apply protective fungicides containing azoxystrobin or chlorothalonil.",
    "Tomato_Tomato_mosaic_virus": "Remove and burn infected plants immediately. Disinfect tools frequently and manage weed hosts.",
    "Tomato_Tomato_Yellow_Leaf_Curl_Virus": "Strictly control whitefly populations using reflective mulches, row covers, or appropriate narrow-spectrum insecticides."
}

def predict_disease(image_path: Path) -> dict:
    try:
        # 1. Open and resize the image to match MobileNet's expected dimensions (224x224)
        image = Image.open(image_path).convert("RGB").resize((224, 224))
        
        # 2. Normalize pixel arrays to [0, 1] as expected by the model
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # 3. Run true deep learning inference
        predictions = MODEL.predict(img_array)
        highest_idx = np.argmax(predictions[0])
        
        predicted_class = CLASS_NAMES[highest_idx]
        confidence_score = float(predictions[0][highest_idx]) * 100
        
        return {
            "disease": predicted_class.replace("_", " "),
            "confidence": round(confidence_score, 1),
            "advice": ADVICE_DATABASE.get(predicted_class, "Review standard agricultural extension guidelines.")
        }
    except Exception as e:
        return {
            "disease": "Analysis Error",
            "confidence": 0.0,
            "advice": f"Model inference failed: {str(e)}"
        }
