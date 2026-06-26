---
name: media-to-obsidian
description: Convert video or audio URLs and local media files into Obsidian notes. Use for YouTube, Bilibili, X video, podcast, meeting recording, or local audio/video files when the user wants transcription, summary, and knowledge-base archiving.
---

# Media to Obsidian

Use this skill to turn a video or audio source into a searchable Obsidian note.

## Configuration

Required:

- `OBSIDIAN_VAULT`: path to the user's Obsidian vault.

Useful tools when available:

- `yt-dlp` for metadata, subtitles, and downloads.
- `ffmpeg` or `ffprobe` for media inspection.
- Local Whisper or another speech-to-text tool for transcription.
- A logged-in browser for NotebookLM or sites that need cookies.

## Workflow

1. Identify whether the input is a URL or a local media file.
2. Get metadata: title, uploader, duration, platform, upload date, and source URL.
3. Get transcript using this priority:
   - Existing subtitles from the platform.
   - NotebookLM or another user-approved cloud transcript path.
   - Local Whisper or another local speech-to-text model.
4. Clean the transcript: remove timestamps when not useful, repeated subtitle lines, and obvious OCR/ASR noise.
5. Summarize into a practical note.
6. Classify into the Obsidian vault.
7. Save the note and transcript file.
8. Report the note path, transcript path, method used, and any quality caveats.

## Commands

Metadata:

```bash
yt-dlp --dump-json --no-download "URL"
```

Subtitle check:

```bash
yt-dlp --list-subs --no-download "URL"
```

Download subtitles:

```bash
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --sub-format vtt --skip-download -o "%(title)s" "URL"
```

Download audio when transcription is needed:

```bash
yt-dlp -f "bestaudio" -o "%(title)s.%(ext)s" "URL"
```

## Note Format

```markdown
---
title: "{author}: {title}"
tags: [媒体笔记]
created: YYYY-MM-DD
type: 收藏
source: "{URL or local path}"
author: "{author}"
duration: "{duration}"
---

# {title}

> {author} | {duration} | {platform}

## Core Idea

One or two sentences.

## Key Points

Structured summary by topic.

## Useful Actions

Only include actions that are concrete and relevant.

## Mentioned Tools / Links

Include resources mentioned in the media.

## Transcript

Link to the transcript file instead of pasting a very long transcript.

---
*Transcribed on YYYY-MM-DD via {method}*
```

## Classification

If the vault has PARA folders:

- Active task or client work -> `01-Projects`
- Ongoing responsibility -> `02-Areas`
- Reusable reference -> `03-Resources`
- Unsure -> `00-Inbox`

## Safety

- Do not claim to analyze a video or audio deeply before getting a real transcript.
- Do not re-download speech models if the model is already installed.
- Do not save private meeting recordings into a public or shared vault unless the user explicitly asks.
- For sites requiring login, use `cdp-browser-reuse`; do not ask for passwords.
