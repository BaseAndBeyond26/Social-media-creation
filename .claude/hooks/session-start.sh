#!/bin/bash
# Cloud-session setup for the HyperFrames student kit:
# npm deps, FFmpeg 7+, local Whisper (faster-whisper + model), render browser.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

npm install --no-audit --no-fund

# The cutting tools pass `-/filter_complex`, which needs FFmpeg 7 or newer.
ff_major=$(ffmpeg -version 2>/dev/null | head -1 | sed -E 's/^ffmpeg version n?([0-9]+).*/\1/' || echo 0)
if ! [[ "$ff_major" =~ ^[0-9]+$ ]] || [ "$ff_major" -lt 7 ]; then
  tmp=$(mktemp -d)
  curl -sSfL https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar xJ -C "$tmp"
  cp "$tmp"/ffmpeg-*-static/ffmpeg "$tmp"/ffmpeg-*-static/ffprobe /usr/local/bin/
  rm -rf "$tmp"
fi

python3 -c "import faster_whisper" 2>/dev/null || pip install --quiet faster-whisper
python3 -c "from faster_whisper import WhisperModel; WhisperModel('medium.en', device='cpu', compute_type='int8')"

npx hyperframes browser ensure
