#!/usr/bin/env python3
"""
Generate game visual assets via SD WebUI Forge / A1111 REST API.
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

DEFAULT_API_URL = "http://127.0.0.1:7860"
DEFAULT_NEGATIVE = "blurry, low quality, lowres, distorted anatomy, bad hands, missing fingers, extra digits, deformed, bad eyes, text, watermark, signature"

def check_api(base_url):
    try:
        url = f"{base_url.rstrip('/')}/sdapi/v1/options"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                current_model = data.get("sd_model_checkpoint", "Unknown")
                print(f"[OK] Generator API is online at {base_url}")
                print(f"[Model] Active checkpoint: {current_model}")
                return True
    except urllib.error.URLError as e:
        print(f"[ERROR] Cannot connect to generator API at {base_url}: {e.reason}")
        print("Make sure Stable Diffusion WebUI Forge is running (webui-user.bat with --api).")
        return False
    except Exception as e:
        print(f"[ERROR] Connection check failed: {e}")
        return False

def generate(prompt, negative, width, height, steps, cfg, sampler, out_path, base_url):
    url = f"{base_url.rstrip('/')}/sdapi/v1/txt2img"
    payload = {
        "prompt": prompt,
        "negative_prompt": negative or DEFAULT_NEGATIVE,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg_scale": cfg,
        "sampler_name": sampler or "Euler a",
        "save_images": False,
        "send_images": True,
    }

    print(f"[Generating] {width}x{height}, {steps} steps, sampler '{payload['sampler_name']}'...")
    print(f"[Prompt] {prompt}")

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode())
            images = result.get("images", [])
            if not images:
                print("[ERROR] Generator returned no images.")
                return False

            img_b64 = images[0]
            img_bytes = base64.b64decode(img_b64)

            os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
            with open(out_path, "wb") as f:
                f.write(img_bytes)

            print(f"[Saved] Asset generated successfully -> {out_path} ({len(img_bytes)} bytes)")
            return True
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        print(f"[ERROR] API HTTP error {e.code}: {err_msg}")
        return False
    except Exception as e:
        print(f"[ERROR] Generation failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Generate art via Forge / SD API")
    parser.add_argument("--check", action="store_true", help="Check API status and current model")
    parser.add_argument("--prompt", type=str, help="Text prompt for generation")
    parser.add_argument("--negative", type=str, default=DEFAULT_NEGATIVE, help="Negative prompt")
    parser.add_argument("--width", type=int, default=832, help="Image width (default 832)")
    parser.add_argument("--height", type=int, default=1152, help="Image height (default 1152)")
    parser.add_argument("--steps", type=int, default=25, help="Sampling steps (default 25)")
    parser.add_argument("--cfg", type=float, default=6.0, help="CFG scale (default 6.0)")
    parser.add_argument("--sampler", type=str, default="Euler a", help="Sampler name")
    parser.add_argument("--out", type=str, help="Output image file path")
    parser.add_argument("--api-url", type=str, default=DEFAULT_API_URL, help=f"API URL (default {DEFAULT_API_URL})")

    args = parser.parse_args()

    if args.check or not args.prompt:
        ok = check_api(args.api_url)
        if not args.prompt:
            sys.exit(0 if ok else 1)

    if not args.out:
        print("[ERROR] Please specify --out <path_to_save_image>")
        sys.exit(1)

    success = generate(
        prompt=args.prompt,
        negative=args.negative,
        width=args.width,
        height=args.height,
        steps=args.steps,
        cfg=args.cfg,
        sampler=args.sampler,
        out_path=args.out,
        base_url=args.api_url,
    )
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
