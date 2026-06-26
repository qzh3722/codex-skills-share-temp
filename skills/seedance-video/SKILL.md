---
name: seedance-video
description: Generate videos with Seedance 2.0 through an API script. Use when the user asks for Seedance, Jimeng/即梦, text-to-video, image-to-video, reference-video generation, short AI video clips, interior walkthrough videos, product videos, or wants to turn a prompt plus optional media into an mp4 file.
---

# Seedance Video

Use this skill to generate an MP4 video with Seedance 2.0. The skill is an execution layer: it accepts a prompt and parameters, calls the provider API, polls the task, downloads the result, and returns a local path.

It does not write the creative prompt from scratch unless the user asks. For prompt patterns, read `references/prompt-guide.md`.

## Safety Rules

- Do not recharge, bind a card, open a paid model, or make any paid account change for the user.
- If the API key is missing, authentication fails, or balance is insufficient, stop and tell the user what they need to do manually.
- Use `--dry-run` first when testing parameters. Dry-run builds the request body but sends no paid request.
- Do not commit `config.json`, API keys, asset IDs tied to private people, customer material, or downloaded videos.
- Do not bypass face, copyright, or platform policy checks.

## Configuration

Preferred: set environment variables.

```bash
ARK_API_KEY="your_ark_key"
FAL_KEY="your_fal_key"
```

Optional local config file next to the script:

```json
{
  "ark_api_key": "YOUR_ARK_API_KEY_HERE",
  "fal_key": "YOUR_FAL_KEY_HERE"
}
```

Only `config.json.example` belongs in the repository. Real `config.json` must stay local.

## Providers

Default provider is Ark:

| Provider | CLI value | Key env var | Notes |
|---|---|---|---|
| Volcengine Ark | `ark` | `ARK_API_KEY` | Official ByteDance/Volcengine channel, async task API |
| fal.ai | `fal` | `FAL_KEY` | Backup provider; API details may differ by model version |

For pricing, model IDs, region, quota, and access rules, check the provider's current official docs before promising costs or availability.

## Command

Run the script from the installed skill directory:

```bash
python scripts/seedance_generate.py --dry-run --prompt "A warm modern living room, slow cinematic camera push-in, soft daylight, 5 seconds"
```

Real generation:

```bash
python scripts/seedance_generate.py \
  --prompt "A warm modern living room, slow cinematic camera push-in, soft daylight" \
  --duration 5 \
  --resolution 720p \
  --ratio 16:9 \
  --output living-room.mp4
```

Image-to-video:

```bash
python scripts/seedance_generate.py \
  --prompt "Image1 is the first frame. The camera slowly pushes toward the window. Keep the furniture and color palette consistent." \
  --image ./living-room.jpg \
  --image-role first_frame \
  --duration 6 \
  --output living-room-motion.mp4
```

## Parameters

- `--prompt`: required text prompt.
- `--provider`: `ark` or `fal`, default `ark`.
- `--fast`: use the provider's fast model/route when supported.
- `--duration`: `4-15` seconds, default `5`; Ark also accepts `-1` for provider smart duration when supported.
- `--resolution`: `480p`, `720p`, or `1080p`, default `720p`.
- `--ratio`: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`, or `adaptive`.
- `--image`: optional image path, URL, or `asset://...`; can be repeated.
- `--image-role`: `first_frame`, `last_frame`, or `reference_image`.
- `--video`: optional reference video URL for Ark; public URL is safest.
- `--audio`: optional reference audio URL or `asset://...`.
- `--no-audio`: disable generated audio when supported.
- `--seed`: optional integer seed.
- `--camera-fixed`: request fixed camera when supported.
- `--return-last-frame`: request a last-frame URL when supported.
- `--web-search`: request provider web search when supported.
- `--output`: output filename, sanitized to basename.
- `--output-dir`: destination directory, default `~/Downloads`.
- `--dry-run`: print request and exit without network generation.

## Workflow

1. Clarify prompt, duration, ratio, resolution, provider, output filename, and input media.
2. Read `references/prompt-guide.md` only when the user needs prompt help.
3. Run dry-run and inspect the request body.
4. If real generation is requested, confirm API key is configured.
5. Run the script.
6. Wait for async polling to finish.
7. Return the absolute MP4 path, task ID, seed, file size, and any last-frame URL.

## Result JSON

The script prints JSON on the final stdout line:

```json
{
  "success": true,
  "local_path": "/Users/example/Downloads/seedance-123.mp4",
  "task_id": "provider-task-id",
  "size_bytes": 1234567,
  "seed": 1234,
  "last_frame_url": "https://..."
}
```

On failure:

```json
{"success": false, "error": "reason"}
```

## Common Failures

| Symptom | Action |
|---|---|
| Missing key | Ask the user to set `ARK_API_KEY` or `FAL_KEY`; do not continue |
| 401/403 | Key wrong, model not enabled, quota/balance issue, or permission problem |
| Task failed | Report provider error; do not blindly retry |
| Poll timeout | Return the task ID so the user can check provider console |
| Video URL expired | Regenerate or check provider console; download immediately after success |
| Reference video rejected | Use a public URL and check provider input limits |

## Human Face and Private Media

Only use real people's faces when the user has rights and the provider supports the required authorization path. Use provider-managed assets such as `asset://...` only when the user supplies them. Do not include private asset IDs in shared examples.

## Boundaries

This skill generates the raw video. It does not do final editing, subtitles, music mixing, multi-clip stitching, quality review, or upload/publishing unless the user separately asks.
