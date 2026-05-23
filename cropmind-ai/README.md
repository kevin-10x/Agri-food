# 🌿 CropMind AI

CropMind AI is a mobile-first agriculture prototype that lets farmers take or upload a crop image, send it to a local backend API, and receive a disease prediction plus treatment advice.

## Features

- Image picker for crop photos
- Mock-free local backend API
- Disease prediction response
- Treatment recommendations
- Expo web build verification

## Project structure

- `App.js` — Expo React Native UI
- `backend/main.py` — FastAPI prediction endpoint
- `backend/utils.py` — lightweight MVP disease heuristic
- `backend/requirements.txt` — Python dependencies
- `.env.example` — API base URL configuration

## Setup

### 1. Install frontend dependencies

```bash
cd cropmind-ai
npm install
```

### 2. Install backend dependencies

```bash
cd cropmind-ai
python -m pip install -r backend/requirements.txt
```

### 3. Start the backend

```bash
cd cropmind-ai
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 4. Start the Expo app

```bash
cd cropmind-ai
npx expo start
```

### 5. Configure the API URL

For local testing, the app uses `http://localhost:8000` by default.

If you need to override it, copy `.env.example` to `.env` and change `EXPO_PUBLIC_API_BASE_URL`.

## Example API response

```json
{
  "disease": "Healthy Leaf",
  "confidence": 91.5,
  "advice": "Crop looks healthy. Continue routine monitoring and irrigation."
}
```

## Next steps

- Replace the MVP heuristic engine with a TensorFlow CNN model
- Add authentication and farmer dashboard
- Add MPESA payments and marketplace features
