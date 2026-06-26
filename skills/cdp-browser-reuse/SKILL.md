---
name: cdp-browser-reuse
description: Reuse an already logged-in Chrome browser through Chrome DevTools Protocol (CDP). Use when Codex needs to operate logged-in websites, avoid re-login, avoid restarting Chrome with --remote-debugging-port, or inspect browser cookies/session state.
---

# CDP Browser Reuse

Use this skill when a task needs a logged-in website. The goal is simple: connect to an existing browser session instead of creating a fresh browser that has no login state.

## Rules

- Do not close or restart the user's browser unless the user explicitly asks.
- Do not ask for passwords or one-time codes.
- Prefer a browser/profile that is already logged in to the target site.
- Verify login state with cookies or a real session endpoint when possible. Do not trust page text alone.
- If no logged-in session exists, stop and ask the user to log in manually in the opened browser.

## Find a CDP Port

Common debug ports are `9222`, `9223`, and app-specific ports. Check them before scanning a wider range.

Python example:

```python
import json
import urllib.request

def get_tabs(port: int):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=2) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return []

def find_port_for(domain: str, ports=(9222, 9223, 9224, 9333, 9334, 9335, 9337)):
    for port in ports:
        tabs = get_tabs(port)
        if any(domain in (t.get("url") or "") for t in tabs):
            return port
    return None
```

PowerShell quick check:

```powershell
1..10 | ForEach-Object {
  $port = 9221 + $_
  try {
    $tabs = Invoke-RestMethod "http://127.0.0.1:$port/json/list" -TimeoutSec 1
    if ($tabs) { "$port`t$($tabs[0].url)" }
  } catch {}
}
```

## Connect with Playwright

Python:

```python
from playwright.sync_api import sync_playwright

port = 9222
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
    context = browser.contexts[0]
    page = next((p for p in context.pages if "example.com" in p.url), context.pages[0])
    page.bring_to_front()
    page.goto("https://example.com", wait_until="domcontentloaded")
    # Do the task here.
    browser.close()  # closes the CDP connection, not the user's Chrome process
```

Node:

```js
const { chromium } = require("playwright");

const browser = await chromium.connectOverCDP("http://127.0.0.1:9222");
const context = browser.contexts()[0];
const pages = context.pages();
const page = pages.find(p => p.url().includes("example.com")) || pages[0];
await page.bringToFront();
```

## Verify Session

Cookie checks are more reliable than scanning page text:

```python
cookies = context.cookies(["https://x.com"])
names = {c["name"] for c in cookies}
if {"auth_token", "ct0"}.issubset(names):
    print("X auth cookies are present")
```

For ChatGPT-like sites, use a real session endpoint if available:

```python
email = page.evaluate("""async () => {
  const r = await fetch('/api/auth/session', {credentials: 'include'});
  const j = await r.json();
  return j?.user?.email || null;
}""")
```

## When CDP Is Not Available

1. Use the Browser or Chrome tool if Codex exposes one.
2. Open the target site and ask the user to complete login manually.
3. Continue after the user confirms the site is logged in.

## Do Not

- Do not run `taskkill /F /IM chrome.exe` or kill all browser processes.
- Do not copy a whole browser profile between machines.
- Do not commit exported cookies.
- Do not use page text such as "Sign in" as the only login check.
