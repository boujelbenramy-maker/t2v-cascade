#!/usr/bin/env python3
"""
CLI client Modal
Usage :
python modal/generate.py --prompt "un dragon au coucher du soleil" --img frame.png --duration 10 --camera zoom_in
"""
import argparse, pathlib, requests

def main():
    parser = argparse.ArgumentParser(description="Génère une vidéo 4K 60 fps via Modal")
    parser.add_argument("--prompt", required=True, help="Texte prompt")
    parser.add_argument("--img", required=True, help="Chemin image de départ")
    parser.add_argument("--duration", type=int, default=8, help="Durée en secondes")
    parser.add_argument("--camera", default="static", choices=["static", "pan_left", "zoom_in", "dolly_out"])
    args = parser.parse_args()

    print("🔥 Lancement sur Modal...")
    # appel local Modal
    import subprocess
    subprocess.run([
        "modal", "run", "modal/main.py",
        "--prompt", args.prompt,
        "--img", args.img,
        "--duration", str(args.duration),
        "--camera", args.camera
    ])

if __name__ == "__main__":
    main()
