---
name: google-flow-generate
description: Generate images in Google Flow through a logged-in browser. Use for concept images, style exploration, mood images, design communication, text-to-image, and image-to-image tasks in Google Flow.
---

# Google Flow Generate

Use this skill to operate Google Flow from Codex. It is a browser workflow, so login state matters.

## Inputs

Collect or infer:

- `mode`: text-to-image or image-to-image
- `prompt`: one clean prompt
- `aspect_ratio`: for example `16:9`, `9:16`, `4:3`, `3:4`
- `model`: use the user's requested Flow model, otherwise keep the current default in the UI
- `reference_image`: required only for image-to-image
- `output_filename`: requested final filename

## Workflow

1. Use `cdp-browser-reuse` or the Chrome/Browser tool to open a logged-in Google Flow tab.
2. Navigate to Google Flow.
3. Confirm the page is loaded and not on a login screen.
4. Set model and aspect ratio only when the UI exposes those settings.
5. Use the real prompt textbox. Google Flow often uses `div[contenteditable="true"][role="textbox"]`.
6. Keep the prompt single-line before typing. Newlines can submit too early in some composer UIs.
7. Type with a human-like delay if using Playwright keyboard input.
8. Submit once.
9. Wait for generation, then inspect the result before downloading.
10. Save to `~/Downloads` unless the user provides another destination.

## Prompt Handling

Do this before typing:

```python
prompt = " ".join(prompt.split())
assert "\n" not in prompt
```

For longer prompts, submit one at a time. If the site reports unusual activity or rate limiting, stop and tell the user instead of retrying repeatedly.

## Quality Check

Before returning the file path, check:

- The generated image matches the requested subject.
- The aspect ratio is close to the requested ratio.
- The image does not include unwanted cameras, watermarks, random text, or unrelated people.
- Any required Chinese or English text is readable enough for the intended use.

## Failure Handling

- Login screen: ask the user to log in manually.
- Prompt not entered: refocus the contenteditable textbox and retry once.
- Generation failure: report the visible error and stop.
- Rate limit or unusual activity: stop and wait for user direction.
- Download blocked: use browser download controls or fetch the image URL with page credentials.

## Boundaries

This skill only drives Google Flow. It does not decide the creative direction, rewrite long marketing copy, or perform final poster layout unless the user explicitly asks.
