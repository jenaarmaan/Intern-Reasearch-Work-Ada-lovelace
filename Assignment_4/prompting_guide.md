# Prompting Guide for Assignment 4

To get the best results from Stable Diffusion v1.5 or SDXL, follow this structured prompting strategy.

## 1. The Prompt Anatomy
A professional prompt usually follows this order:
`[Subject] + [Action/Pose] + [Setting/Background] + [Artistic Style] + [Artist Reference] + [Technical Quality]`

### Example
> "A majestic white owl flying through a crystal cave, mystical atmosphere, oil painting, studio lighting, detailed feathers, 8k resolution, trending on ArtStation"

## 2. Weighting and Emphasis
*   **Emphasis**: Use parentheses to increase weight `(keyword:1.2)` or brackets to decrease `[keyword:0.8]`.
*   **Order Matters**: Keywords at the beginning of the prompt have more influence than those at the end.

## 3. ControlNet Conditioning
When using ControlNet, the prompt should describe what is *happening* in the structure provided by the control image.
*   If the ControlNet is **Canny (Edges)** of a building, your prompt should focus on the *texture* and *style* of that building (e.g., "Medieval castle made of volcanic rock").

## 4. Negative Prompting
Negative prompts are essential to remove unwanted artifacts. Always include:
> "monochrome, lowres, bad anatomy, worst quality, low quality, blurry, distorted, text, watermark, signature, extra fingers, malformed limbs"

## 5. Advanced ControlNet Techniques
*   **Conditioning Scale**: The `controlnet_conditioning_scale` parameter (default 1.0) determines how much the structure influences the generation. 
    *   Set it to **0.5-0.7** for a "loose" interpretation (good for artistic styles).
    *   Set it to **1.0-1.2** for strict adherence (good for architectural or technical work).
*   **Multi-ControlNet**: You can stack multiple ControlNets (e.g., Canny for edges + Depth for volume). The A100 has enough memory to handle 2-3 ControlNets simultaneously.

## 6. Pro Tips for A100 Users
*   **Step Count**: On an A100, you can easily go up to 50-70 steps for ultra-fine detail without long wait times.
*   **Guidance Scale (CFG)**: Keep it between 7.0 and 9.0. Higher values (12+) make the image more saturated and "fried".
*   **Batching**: Use `num_images_per_prompt` to generate 4-8 images at once. The A100's parallelism makes this almost as fast as generating one.
*   **High-Res Fix**: Generate at 512x512 first, then use an upscaler for the best quality/speed trade-off.
