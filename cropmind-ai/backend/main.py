from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil

from backend.utils import predict_disease

app = FastAPI(title="CropMind AI Backend")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "CropMind AI backend is running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file")

    destination = UPLOAD_DIR / file.filename

    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = predict_disease(destination)
        return result
    finally:
        if destination.exists():
            destination.unlink()
