# ==========================================
# STAGE 1: Build the Expo Web Frontend
# ==========================================
# Upgraded from node:18 to node:20 to meet Expo's modern requirements
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

# Copy frontend dependency files
COPY package*.json ./
RUN npm ci

# Copy frontend source code
COPY . .

# FIX: Swapped deprecated export:web command with modern expo export command
RUN npx expo export --platform web

# ==========================================
# STAGE 2: Final Production Environment
# ==========================================
FROM python:3.10-slim AS final
WORKDIR /app

# Install Node.js runtime environment dependencies (needed to host static assets cleanly)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the Python FastAPI source code
COPY backend/ ./backend

# FIX: Modern Expo saves the output into a 'dist' directory instead of 'web-build'
COPY --from=frontend-builder /app/frontend/dist ./public

# Expose the API and Web server port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Launch the FastAPI app with Uvicorn
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
