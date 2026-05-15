# Multi-stage build for a high-performance AI Platform

# --- Stage 1: Build Frontend ---
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# --- Stage 2: Final Image ---
FROM python:3.10-slim
WORKDIR /app

# Install system dependencies for OpenCV and AI
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from Stage 1
COPY --from=frontend-builder /app/frontend/.next ./.next
COPY --from=frontend-builder /app/frontend/public ./public
COPY --from=frontend-builder /app/frontend/package*.json ./

# Install only production node modules if needed for serving
# Alternatively, we can use a dedicated Node server, but often Next.js 'standalone' is better.
# For simplicity in this assignment, we'll assume a dual-process launch.

# Setup launch script
COPY launch.py ./

EXPOSE 8000 3000

CMD ["python", "launch.py"]
