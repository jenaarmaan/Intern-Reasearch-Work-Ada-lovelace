# Assignment 4: Stable Diffusion & ControlNet

## Overview
This project demonstrates the implementation of a controlled image generation pipeline using **Stable Diffusion** and **ControlNet** via the HuggingFace `diffusers` library. It is specifically optimized for high-performance compute environments like **Google Colab A100**.

## Project Structure
*   `stable_diffusion_controlnet.ipynb`: The main notebook for interactive execution in Colab.
*   `stable_diffusion_controlnet.py`: Python script version of the pipeline.
*   `prompting_guide.md`: A comprehensive guide on how to write effective prompts for SD.
*   `requirements.txt`: List of necessary Python packages.
*   `implementation_plan.md`: The roadmap followed for this assignment.

## Key Concepts
1.  **Stable Diffusion**: A latent diffusion model for text-to-image generation.
2.  **ControlNet**: A neural network structure to control diffusion models by adding extra conditions (like Canny edges, depth maps, or human poses).
3.  **Prompt Engineering**: The art of refining text inputs to guide the AI towards specific artistic or technical outputs.

## Setup Instructions
1.  Upload `stable_diffusion_controlnet.ipynb` to Google Colab.
2.  Change the runtime type to **GPU** (Select **A100** if available).
3.  Run the cells sequentially.

## Troubleshooting
*   **CUDA Error**: Ensure the runtime has a GPU allocated.
*   **Memory Issues**: The A100 has 40GB+ of VRAM, which is plenty for SD v1.5 and SDXL. If using a smaller GPU, keep `pipe.enable_model_cpu_offload()` active.
