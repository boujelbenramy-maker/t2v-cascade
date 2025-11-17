"""
Modal serveur GPU
Text-to-Video cascade 4K 60 fps
"""
import modal
import os, tempfile, subprocess
from pathlib import Path

stub = modal.Stub("t2v-cascade")
image = (
    modal.Image.debian_slim()
    .apt_install("git", "wget", "ffmpeg", "libgl1-mesa-glx")
    .pip_install(
        "torch==2.3.1+cu121", "torchvision", "torchaudio",
        "--index-url", "https://download.pytorch.org/whl/cu121"
    )
    .pip_install(
        "diffusers>=0.31", "transformers", "accelerate", "xformers",
        "imageio[ffmpeg]", "opencv-python", "controlnet-aux",
        "realesrgan", "rife-torch", "wav2lip-emotion"
    )
    .run_commands("git clone https://github.com/boujelbenramy-maker/t2v-cascade.git /repo")
)

@stub.function(gpu="A10G", image=image, timeout=900, secrets=[])
def run_cascade(prompt: str, image_bytes: bytes, duration: int, camera: str):
    import cv2, numpy as np, imageio
    from src.pipeline import generate_cascade
    # save uploaded image
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image_bytes)
        img_path = tmp.name
    # generate
    video_np = generate_cascade(prompt, img_path, duration, camera, target_fps=60)
    # save mp4
    out = "/tmp/out.mp4"
    imageio.mimsave(out, video_np, fps=60, codec="h264", ffmpeg_params=["-crf", "18"])
    return open(out, "rb").read()

@stub.local_entrypoint()
def main(prompt: str, img_path: str, duration: int = 8, camera: str = "static"):
    with open(img_path, "rb") as f:
        video_bytes = run_cascade.call(prompt, f.read(), duration, camera)
    output = Path("output_modal.mp4")
    output.write_bytes(video_bytes)
    print("✅ Vidéo sauvegardée : output_modal.mp4")
