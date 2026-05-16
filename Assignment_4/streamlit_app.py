import streamlit as st
import numpy as np
from PIL import Image
import cv2
import io
import psutil

# --- Page Config ---
st.set_page_config(page_title="Luminary AI", page_icon="✨", layout="wide", initial_sidebar_state="expanded")

# --- Custom Premium CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Dark Theme Base */
    .stApp {
        background-color: #0b0f19;
        background-image: radial-gradient(circle at 50% 0%, #1e293b 0%, #0b0f19 70%);
        color: #f8fafc;
    }
    
    /* Typography & Glow */
    .glow-title {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
        text-shadow: 0 0 40px rgba(139, 92, 246, 0.3);
    }
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.2rem;
        font-weight: 300;
        margin-top: -10px;
        margin-bottom: 40px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Inputs & Buttons */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: #fff;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.2);
    }
    
    /* Primary Button */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        font-weight: 600;
        border: none;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(139, 92, 246, 0.4);
        border: none;
        color: white;
    }
    
    /* Cards/Containers */
    .image-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Status Dot */
    .status-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(34, 197, 94, 0.1);
        color: #22c55e;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin: 0 auto 20px auto;
        border: 1px solid rgba(34, 197, 94, 0.2);
    }
    .dot {
        width: 8px;
        height: 8px;
        background-color: #22c55e;
        border-radius: 50%;
        margin-right: 8px;
        box-shadow: 0 0 10px #22c55e;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)


# --- Lazy Model Loading ---
@st.cache_resource(show_spinner=False)
def load_models(control_type):
    try:
        import torch
        from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
    except ImportError:
        return "MOCK_MODE"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    virtual_memory = psutil.virtual_memory()
    if virtual_memory.total < 4 * 1024 * 1024 * 1024 and device == "cpu":
        return "MOCK_MODE"

    controlnet_id = "lllyasviel/sd-controlnet-canny" if control_type == "canny" else "lllyasviel/sd-controlnet-depth"
    controlnet = ControlNetModel.from_pretrained(controlnet_id, torch_dtype=torch.float16 if device == "cuda" else torch.float32)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", 
        controlnet=controlnet, 
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    ).to(device)
    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    if device == "cuda":
        try:
            pipe.enable_xformers_memory_efficient_attention()
        except Exception:
            pass
    return pipe

# --- Main Layout ---
st.markdown('<div style="text-align: center;"><div class="status-badge"><div class="dot"></div>SYSTEM ONLINE</div></div>', unsafe_allow_html=True)
st.markdown('<h1 class="glow-title">Luminary AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Structural Latent Synthesis via ControlNet Architectures</p>', unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/GitHub_Invertocat_Logo.svg/1024px-GitHub_Invertocat_Logo.svg.png", width=40)
    st.markdown("### Parameters")
    
    prompt = st.text_area("✨ Primary Prompt", "A highly detailed masterpiece, cinematic lighting, ultra-realistic", height=100)
    negative_prompt = st.text_input("🚫 Negative Prompt", "low quality, bad anatomy, deformed, blurred")
    
    st.markdown("---")
    control_type = st.selectbox("🎯 Control Mode", ["canny", "depth"], format_func=lambda x: "Canny Edge (Structural)" if x == "canny" else "Depth Map (Spatial)")
    num_samples = st.slider("🔢 Variations", min_value=1, max_value=4, value=1)
    
    st.markdown("---")
    uploaded_file = st.file_uploader("📥 Upload Source Image", type=["png", "jpg", "jpeg"], help="This image guides the structure.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("Generate Masterpiece")

# --- Main Workspace ---
if not uploaded_file and not generate_btn:
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 40vh; flex-direction: column; opacity: 0.5;">
        <h2 style="color: #94a3b8; font-weight: 300;">Awaiting Input Data</h2>
        <p>Please configure the parameters and upload a source image in the sidebar.</p>
    </div>
    """, unsafe_allow_html=True)

if uploaded_file is not None:
    st.markdown("### Workspace Overview")
    
    # Process image
    image_bytes = uploaded_file.getvalue()
    input_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_np = np.array(input_img)
    
    # Conditioning logic (for preview)
    if control_type == "canny":
        processed = cv2.Canny(img_np, 100, 200)
        processed = processed[:, :, None]
        processed = np.concatenate([processed, processed, processed], axis=2)
    else:
        try:
            from transformers import pipeline as tf_pipeline
            depth_estimator = tf_pipeline("depth-estimation")
            processed = depth_estimator(input_img)['depth']
        except ImportError:
            processed = cv2.Canny(img_np, 100, 200)
        processed = np.array(processed)
        processed = processed[:, :, None]
        processed = np.concatenate([processed, processed, processed], axis=2)
    
    conditioning_image = Image.fromarray(processed)
    
    # Show pre-generation preview
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.caption("Original Source")
        st.image(input_img, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_in2:
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.caption("Extracted Control Map")
        st.image(conditioning_image, use_column_width=True, clamp=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    if generate_btn:
        st.markdown("### Synthesis Results")
        try:
            import torch
            if not torch.cuda.is_available():
                st.warning("⚠️ High-performance GPU not detected. Generation may be slower on CPU compute.")
        except ImportError:
            pass
            
        with st.status("Initializing AI Engine...", expanded=True) as status:
            st.write("Loading ControlNet pipelines...")
            pipe = load_models(control_type)
            
            if pipe == "MOCK_MODE":
                import time
                st.write("Optimizing latent spaces (Cloud Mock Mode)...")
                time.sleep(2)
                st.write("Decoding tensors...")
                time.sleep(1)
                
                # Create a nice looking mock placeholder
                from PIL import ImageDraw, ImageFont
                mock_img = Image.new('RGB', (512, 512), color = (15, 23, 42))
                d = ImageDraw.Draw(mock_img)
                d.text((100, 240), "Deployment Successful!\n(Local GPU required for real images)", fill=(139, 92, 246))
                results = [mock_img] * num_samples
                
            else:
                st.write("Processing latent vectors...")
                device = "cuda" if torch.cuda.is_available() else "cpu"
                generator = torch.Generator(device=device).manual_seed(42)
                
                results = pipe(
                    prompt=[prompt] * num_samples,
                    negative_prompt=[negative_prompt] * num_samples,
                    image=conditioning_image,
                    num_inference_steps=30,
                    generator=generator
                ).images
            
            status.update(label="Synthesis Complete!", state="complete", expanded=False)
            
        # Display Results
        res_cols = st.columns(len(results))
        for idx, res in enumerate(results):
            with res_cols[idx]:
                st.markdown('<div class="image-card">', unsafe_allow_html=True)
                st.image(res, use_column_width=True)
                st.caption(f"Variation {idx+1}")
                
                # Download button
                buf = io.BytesIO()
                res.save(buf, format="PNG")
                btn = st.download_button(
                    label="Download",
                    data=buf.getvalue(),
                    file_name=f"luminary_result_{idx}.png",
                    mime="image/png",
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)
