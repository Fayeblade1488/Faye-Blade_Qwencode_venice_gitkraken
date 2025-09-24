#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Venice AI Image Generation Module for Qwen Code
This module provides integration with Venice AI's image generation and upscaling API.
It enables uncensored image generation through the Venice platform.
"""

import argparse
import base64
import hashlib
import json
import os
import pathlib
import random
import signal
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class VeniceAIImageGenerator:
    """
    A class to interact with Venice AI's image generation API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("VENICE_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided. Use api_key parameter or set VENICE_API_KEY environment variable.")
        
        self.base_url = "https://api.venice.ai/api/v1"
        self.gen_endpoint = f"{self.base_url}/image/generate"
        self.upscale_endpoint = f"{self.base_url}/image/upscale"
        
        # Default settings for uncensored generation
        self.default_model = "flux-dev-uncensored"  # Uncensored model
        self.default_steps = 30  # Appropriate for uncensored model
        self.default_cfg = 5.0
        self.default_negative = ""  # Empty negative prompt for uncensored results
        self.default_safe_mode = False  # Disable safe mode for uncensored generation
        
        # Aspect ratio to dimensions mapping
        self.aspect_to_size = {
            "square": (1024, 1024),
            "tall": (768, 1024),
            "wide": (1024, 768),
        }
    
    def _session(self, timeout_connect=10, timeout_read=120) -> requests.Session:
        """Create a requests session with retry logic and timeout handling."""
        s = requests.Session()
        retry = Retry(
            total=5,
            read=5,
            connect=5,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["GET", "POST"])
        )
        s.mount("https://", HTTPAdapter(max_retries=retry))
        s.mount("http://", HTTPAdapter(max_retries=retry))
        s.request = self._with_timeouts(s.request, (timeout_connect, timeout_read))
        s.headers.update({
            "User-Agent": "qwen-cli-venice-integration/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
        })
        return s
    
    def _with_timeouts(self, func, timeouts: Tuple[int, int]):
        """Add timeout wrapper to request function."""
        def wrapper(method, url, **kwargs):
            timeout = kwargs.pop("timeout", (timeouts[0], timeouts[1]))
            time.sleep(random.uniform(0, 0.05))
            return func(method, url, timeout=timeout, **kwargs)
        return wrapper
    
    def _size_from_aspect(self, aspect: str) -> Tuple[int, int]:
        """Get dimensions from aspect ratio."""
        if aspect not in self.aspect_to_size:
            raise ValueError(f"Invalid aspect ratio: {aspect}. Choose from {list(self.aspect_to_size)}")
        return self.aspect_to_size[aspect]
    
    def _ensure_dir(self, p: pathlib.Path) -> None:
        """Ensure directory exists."""
        p.mkdir(parents=True, exist_ok=True)
    
    def _now_iso(self) -> str:
        """Get current time in ISO format."""
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    
    def _save_bytes(self, path: pathlib.Path, data: bytes) -> None:
        """Save bytes to file."""
        self._ensure_dir(path.parent)
        tmp = path.with_suffix(path.suffix + ".part")
        with open(tmp, "wb") as f:
            f.write(data)
        tmp.replace(path)
    
    def _decode_image_from_json(self, payload: Dict[str, Any]) -> bytes:
        """Decode image from JSON response."""
        if "image" in payload and isinstance(payload["image"], str):
            return base64.b64decode(payload["image"])
        if "images" in payload and isinstance(payload["images"], list) and payload["images"]:
            return base64.b64decode(payload["images"][0])
        raise KeyError("No image data found in response JSON.")
    
    def _is_binary_image_response(self, resp: requests.Response) -> bool:
        """Check if response is a binary image."""
        ctype = resp.headers.get("Content-Type", "")
        return ctype.startswith("image/")
    
    def _sha256(self, data: bytes) -> str:
        """Calculate SHA256 hash of data."""
        return hashlib.sha256(data).hexdigest()
    
    def _effective_dims(self, aspect: str, width: Optional[int], height: Optional[int]) -> Tuple[int, int]:
        """Get effective dimensions based on aspect ratio or specified dimensions."""
        if width and height:
            return int(width), int(height)
        return self._size_from_aspect(aspect)
    
    def generate_image(
        self,
        prompt: str,
        model: Optional[str] = None,
        aspect_ratio: str = "tall",
        width: Optional[int] = None,
        height: Optional[int] = None,
        steps: Optional[int] = None,
        cfg_scale: Optional[float] = None,
        negative_prompt: Optional[str] = None,
        seed: Optional[int] = None,
        output_format: str = "png",
        image_style: Optional[str] = None,
        hide_watermark: bool = True,
        embed_exif: bool = False,
        safe_mode: Optional[bool] = None,
        auto_upscale: bool = True,
        upscale_scale: int = 4,
        upscale_enhance: bool = True,
        upscale_creativity: float = 0.15,
        upscale_replication: float = 0.35,
        upscale_prompt: Optional[str] = None,
        output_dir: str = "generated",
        output_name: Optional[str] = None,
        verbose: bool = False,
    ) -> Dict[str, Any]:
        """
        Generate an image using Venice AI.
        
        Args:
            prompt: The prompt for image generation
            model: Model to use (defaults to uncensored model)
            aspect_ratio: Aspect ratio for output (square, tall, wide)
            width: Override width
            height: Override height
            steps: Number of inference steps
            cfg_scale: Classifier-free guidance scale
            negative_prompt: Negative prompt
            seed: Random seed
            output_format: Output format (png, webp)
            image_style: Style preset
            hide_watermark: Whether to hide watermark
            embed_exif: Whether to embed EXIF
            safe_mode: Whether to use safe mode (default False for uncensored)
            auto_upscale: Whether to automatically upscale generated images
            upscale_scale: Upscale scale factor
            upscale_enhance: Whether to enhance details during upscaling
            upscale_creativity: Creativity strength for enhancement
            upscale_replication: Replication factor during upscaling
            upscale_prompt: Prompt to guide enhancement
            output_dir: Directory for outputs
            output_name: Base output filename
            verbose: Verbose output
            
        Returns:
            Dictionary with generation results
        """
        # Set defaults if not provided
        model = model or self.default_model
        steps = steps or self.default_steps
        cfg_scale = cfg_scale or self.default_cfg
        negative_prompt = negative_prompt or self.default_negative
        safe_mode = safe_mode if safe_mode is not None else self.default_safe_mode
        
        if verbose:
            print(f"Generating image with prompt: '{prompt}' using model: {model}")
        
        # Get dimensions
        w, h = self._effective_dims(aspect_ratio, width, height)
        
        # Create the session and request
        s = self._session()
        data: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": w,
            "height": h,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "format": output_format,
            "hide_watermark": hide_watermark,
            "embed_exif_metadata": embed_exif,
            "safe_mode": safe_mode,  # Explicitly disable for uncensored generation
        }
        
        if seed is not None:
            data["seed"] = seed
        if image_style and image_style.lower() != "none":
            data["style_preset"] = image_style
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = s.post(self.gen_endpoint, headers=headers, json=data)
        req_id = resp.headers.get("x-request-id") or resp.headers.get("X-Request-ID")
        
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            err = {"status": resp.status_code, "text": resp.text, "request_id": req_id}
            try:
                err["json"] = resp.json()
            except Exception:
                pass
            raise requests.HTTPError(json.dumps(err)) from None
        
        # Handle the response
        if self._is_binary_image_response(resp):
            result: Dict[str, Any] = {"images": [base64.b64encode(resp.content).decode("utf-8")]}
        else:
            result = resp.json()
        
        # Extract image data
        images_b64: List[str] = []
        if "images" in result and isinstance(result["images"], list):
            images_b64 = [img for img in result["images"] if isinstance(img, str)]
        elif "image" in result and isinstance(result["image"], str):
            images_b64 = [result["image"]]
        else:
            raise KeyError("No images found in generation response.")
        
        if not images_b64:
            raise ValueError("No image generated.")
        
        # Decode the first image
        b = base64.b64decode(images_b64[0])
        output = {"bytes": b, "meta": {"response": result, "request_id": req_id}}
        
        if verbose:
            print(f"[gen] got {len(b)} bytes (sha256={self._sha256(b)[:12]})", file=sys.stderr)
        
        # Save the generated image
        out_dir = pathlib.Path(output_dir).resolve()
        upscaled_dir = out_dir / "upscaled"
        meta_dir = out_dir / "metadata"
        self._ensure_dir(out_dir)
        self._ensure_dir(upscaled_dir)
        self._ensure_dir(meta_dir)
        
        # Create filename
        ts_short = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
        seed_tag = f"s{seed}" if seed is not None else "rnd"
        stem = f"{output_name or 'venice_image'}_{seed_tag}_{ts_short}_1"
        img_path = out_dir / f"{stem}.{output_format}"
        
        # Save image
        self._save_bytes(img_path, b)
        sha = self._sha256(b)
        
        # Create metadata
        meta_payload = {
            "timestamp": self._now_iso(),
            "mode": "generate",
            "request_params": {
                "prompt": prompt,
                "model": model,
                "aspect_ratio": aspect_ratio,
                "width": width,
                "height": height,
                "steps": steps,
                "cfg_scale": cfg_scale,
                "negative_prompt": negative_prompt,
                "seed": seed,
                "output_format": output_format,
                "image_style": image_style,
                "hide_watermark": hide_watermark,
                "embed_exif": embed_exif,
                "safe_mode": safe_mode,
            },
            "response_meta": output.get("meta", {}),
            "output_sha256": sha,
            "output_path": str(img_path),
        }
        
        # Save metadata
        meta_path = meta_dir / f"{stem}.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta_payload, f, ensure_ascii=False, indent=2)
        
        result_dict = {
            "success": True,
            "generated_image_path": str(img_path),
            "metadata_path": str(meta_path),
            "image_sha256": sha,
            "request_id": req_id,
            "response_data": result
        }
        
        # Upscale if requested
        if auto_upscale:
            try:
                up_bytes, up_meta = self.upscale_image_bytes(
                    b, scale=upscale_scale, enhance=upscale_enhance,
                    enhance_creativity=upscale_creativity, enhance_prompt=upscale_prompt,
                    replication=upscale_replication, verbose=verbose
                )
                
                up_path = upscaled_dir / f"{stem}_upscaled.{output_format}"
                self._save_bytes(up_path, up_bytes)
                up_sha = self._sha256(up_bytes)
                
                up_meta_payload = {
                    "timestamp": self._now_iso(),
                    "mode": "upscale_post_gen",
                    "source_image": str(img_path),
                    "upscale_params": {
                        "scale": upscale_scale,
                        "enhance": upscale_enhance,
                        "creativity": upscale_creativity,
                        "replication": upscale_replication,
                        "enhance_prompt": upscale_prompt,
                    },
                    "response_meta": up_meta,
                    "output_sha256": up_sha,
                    "output_path": str(up_path),
                }
                
                up_meta_path = meta_dir / f"{stem}_upscaled.json"
                with open(up_meta_path, "w", encoding="utf-8") as f:
                    json.dump(up_meta_payload, f, ensure_ascii=False, indent=2)
                
                result_dict["upscaled_image_path"] = str(up_path)
                result_dict["upscaled_metadata_path"] = str(up_meta_path)
                result_dict["upscaled_image_sha256"] = up_sha
                
                if verbose:
                    print(f"Upscaled → {up_path}")
                
            except Exception as e:
                if verbose:
                    print(f"Warning: Upscaling failed: {e}", file=sys.stderr)
                result_dict["upscale_error"] = str(e)
        
        if verbose:
            print(f"Generated → {img_path}")
        
        return result_dict
    
    def upscale_image_bytes(
        self,
        image_bytes: bytes,
        scale: int = 4,
        enhance: bool = True,
        enhance_creativity: float = 0.15,
        enhance_prompt: Optional[str] = None,
        replication: float = 0.35,
        verbose: bool = False,
    ) -> Tuple[bytes, Dict[str, Any]]:
        """
        Upscale an image using Venice AI.
        
        Args:
            image_bytes: Image bytes to upscale
            scale: Scale factor (2, 3, 4, 8)
            enhance: Whether to enhance details
            enhance_creativity: Creativity strength for enhancement
            enhance_prompt: Prompt to guide enhancement
            replication: Replication factor
            verbose: Verbose output
            
        Returns:
            Tuple of upscaled image bytes and response metadata
        """
        s = self._session()
        img_b64 = base64.b64encode(image_bytes).decode("utf-8")
        data: Dict[str, Any] = {
            "image": img_b64,
            "scale": scale,
            "enhance": enhance,
            "enhanceCreativity": enhance_creativity,
            "replication": replication,
        }
        if enhance_prompt:
            data["enhancePrompt"] = enhance_prompt
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = s.post(self.upscale_endpoint, headers=headers, json=data)
        req_id = resp.headers.get("x-request-id") or resp.headers.get("X-Request-ID")
        
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            err = {"status": resp.status_code, "text": resp.text, "request_id": req_id}
            try:
                err["json"] = resp.json()
            except Exception:
                pass
            raise requests.HTTPError(json.dumps(err)) from None
        
        if self._is_binary_image_response(resp):
            up_bytes, payload = resp.content, {"binary": True, "status_code": resp.status_code, "request_id": req_id}
        else:
            payload = resp.json()
            up_bytes = self._decode_image_from_json(payload)
            payload["request_id"] = req_id
        
        if verbose:
            print(f"[upscale] got {len(up_bytes)} bytes (sha256={self._sha256(up_bytes)[:12]})", file=sys.stderr)
        
        return up_bytes, payload
    
    def upscale_image_file(
        self,
        image_path: str,
        output_path: Optional[str] = None,
        scale: int = 4,
        enhance: bool = True,
        enhance_creativity: float = 0.15,
        enhance_prompt: Optional[str] = None,
        replication: float = 0.35,
        verbose: bool = False,
    ) -> Dict[str, Any]:
        """
        Upscale an image file using Venice AI.
        
        Args:
            image_path: Path to the input image file
            output_path: Path for the output image (optional)
            scale: Scale factor (2, 3, 4, 8)
            enhance: Whether to enhance details
            enhance_creativity: Creativity strength for enhancement
            enhance_prompt: Prompt to guide enhancement
            replication: Replication factor
            verbose: Verbose output
            
        Returns:
            Dictionary with upscaling results
        """
        # Read the input image
        with open(image_path, "rb") as f:
            raw = f.read()
        
        # Upscale
        up_bytes, up_meta = self.upscale_image_bytes(
            raw, scale, enhance, enhance_creativity, enhance_prompt, replication, verbose
        )
        
        # Determine output path
        if output_path is None:
            path_obj = pathlib.Path(image_path)
            output_path = path_obj.with_name(f"{path_obj.stem}_upscaled{path_obj.suffix}")
        
        # Save upscaled image
        with open(output_path, "wb") as f:
            f.write(up_bytes)
        
        result = {
            "success": True,
            "input_path": image_path,
            "output_path": output_path,
            "input_sha256": self._sha256(raw),
            "output_sha256": self._sha256(up_bytes),
            "request_id": up_meta.get("request_id"),
            "response_meta": up_meta
        }
        
        if verbose:
            print(f"Upscaled image → {output_path}")
        
        return result
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List all available models from Venice API."""
        s = self._session()
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = s.get(f"{self.base_url}/models", headers=headers)
        
        try:
            resp.raise_for_status()
            data = resp.json()
            return data.get("data", [])
        except requests.HTTPError:
            print(f"Error listing models: {resp.status_code} - {resp.text}")
            return []
    
    def get_uncensored_models(self) -> List[Dict[str, Any]]:
        """Get only the uncensored models from Venice API."""
        all_models = self.list_models()
        uncensored_keywords = ["uncensored", "flux-dev", "lustify"]
        
        uncensored_models = []
        for model in all_models:
            model_id = model.get("id", "").lower()
            model_name = model.get("model_spec", {}).get("name", "").lower()
            
            # Check if the model name or ID contains uncensored keywords
            if any(keyword in model_id or keyword in model_name for keyword in uncensored_keywords):
                uncensored_models.append(model)
        
        return uncensored_models


# Example usage
if __name__ == "__main__":
    # This would be run as a command line tool
    parser = argparse.ArgumentParser(description="Venice AI Image Generator with Uncensored Capabilities")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt for image generation")
    parser.add_argument("--model", type=str, default="flux-dev-uncensored", help="Model to use for generation")
    parser.add_argument("--aspect-ratio", type=str, default="tall", choices=["square", "tall", "wide"], help="Aspect ratio for output")
    parser.add_argument("--output-dir", type=str, default="generated", help="Directory for outputs")
    parser.add_argument("--output-name", type=str, help="Base output filename")
    parser.add_argument("--steps", type=int, default=30, help="Number of inference steps")
    parser.add_argument("--cfg-scale", type=float, default=5.0, help="Classifier-free guidance scale")
    parser.add_argument("--seed", type=int, help="Random seed for generation")
    parser.add_argument("--format", type=str, default="png", choices=["png", "webp"], help="Output format")
    parser.add_argument("--safe-mode", action="store_true", help="Enable safe mode (default: False for uncensored)")
    parser.add_argument("--no-safe-mode", action="store_true", help="Explicitly disable safe mode")
    parser.add_argument("--no-watermark", action="store_true", help="Hide watermark (default: True)")
    parser.add_argument("--upscale", action="store_true", help="Automatically upscale generated images")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--api-key", type=str, help="Venice API key (or set VENICE_API_KEY env var)")
    
    args = parser.parse_args()
    
    # Determine safe mode
    if args.no_safe_mode:
        safe_mode = False
    elif args.safe_mode:
        safe_mode = True
    else:
        safe_mode = False  # Default to False for uncensored
    
    # Create generator instance
    try:
        generator = VeniceAIImageGenerator(api_key=args.api_key)
        
        # Generate image
        result = generator.generate_image(
            prompt=args.prompt,
            model=args.model,
            aspect_ratio=args.aspect_ratio,
            steps=args.steps,
            cfg_scale=args.cfg_scale,
            seed=args.seed,
            output_format=args.format,
            safe_mode=safe_mode,
            hide_watermark=not args.no_watermark,
            auto_upscale=args.upscale,
            output_dir=args.output_dir,
            output_name=args.output_name,
            verbose=args.verbose
        )
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)