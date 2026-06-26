# Seedance Prompt Guide

Use this file only when the user needs help writing or improving a Seedance prompt.

## Core Formula

For one simple shot:

```text
visual style, subject, action, environment and lighting, camera movement, sound
```

Example:

```text
Warm documentary interior style, afternoon sunlight enters a modern living room through sheer curtains, the camera slowly pushes forward past a wooden coffee table and beige sofa, dust floats in the light beam, soft wind and distant birds in the background.
```

## Timed Structure

For 9-15 second videos, split the prompt by time:

```text
15-second cinematic interior walkthrough.
0-4s: establish the entrance and move forward slowly.
4-8s: turn right into the living room and glide past the sofa.
8-12s: pass the dining table and kitchen island.
12-15s: settle on the final hero composition.
```

Keep the number of scene changes realistic. A 5-second clip should not contain three rooms and multiple actions.

## Referencing Media

When the script receives images, videos, or audio, refer to them by order:

- `Image1`, `Image2`
- `Video1`, `Video2`
- `Audio1`

Say what each item is for:

```text
Image1 is the first frame. Image2 is the product reference. Video1 is the camera movement reference. Keep the product shape from Image2 while following the motion rhythm of Video1.
```

Do not write private asset IDs inside the prompt body. Use `Image1` / `Video1` instead.

## Camera Language

Use clear camera terms:

- slow push-in
- pull-back
- pan left/right
- tilt up/down
- tracking shot
- orbit shot
- handheld documentary movement
- fixed camera
- first-person walkthrough

Avoid combining too many camera moves in one short clip. A stable prompt usually uses one or two movements.

## Interior Design Walkthrough

For multiple renderings from one project:

```text
Modern warm minimalist home walkthrough, first-person perspective, one continuous smooth camera move. These images are rooms from the same home; keep the same material palette, lighting, and design style throughout.
Image1 = entryway. Image2 = living room to the right of the entryway. Image3 = open dining-kitchen at the end of the living room.
0-4s: start from Image1 and move forward through the entryway.
4-9s: turn right into Image2, gliding past sofa and coffee table.
9-15s: continue toward Image3 and slow down near the kitchen island.
Room interiors should closely match the reference images; transitions between rooms may be generated smoothly.
```

Practical rule: give each room at least about 3 seconds. If there are more than 4-5 rooms, generate multiple clips and stitch them later.

## Product Video

```text
Premium product commercial, dark neutral background, the product slowly rotates 180 degrees on a matte surface, soft rim light outlines the shape, camera moves from medium shot to close-up, material texture is crisp, no extra logos or random text.
```

## People and Faces

Only use real people when the user has rights and the provider supports the required asset or authorization workflow.

Prompt tips:

- Write "same face, same hairstyle, same clothing" when identity consistency matters.
- Write "natural blinking, subtle head movement, synchronized mouth movement" for talking portraits.
- Avoid asking the model to imitate a celebrity or a private person without authorization.

## Common Mistakes

- Too many scenes for the duration.
- Conflicting camera instructions, such as "fixed camera" and "orbit around the room" in the same shot.
- Uploading references but not saying what each one should control.
- Relying on exact timestamps for complex action. Use timed sections as guidance, not frame-level control.
- Forgetting sound. One line of ambient sound often makes the result feel more real.
