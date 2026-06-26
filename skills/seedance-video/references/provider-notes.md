# Seedance Provider Notes

Provider APIs, model IDs, pricing, and access rules can change. Before teaching exact prices or promising availability, check the current official provider docs.

## Ark

Typical integration shape:

- Create an async generation task.
- Receive a task ID.
- Poll task status.
- On success, receive a temporary video URL.
- Download immediately because provider-hosted URLs may expire.

The public script uses:

- `ARK_API_KEY`
- Ark base URL configured in `scripts/seedance_generate.py`
- Standard and fast model IDs configured in the script

## fal.ai

fal.ai is included as a backup route. Its model slugs and response schema can change, so treat it as best-effort unless you verify against current fal docs.

The public script uses:

- `FAL_KEY`
- text-to-video and image-to-video slugs configured in `scripts/seedance_generate.py`

## Cost Control

- Always use `--dry-run` for debugging.
- Use short duration and lower resolution for tests.
- Do not retry failed paid generations blindly.
- Keep task IDs in the final report so the user can inspect provider logs.
