---
name: chatgpt-image
description: Generate images through the ChatGPT web app from Codex. Use when the user asks for ChatGPT image generation, GPT-Image generation, image-to-image through ChatGPT, visual concept creation, posters, diagrams, reference sheets, or series image generation.
---

# ChatGPT Image

Use this skill to generate images in the ChatGPT web app. This is a logged-in browser workflow.

## Inputs

Collect or infer:

- `prompt`: the final visual instruction
- `output_filename`: final image filename
- `fresh_chat`: default `true`
- `reference_image`: optional local path
- `expected_image_count`: default `1`

## Workflow

1. Use `cdp-browser-reuse` or the Chrome/Browser tool to connect to a logged-in ChatGPT tab.
2. Confirm the page is not on a login screen.
3. Start a fresh chat unless the user needs the current conversation context.
4. If a reference image is provided, upload it through an image-accepting file input and verify that the user message contains an image after submit.
5. Keep the prompt focused on the desired output, required elements, exclusions, and aspect ratio.
6. Type or paste the prompt carefully. If using keyboard typing, avoid raw newline characters unless sending `Shift+Enter`.
7. Submit with the send button, not the Enter key.
8. Wait for image generation. Do not call failure before a reasonable wait has passed.
9. Find the generated image in the main conversation area, excluding images from the user's uploaded message.
10. Download the image to `~/Downloads` unless the user specifies another destination.
11. If a temporary task tab was opened, close it after download while keeping at least one ChatGPT tab alive when possible.

## Prompt Pattern

Use a compact structure:

```text
Goal: one sentence describing the final image.
Style: visual style, medium, mood.
Must include: exact objects, text, colors, layout, aspect ratio.
Must not include: fake QR codes, random logos, extra people, unreadable text.
Output: one image, requested aspect ratio.
```

For a series, explicitly request separate images:

```text
Do not create a collage. Generate {N} separate images in order. Each image should be a standalone {aspect_ratio} image. Do not ask me to continue; complete all {N} images in this run.
```

## Reference Image Checks

When uploading a reference image:

- Prefer file inputs whose `accept` contains `image`.
- After submit, inspect the last user message and confirm it includes an image.
- If the model says it has no reference image, stop and retry the upload once.

## Download Selector Guidance

When using browser automation, avoid hard-coding an image CDN domain. Prefer:

- Generated image `alt` text when present.
- Images in `main` or assistant message containers.
- Excluding images inside `[data-message-author-role="user"]`.
- A size check such as `naturalWidth >= 700`.

## Failure Handling

- Login screen: ask the user to log in manually.
- Content policy error: report it and offer a safer rewrite.
- Generation error: do not repeatedly hit regenerate; diagnose prompt length, policy, or login state.
- No image after waiting: report timeout and preserve the chat for user inspection if useful.

## Boundaries

This skill only drives ChatGPT image generation and download. Prompt strategy, design critique, final layout, and post-processing belong to other skills unless the user asks for them here.
