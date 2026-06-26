---
name: x-to-obsidian
description: Save an X/Twitter status URL, thread, or article into an Obsidian note. Use when the user pastes an x.com or twitter.com status URL, says save this tweet/thread, 收藏推文, 保存推文, or asks to archive X content into a knowledge base.
---

# X to Obsidian

Use this skill to turn an X/Twitter post or thread into a useful Obsidian note.

## Configuration

Required:

- `OBSIDIAN_VAULT`: path to the user's Obsidian vault.

Optional:

- `X_AUTH_TOKEN`: X `auth_token` cookie.
- `X_CT0`: X `ct0` cookie.

Never commit real cookies or API keys. Use environment variables or a local untracked `cookies.json`.

## Workflow

1. Extract the first `x.com/.../status/...` or `twitter.com/.../status/...` URL from the user request.
2. Fetch the post, thread, and useful replies.
3. Resolve important external links when feasible.
4. If the post links to an article, repo, video, or product page, inspect the original asset instead of saving only the repost text.
5. Select a PARA destination under the Obsidian vault.
6. Write a Markdown note with source URL, author, content, links, useful replies, and a short value analysis.
7. Report the saved note path and any extraction limits.

## Fetch Strategy

Prefer the least fragile available path:

1. Existing local fetch script, if the user has one.
2. Logged-in browser via `cdp-browser-reuse`.
3. X cookies from `X_AUTH_TOKEN` and `X_CT0`.
4. Public page fetch only when the post is fully public.

If authentication is missing or expired, ask the user to log in or provide fresh cookies. Do not ask for a password.

## Note Format

Use this structure:

```markdown
---
title: "{short title}"
tags: [X收藏]
created: YYYY-MM-DD
type: 收藏
source: "{original URL}"
author: "{display name or handle}"
---

# {short Chinese title}

> Source: {original URL}
> Author: {author}

## Original Assets

Include this section only when there is a linked video, article, repo, or product page. Summarize the original source first.

## Thread

Preserve the post or thread in readable order.

## Related Links

List resolved URLs and one-line descriptions.

## Notable Replies

Keep only replies that add new facts, corrections, examples, or strong counterpoints.

## Value

Explain why this matters to the user's work in 3-5 practical bullets.

---
*Saved from X on YYYY-MM-DD via x-to-obsidian*
```

## Classification

If the vault already has a PARA structure, choose:

- `01-Projects` for active project work.
- `02-Areas` for ongoing responsibilities.
- `03-Resources` for reusable reference material.
- `00-Inbox` when unsure.

If no structure exists, save under `00-Inbox` and say why.

## Safety

- Do not publish cookies, bearer tokens, screenshots containing private DMs, or private account data.
- If the post is deleted, protected, or unavailable, say so.
- If an external short link cannot be resolved, keep the original short URL and mark it unresolved.
