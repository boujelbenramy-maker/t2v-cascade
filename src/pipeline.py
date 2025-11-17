"""
Text-to-Video cascade commun Colab / Modal / local
720p → 4K 60 fps
"""
import os, torch, cv2, imageio, tempfile, subprocess
from diffusers import CogVideoXImageToVideoPipeline, DPMSolverMultistepScheduler
from controlnet_aux import MidasDetector
from realesrgan import RealESRGAN
from rife_torch import interpolate

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype  = torch.float16 if device=="cuda" else torch.float32

pipe      = CogVideoXImageToVideoPipeline.from_pretrained(
                "THUDM/CogVideoX-5b-I2V", torch_dtype=dtype).to(device)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
depth_detector = MidasDetector.from_pretrained("lllyasviel/Annotators")
upscaler       = RealESRGAN(device, scale=4) if device=="cuda" else None

def generate_cascade(prompt, image_path, duration_s=8, camera="static", target_fps=60):
    b, f = 1, 64*duration_s//8                     # 64 frames pour 8 s
    image = cv2.imread(image_path)
    depth_map = depth_detector(image)

    # camera motion
    if camera == "pan_left":
        depth_map = np.roll(depth_map, -30, axis=1)
    elif camera == "zoom_in":
        h, w = depth_map.shape[:2]
        depth_map = cv2.resize(depth_map, None, fx=1.15, fy=1.15)[30:-30, 30:-30]

    # 1) DiT denoise
    latents = pipe(
        prompt=prompt,
        image=image,
        control_image=depth_map,
        num_frames=f,
        height=256, width=256,
        num_inference_steps=20,
        guidance_scale=7.5,
        generator=torch.Generator(device).manual_seed(42)
    ).latents

    # 2) 4K decode
    video_4k = vae4k.decode(latents, target_fps=target_fps, output_size=(2160, 3840)) if upscaler else latents
    return video_4k
