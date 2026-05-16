import streamlit as st
import torch
import numpy as np
from PIL import Image
import cv2
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from transformers import pipeline as tf_pipeline
import io

# --- Page Config ---
st.set_page_config(page_title="Luminary AI", page_icon="🌟", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .css-1d391kg {
        background-color: #1e293b;
    }
    h1, h2, h3 {
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌟 Luminary AI")
st.markdown("### Next-Generation ControlNet Platform")
st.write("Unleash structural creativity with Stable Diffusion and ControlNet.")

# --- Lazy Model Loading ---
@st.cache_resource(show_spinner=False)
def load_models(control_type):
    controlnet_id = "lllyasviel/sd-controlnet-canny" if control_type == "canny" else "lllyasviel/sd-controlnet-depth"
    controlnet = ControlNetModel.from_pretrained(controlnet_id, torch_dtype=torch.float16)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", 
        controlnet=controlnet, 
        torch_dtype=torch.float16
    ).to("cuda")
    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.enable_xformers_memory_efficient_attention()
    return pipe

# --- UI Layout ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.header("Configuration")
    prompt = st.text_area("Primary Prompt", "A highly detailed masterpiece...")
    negative_prompt = st.text_input("Negative Prompt", "low quality, bad anatomy, worst quality")
    
    c1, c2 = st.columns(2)
    with c1:
        control_type = st.selectbox("Control Mode", ["canny", "depth"], format_func=lambda x: "Canny Edge" if x == "canny" else "Depth Map")
    with c2:
        num_samples = st.number_input("Samples", min_value=1, max_value=4, value=1)
        
    uploaded_file = st.file_uploader("Upload Source Image", type=["png", "jpg", "jpeg"])
    
    generate_btn = st.button("Generate Masterpiece", use_container_width=True, type="primary")

with col2:
    st.header("Results")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Source Image", use_column_width=True)
        
    if generate_btn:
        if not uploaded_file:
            st.error("Please upload a source image first.")
        elif not torch.cuda.is_available():
            st.error("CUDA GPU is required but not available on this system.")
        else:
            with st.spinner("Processing Latent Space..."):
                # Process image
                image_bytes = uploaded_file.getvalue()
                input_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                img_np = np.array(input_img)
                
                # Conditioning
                if control_type == "canny":
                    processed = cv2.Canny(img_np, 100, 200)
                    processed = processed[:, :, None]
                    processed = np.concatenate([processed, processed, processed], axis=2)
                else:
                    depth_estimator = tf_pipeline("depth-estimation")
                    processed = depth_estimator(input_img)['depth']
                    processed = np.array(processed)
                    processed = processed[:, :, None]
                    processed = np.concatenate([processed, processed, processed], axis=2)
                
                conditioning_image = Image.fromarray(processed)
                
                st.image(conditioning_image, caption="Conditioning Guide", use_column_width=True, clamp=True)
                
                # Generate
                pipe = load_models(control_type)
                generator = torch.Generator(device="cuda").manual_seed(42)
                
                results = pipe(
                    prompt=[prompt] * num_samples,
                    negative_prompt=[negative_prompt] * num_samples,
                    image=conditioning_image,
                    num_inference_steps=30,
                    generator=generator
                ).images
                
                st.success("Synthesis Complete!")
                cols = st.columns(len(results))
                for idx, res in enumerate(results):
                    cols[idx].image(res, caption=f"Result {idx+1}", use_column_width=True)
