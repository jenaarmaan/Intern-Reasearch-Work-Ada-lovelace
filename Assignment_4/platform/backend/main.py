from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sys
import os
import uuid
import numpy as np
from PIL import Image
import io

# Debug: Print environment info
print(f"Python: {sys.executable}")
print(f"Path: {sys.path}")

try:
    import cv2
    print(f"OpenCV version: {cv2.__version__}")
except ImportError as e:
    print(f"🚨 CRITICAL ERROR: Could not import cv2. Error: {e}")
    # Force add user site packages just in case
    import site
    user_site = site.getusersitepackages()
    if user_site not in sys.path:
        sys.path.append(user_site)
        print(f"Added user site: {user_site}")
    try:
        import cv2
        print("Successfully imported cv2 after manual path injection.")
    except ImportError:
        print("Manual path injection failed.")

try:
    import torch
    from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
    from diffusers.utils import load_image
except ImportError as e:
    print(f"🚨 CRITICAL ERROR: Could not import AI libraries. Error: {e}")

app = FastAPI()

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage for generated images
UPLOAD_DIR = "static/uploads"
OUTPUT_DIR = "static/outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mount static folders for AI outputs
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount frontend (built with 'npm run build' / output: 'export')
# Ensure the 'frontend/out' directory exists
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "../frontend/out")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    print(f"Warning: Frontend directory {FRONTEND_DIR} not found. UI will not be served.")

# Global variables for models (lazy loading)
pipe = None
current_control_type = None

def load_models(control_type="canny"):
    global pipe, current_control_type
    if pipe is not None and current_control_type == control_type:
        return
    
    print(f"Loading models for {control_type}...")
    controlnet_id = "lllyasviel/sd-controlnet-canny" if control_type == "canny" else "lllyasviel/sd-controlnet-depth"
    
    controlnet = ControlNetModel.from_pretrained(controlnet_id, torch_dtype=torch.float16)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", 
        controlnet=controlnet, 
        torch_dtype=torch.float16
    ).to("cuda")
    
    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.enable_xformers_memory_efficient_attention()
    current_control_type = control_type

@app.get("/")
def read_root():
    return {"status": "AI Engine Online", "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None"}

@app.post("/generate")
async def generate(
    prompt: str = Form(...),
    negative_prompt: str = Form(""),
    control_type: str = Form("canny"),
    num_samples: int = Form(1),
    image: UploadFile = File(...)
):
    if not torch.cuda.is_available():
        raise HTTPException(status_code=500, detail="CUDA GPU not available on this server")

    # 1. Save and process uploaded image
    contents = await image.read()
    input_img = Image.open(io.BytesIO(contents)).convert("RGB")
    input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.png")
    input_img.save(input_path)

    # 2. Preprocess for ControlNet
    img_np = np.array(input_img)
    if control_type == "canny":
        processed = cv2.Canny(img_np, 100, 200)
        processed = processed[:, :, None]
        processed = np.concatenate([processed, processed, processed], axis=2)
    else:
        # Simple depth estimation (fallback or use transformers)
        from transformers import pipeline as tf_pipeline
        depth_estimator = tf_pipeline("depth-estimation")
        processed = depth_estimator(input_img)['depth']
        processed = np.array(processed)
        processed = processed[:, :, None]
        processed = np.concatenate([processed, processed, processed], axis=2)
    
    conditioning_image = Image.fromarray(processed)

    # 3. Load/Switch Models if needed
    load_models(control_type)

    # 4. Generate
    generator = torch.Generator(device="cuda").manual_seed(42)
    results = pipe(
        prompt=[prompt] * num_samples,
        negative_prompt=[negative_prompt] * num_samples,
        image=conditioning_image,
        num_inference_steps=30,
        generator=generator
    ).images

    # 5. Save results
    output_urls = []
    for i, res in enumerate(results):
        filename = f"{uuid.uuid4()}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        res.save(filepath)
        output_urls.append(f"/static/outputs/{filename}")

    return {
        "success": True,
        "outputs": output_urls,
        "conditioning": f"/static/uploads/{os.path.basename(input_path)}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
