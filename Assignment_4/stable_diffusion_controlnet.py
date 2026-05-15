# Assignment 4: Image Generation with Stable Diffusion & ControlNet
# Topic: Prompting & ControlNet using HuggingFace Diffusers on Colab A100

"""
This script implements a production-grade pipeline for generating images using 
Stable Diffusion and ControlNet. It is optimized for high-end GPUs like the NVIDIA A100.

Key Features:
1. Environment setup for HuggingFace Diffusers.
2. Loading Stable Diffusion v1.5 with ControlNet (Canny Edge).
3. Advanced prompting techniques (Multi-stage + Negative Prompting).
4. Automated image preprocessing for ControlNet.
5. Optimized inference using float16 and xformers (if available).
"""

import os
import torch
import cv2
import numpy as np
from PIL import Image
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from diffusers.utils import load_image

def setup_environment():
    """Installs required packages if running in a Colab environment."""
    print("Setting up environment...")
    # These would normally be run in a Colab cell
    # !pip install -q diffusers transformers accelerate opencv-python controlnet_aux
    pass

def get_canny_image(image_path_or_url):
    """
    Loads an image and extracts Canny edges for ControlNet conditioning.
    """
    image = load_image(image_path_or_url)
    image = np.array(image)

    # Convert to grayscale and find edges
    low_threshold = 100
    high_threshold = 200
    image = cv2.Canny(image, low_threshold, high_threshold)
    
    # ControlNet expects RGB conditioning images
    image = image[:, :, None]
    image = np.concatenate([image, image, image], axis=2)
    canny_image = Image.fromarray(image)
    
    return canny_image

def run_sd_controlnet_pipeline(
    prompt: str,
    negative_prompt: str,
    conditioning_image: Image.Image,
    model_id: str = "runwayml/stable-diffusion-v1-5",
    controlnet_id: str = "lllyasviel/sd-controlnet-canny",
    num_inference_steps: int = 30,
    guidance_scale: float = 7.5,
    controlnet_conditioning_scale: float = 1.0,
    num_images_per_prompt: int = 1
):
    """
    Initializes and runs the Stable Diffusion + ControlNet pipeline.
    Supports batch generation.
    """
    print(f"Loading models: {model_id} + {controlnet_id}...")
    
    # 1. Load ControlNet model
    controlnet = ControlNetModel.from_pretrained(
        controlnet_id, 
        torch_dtype=torch.float16
    )
    
    # 2. Load the main Pipeline
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        model_id, 
        controlnet=controlnet, 
        torch_dtype=torch.float16
    ).to("cuda")

    # 3. Optimize for A100 (Speed & Memory)
    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    
    # On A100, we can use xformers if available for even faster inference
    try:
        pipe.enable_xformers_memory_efficient_attention()
        print("xformers enabled.")
    except Exception:
        print("xformers not available, using standard attention.")

    print(f"Generating {num_images_per_prompt} image(s)...")
    # 4. Generate
    generator = torch.Generator(device="cuda").manual_seed(42)
    
    output = pipe(
        prompt=[prompt] * num_images_per_prompt,
        negative_prompt=[negative_prompt] * num_images_per_prompt,
        image=conditioning_image,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        controlnet_conditioning_scale=controlnet_conditioning_scale,
        generator=generator
    )

    return output.images

def get_depth_image(image_path_or_url):
    """
    Extracts a depth map from an image using a pre-trained estimator.
    Requires transformers and PIL.
    """
    from transformers import pipeline
    depth_estimator = pipeline("depth-estimation")
    image = load_image(image_path_or_url)
    depth_map = depth_estimator(image)['depth']
    
    # Convert depth map back to RGB format for ControlNet
    depth_map = np.array(depth_map)
    depth_map = depth_map[:, :, None]
    depth_map = np.concatenate([depth_map, depth_map, depth_map], axis=2)
    depth_image = Image.fromarray(depth_map)
    
    return depth_image

if __name__ == "__main__":
    # Example Usage for Assignment 4: Batch Generation with Canny ControlNet
    
    # Configuration
    PROMPT = "A cybernetic dragon made of liquid gold, obsidian scales, intricate circuitry, volumetric lighting, 8k"
    NEGATIVE_PROMPT = "blurry, lowres, ugly, deformed, text"
    NUM_SAMPLES = 2
    
    source_image_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/controlnet_training/canny_conditioning.png"
    
    try:
        # Pre-process Canny
        canny_cond = get_canny_image(source_image_url)
        canny_cond.save("canny_conditioning.png")
        
        # Run Pipeline
        if torch.cuda.is_available():
            results = run_sd_controlnet_pipeline(
                prompt=PROMPT,
                negative_prompt=NEGATIVE_PROMPT,
                conditioning_image=canny_cond,
                num_images_per_prompt=NUM_SAMPLES
            )
            
            for i, img in enumerate(results):
                img.save(f"generated_dragon_{i}.png")
            print(f"Successfully generated {len(results)} images.")
        else:
            print("CUDA not available. Demo only.")
            
    except Exception as e:
        print(f"Error: {e}")
