#!/usr/bin/env python3
"""
Koori Notes — record a call or on-site quote conversation, get structured job notes.

You record on your phone (Voice Memos, or any recorder), AirDrop/save the audio to
your Mac, then run this on the file. It:
  1. Transcribes the audio LOCALLY (openai-whisper on your Mac — private, no upload,
     no per-minute cost; good for client conversations).
  2. An LLM turns the transcript into a structured Koori site-visit / quote note
     (scope, measurements, PC items, budget, timeline, client asks, Brad's next actions),
     built around the pricing-waterfall inputs so it feeds straight into a quote.
  3. Writes a markdown note next to the audio (and prints it). Nothing is sent.

USAGE
  pip3 install openai-whisper anthropic          # + `brew install ffmpeg` (one-time)
  export ANTHROPIC_API_KEY="<your key>"
  python3 koori_notes.py "/path/to/recording.m4a"
  python3 koori_notes.py "/path/to/recording.m4a" --type call   # phone call vs quote

Notes:
- Whisper model defaults to "small" (good accuracy, runs on Apple Silicon in ~real time).
  Use --model base for faster/rougher, --model medium for best.
- NSW: you may record a private conversation you're a party to for your own use; get
  consent before sharing it around.
- Saving the note into the job's OneNote/SharePoint folder needs Graph write access
  (same token as koori_admin.py) — v1 writes a local .md you can drop in.
"""

import os
import sys
import argparse
from datetime import datetime

QUOTE_TEMPLATE = """You are Brad Robinson's estimator assistant at Koori Constructions
(100% Aboriginal-owned NSW builder). Turn this transcript of an ON-SITE QUOTE / site
visit into a structured note Brad can quote from. Use ONLY what's in the transcript —
never invent numbers; write [not captured] where something's missing. Markdown:

# Site Visit / Quote Note — {date}
**Client:** …  **Address / suburb:** …  **Contact:** …
**Job type:** (bathroom / kitchen / deck / pergola / extension / other)
## Scope discussed
- (room-by-room / element-by-element, bullet each item)
## Measurements & quantities captured
- …
## PC items & selections (client choices, allowances)
- …
## Site conditions / access / risks (asbestos? stairs? parking? existing damage?)
- …
## Budget & timeline signals
- Budget: …  Start: …  Decision timeframe: …
## Client concerns / promises made
- …
## Brad's next actions (owner + when)
- [ ] …
## Quote flags (waterfall)
- Residential/commercial? margin note; anything needing a subbie/supplier quote (>$500);
  HBCF if >$20k; travel loading if >45min from Jilliby."""

CALL_TEMPLATE = """You are Brad Robinson's assistant at Koori Constructions. Turn this
PHONE CALL transcript into a short structured note. Use only what's said. Markdown:

# Call Note — {date}
**With:** …  **Re (job/topic):** …
## Key points
- …
## Decisions / agreements
- …
## Actions (owner + when)
- [ ] …
## Follow-up needed
- …"""


def transcribe(path: str, model_name: str) -> str:
    try:
        import whisper
    except ImportError:
        sys.exit("Install transcription: pip3 install openai-whisper  (and: brew install ffmpeg)")
    if not os.path.exists(path):
        sys.exit(f"Audio file not found: {path}")
    print(f"Transcribing ({model_name}) — this runs locally, give it a moment...")
    model = whisper.load_model(model_name)
    result = model.transcribe(path)
    return result["text"].strip()


def structure(transcript: str, kind: str, anthropic_key: str) -> str:
    import anthropic
    tmpl = CALL_TEMPLATE if kind == "call" else QUOTE_TEMPLATE
    system = tmpl.replace("{date}", datetime.now().strftime("%d %b %Y"))
    client = anthropic.Anthropic(api_key=anthropic_key)
    msg = client.messages.create(
        model="claude-sonnet-5", max_tokens=1500, system=system,
        messages=[{"role": "user", "content": f"Transcript:\n\n{transcript}"}])
    return msg.content[0].text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio", help="path to the recording (.m4a/.mp3/.wav)")
    ap.add_argument("--type", choices=["quote", "call"], default="quote")
    ap.add_argument("--model", default="small", help="whisper model: base/small/medium")
    args = ap.parse_args()

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("Set ANTHROPIC_API_KEY.")

    transcript = transcribe(args.audio, args.model)
    note = structure(transcript, args.type, key)

    out = os.path.splitext(args.audio)[0] + "-note.md"
    with open(out, "w") as f:
        f.write(note + "\n\n---\n## Full transcript\n" + transcript + "\n")
    print("\n" + note)
    print(f"\n✓ Saved: {out}  (drop into the job's OneNote/SharePoint folder)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
