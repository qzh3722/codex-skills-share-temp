#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="$ROOT/skills"
CODEX_DIR="${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}"
CLAUDE_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

if [ ! -d "$SKILLS_ROOT" ]; then
  echo "Missing skills directory: $SKILLS_ROOT" >&2
  exit 1
fi

copy_skills_to() {
  local target="$1"
  mkdir -p "$target"
  for skill in "$SKILLS_ROOT"/*; do
    [ -d "$skill" ] || continue
    local name
    name="$(basename "$skill")"
    rm -rf "$target/$name"
    cp -R "$skill" "$target/$name"
    echo "Installed $name -> $target/$name"
  done
}

copy_skills_to "$CODEX_DIR"

if [ "${SKIP_CLAUDE:-0}" != "1" ]; then
  copy_skills_to "$CLAUDE_DIR"
fi

echo "Done."
