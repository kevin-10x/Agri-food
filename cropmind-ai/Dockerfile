# ==========================================
# STAGE 1: Build the Expo Web Frontend
# ==========================================
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend

# Copy frontend dependency files
COPY package*.json ./
RUN npm ci

# Copy frontend source code
COPY . .

# Build the static web files (generates a web-build folder)
RUN npx expo export:web

# ==========================================
# STAGE 2: Final Production Environment
# ==========================================
FROM python:3.10-slim AS final
WORKDIR /app

# Install Node.js runtime environment dependencies (needed to host static assets cleanly or minimal tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the Python FastAPI source code
COPY backend/ ./backend

# Copy the compiled static frontend files from Stage 1 into a public folder
COPY --from=frontend-builder /app/frontend/web-build ./public

# Expose the API and Web server port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Launch the FastAPI app with Uvicorn
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
