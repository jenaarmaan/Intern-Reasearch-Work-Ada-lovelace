# Deployment Guide: Luminary AI Platform

To make your Assignment 4 "Ready for the World," follow these deployment strategies.

## 1. Deploying to Hugging Face Spaces (GPU Enabled)
Hugging Face is the best place for this platform because it offers A100/T4 GPUs.

1.  Create a new **Space** on Hugging Face.
2.  Select **Docker** as the SDK.
3.  Upload the contents of `Assignment_4/platform/` to the Space repository.
4.  Hugging Face will automatically build the image using the provided `Dockerfile`.
5.  In the Space settings, choose a GPU tier (e.g., "T4 small" or "A100").

## 2. Professional Hybrid Deployment (Vercel + Cloud)
For a production-grade platform, split the frontend and backend.

### A. Frontend (Next.js) -> Vercel
1.  Connect your GitHub repository to **Vercel**.
2.  Set the root directory to `Assignment_4/platform/frontend`.
3.  Vercel will deploy the UI with global CDN support.

### B. Backend (FastAPI) -> AWS / GCP / RunPod
1.  Deploy the `backend` folder to a GPU-enabled instance.
2.  **RunPod** or **Lambda Labs** are great, low-cost alternatives for A100 access.
3.  Ensure the backend is accessible via a public IP or domain.

### C. Connection
Update the `fetch` URL in `frontend/src/app/page.tsx` from `http://localhost:8000` to your new backend URL.

## 3. Environment Variables
Add these to your deployment settings for security:
*   `NEXT_PUBLIC_API_URL`: Your backend address.
*   `HF_TOKEN`: (Optional) If using private Hugging Face models.
