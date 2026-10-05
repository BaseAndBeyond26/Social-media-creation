#!/usr/bin/env python3
"""Transcribe a video/audio file locally with faster-whisper -> word-level JSON.

Output matches the ElevenLabs Scribe shape the cutting tools expect:
  { text, language_code, audio_duration_secs, words: [{text, start, end, type}] }
where type is "word" or "spacing". Nothing leaves this machine.

Usage:
  python3 scripts/transcribe-local-whisper.py <input> [--output path]
      [--model small.en|medium.en|large-v3] [--language en]

Setup: pip install faster-whisper  (models download on first use)
"""
import argparse
import json
import os
import sys
import time

# Nudges Whisper to keep fillers and restarts instead of tidying them away,
# so cut-mistakes can see them.
FILLER_PROMPT = "Um, uh, so, like, I mean, you know, I- I think, hmm."


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("--output", "-o")
    p.add_argument("--model", default="small.en")
    p.add_argument("--language", default="en")
    p.add_argument("--no-filler-prompt", action="store_true")
    a = p.parse_args()

    if not os.path.isfile(a.input):
        sys.exit(f"input not found: {a.input}")
    out = a.output or os.path.splitext(a.input)[0] + ".json"

    from faster_whisper import WhisperModel

    t0 = time.time()
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        a.input,
        language=a.language,
        word_timestamps=True,
        vad_filter=False,  # keep real pause timing for cut-silences
        condition_on_previous_text=False,
        initial_prompt=None if a.no_filler_prompt else FILLER_PROMPT,
    )

    words = []
    for seg in segments:
        for w in seg.words or []:
            text = w.word.strip()
            if not text:
                continue
            if words:
                words.append({"text": " ", "start": words[-1]["end"], "end": round(w.start, 3), "type": "spacing"})
            words.append({
                "text": text,
                "start": round(w.start, 3),
                "end": round(w.end, 3),
                "type": "word",
                "logprob": round(w.probability, 4),
            })

    doc = {
        "language_code": info.language,
        "language_probability": round(info.language_probability, 4),
        "text": "".join(w["text"] for w in words),
        "audio_duration_secs": round(info.duration, 3),
        "transcriber": f"faster-whisper/{a.model}",
        "words": words,
    }
    with open(out, "w") as f:
        json.dump(doc, f, indent=2)

    n = sum(1 for w in words if w["type"] == "word")
    print(f"ok {time.time() - t0:.1f}s | {n} words | {info.duration:.1f}s audio | {out}")


if __name__ == "__main__":
    main()
