#!/usr/bin/env python3
"""Generate videos with Seedance-style provider APIs.

Public teaching version:
- reads keys from environment or local config.json
- supports dry-run without paid network calls
- avoids personal paths and private asset IDs
- uses only the Python standard library
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ARK_BASE = "https://ark.cn-beijing.volces.com/api/v3"
ARK_MODEL_STD = "doubao-seedance-2-0-260128"
ARK_MODEL_FAST = "doubao-seedance-2-0-fast-260128"

FAL_BASE = "https://fal.run"
FAL_SLUG_T2V = "bytedance/seedance-2.0/text-to-video"
FAL_SLUG_T2V_FAST = "bytedance/seedance-2.0/fast/text-to-video"
FAL_SLUG_I2V = "bytedance/seedance-2.0/image-to-video"
FAL_SLUG_I2V_FAST = "bytedance/seedance-2.0/fast/image-to-video"

POLL_INTERVAL_SECONDS = 15
POLL_MAX_TRIES = 60
MIN_VALID_BYTES = 100 * 1024


def mask_secret(value: str | None) -> str | None:
    if not value:
        return None
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}***{value[-4:]}"


def load_api_key(provider: str) -> tuple[str | None, str]:
    env_var = "ARK_API_KEY" if provider == "ark" else "FAL_KEY"
    key = os.environ.get(env_var)
    if key:
        return key, env_var

    cfg = Path(__file__).resolve().parents[1] / "config.json"
    if cfg.exists():
        try:
            data = json.loads(cfg.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        key = data.get("ark_api_key" if provider == "ark" else "fal_key")
        if key:
            return key, str(cfg)

    return None, env_var


def file_to_data_url(path_text: str, default_mime: str) -> str:
    path = Path(path_text).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Input file does not exist: {path_text}")
    mime = mimetypes.guess_type(str(path))[0] or default_mime
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def image_to_url(value: str) -> str:
    if value.startswith(("http://", "https://", "asset://", "data:image/")):
        return value
    return file_to_data_url(value, "image/png")


def video_to_url(value: str) -> str:
    if value.startswith(("http://", "https://", "asset://")):
        return value
    return file_to_data_url(value, "video/mp4")


def build_ark_request(args: argparse.Namespace, api_key: str | None) -> dict:
    model = ARK_MODEL_FAST if args.fast else ARK_MODEL_STD
    content = [{"type": "text", "text": args.prompt}]

    for image in args.image or []:
        content.append({
            "type": "image_url",
            "image_url": {"url": image_to_url(image)},
            "role": args.image_role,
        })

    for video in args.video or []:
        content.append({
            "type": "video_url",
            "video_url": {"url": video_to_url(video)},
            "role": "reference_video",
        })

    if args.audio:
        content.append({
            "type": "audio_url",
            "audio_url": {"url": args.audio},
            "role": "reference_audio",
        })

    body = {
        "model": model,
        "content": content,
        "ratio": args.ratio,
        "duration": args.duration,
        "resolution": args.resolution,
        "generate_audio": not args.no_audio,
    }

    if args.seed is not None:
        body["seed"] = args.seed
    if args.camera_fixed:
        body["camera_fixed"] = True
    if args.return_last_frame:
        body["return_last_frame"] = True
    if args.web_search:
        body["tools"] = [{"type": "web_search"}]

    return {
        "provider": "ark",
        "method": "POST",
        "url": f"{ARK_BASE}/contents/generations/tasks",
        "headers": {
            "Authorization": f"Bearer {api_key}" if api_key else "Bearer <ARK_API_KEY>",
            "Content-Type": "application/json",
        },
        "body": body,
        "poll_url_template": f"{ARK_BASE}/contents/generations/tasks/{{task_id}}",
    }


def build_fal_request(args: argparse.Namespace, api_key: str | None) -> dict:
    if args.video:
        raise ValueError("--video is only implemented for provider=ark in this script")

    if args.image:
        slug = FAL_SLUG_I2V_FAST if args.fast else FAL_SLUG_I2V
    else:
        slug = FAL_SLUG_T2V_FAST if args.fast else FAL_SLUG_T2V

    body = {
        "prompt": args.prompt,
        "resolution": args.resolution,
        "duration": str(args.duration),
        "aspect_ratio": args.ratio,
        "generate_audio": not args.no_audio,
    }
    if args.seed is not None:
        body["seed"] = args.seed
    if args.image:
        body["image_url"] = image_to_url(args.image[0])

    return {
        "provider": "fal",
        "method": "POST",
        "url": f"{FAL_BASE}/{slug}",
        "headers": {
            "Authorization": f"Key {api_key}" if api_key else "Key <FAL_KEY>",
            "Content-Type": "application/json",
        },
        "body": body,
        "poll_url_template": None,
    }


def post_json(url: str, headers: dict, body: dict, timeout: int = 120) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def get_json(url: str, headers: dict, timeout: int = 60) -> dict:
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def run_ark(spec: dict) -> tuple[str, str, str | None, int | None]:
    created = post_json(spec["url"], spec["headers"], spec["body"])
    task_id = created.get("id")
    if not task_id:
        raise RuntimeError(f"Task creation returned no id: {created}")

    print(f"[ark] task created: {task_id}", file=sys.stderr)
    poll_url = spec["poll_url_template"].format(task_id=task_id)

    for index in range(POLL_MAX_TRIES):
        time.sleep(POLL_INTERVAL_SECONDS)
        status_payload = get_json(poll_url, spec["headers"])
        status = status_payload.get("status")
        print(f"[ark] poll {index + 1}/{POLL_MAX_TRIES}: {status}", file=sys.stderr)

        if status == "succeeded":
            content = status_payload.get("content") or {}
            video_url = content.get("video_url")
            if not video_url:
                raise RuntimeError(f"Task succeeded but no video_url was returned: {status_payload}")
            return task_id, video_url, content.get("last_frame_url"), status_payload.get("seed")

        if status == "failed":
            raise RuntimeError(f"Task failed: {status_payload}")

    raise TimeoutError(f"Polling timed out; task_id={task_id}")


def run_fal(spec: dict) -> tuple[None, str, None, int | None]:
    result = post_json(spec["url"], spec["headers"], spec["body"])
    video_url = (result.get("video") or {}).get("url") or result.get("video_url")
    if not video_url:
        raise RuntimeError(f"fal response did not include a video URL: {result}")
    return None, video_url, None, result.get("seed")


def download_file(url: str, output_dir: Path, output_name: str) -> tuple[Path, int]:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / os.path.basename(output_name)
    with urllib.request.urlopen(url, timeout=300) as response:
        output_path.write_bytes(response.read())
    size = output_path.stat().st_size
    if size < MIN_VALID_BYTES:
        raise RuntimeError(f"Downloaded file is too small ({size} bytes); treating as failed")
    return output_path, size


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a video with Seedance-style provider APIs")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--provider", choices=["ark", "fal"], default="ark")
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--duration", type=int, default=5)
    parser.add_argument("--resolution", choices=["480p", "720p", "1080p"], default="720p")
    parser.add_argument("--ratio", choices=["16:9", "9:16", "1:1", "4:3", "3:4", "21:9", "adaptive"], default="16:9")
    parser.add_argument("--image", action="append", default=None)
    parser.add_argument("--image-role", choices=["first_frame", "last_frame", "reference_image"], default="first_frame")
    parser.add_argument("--video", action="append", default=None)
    parser.add_argument("--audio", default=None)
    parser.add_argument("--no-audio", action="store_true")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--camera-fixed", action="store_true")
    parser.add_argument("--return-last-frame", action="store_true")
    parser.add_argument("--web-search", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--output-dir", default=str(Path.home() / "Downloads"))
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.duration != -1 and not 4 <= args.duration <= 15:
        print(json.dumps({"success": False, "error": "duration must be 4-15 or -1"}, ensure_ascii=False))
        return 2

    api_key, key_source = load_api_key(args.provider)
    builder = build_ark_request if args.provider == "ark" else build_fal_request

    try:
        spec = builder(args, api_key)
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False))
        return 2

    if args.dry_run:
        printable = {
            "dry_run": True,
            "provider": spec["provider"],
            "method": spec["method"],
            "url": spec["url"],
            "headers": dict(spec["headers"]),
            "body": spec["body"],
            "poll_url_template": spec["poll_url_template"],
            "api_key_source": key_source,
            "api_key_present": bool(api_key),
        }
        auth = printable["headers"].get("Authorization")
        if auth and api_key:
            printable["headers"]["Authorization"] = auth.replace(api_key, mask_secret(api_key) or "***")
        print(json.dumps(printable, ensure_ascii=False, indent=2))
        return 0

    if not api_key:
        message = f"Missing API key. Set {'ARK_API_KEY' if args.provider == 'ark' else 'FAL_KEY'} or local config.json."
        print(json.dumps({"success": False, "error": message}, ensure_ascii=False))
        return 3

    output_name = os.path.basename(args.output or f"seedance-{int(time.time())}.mp4")
    output_dir = Path(args.output_dir).expanduser()

    try:
        runner = run_ark if args.provider == "ark" else run_fal
        task_id, video_url, last_frame_url, seed = runner(spec)
        output_path, size = download_file(video_url, output_dir, output_name)
        result = {
            "success": True,
            "local_path": str(output_path.resolve()),
            "task_id": task_id,
            "size_bytes": size,
            "seed": seed,
        }
        if last_frame_url:
            result["last_frame_url"] = last_frame_url
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(json.dumps({"success": False, "error": f"HTTP {exc.code}: {detail}"}, ensure_ascii=False))
        return 1
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
