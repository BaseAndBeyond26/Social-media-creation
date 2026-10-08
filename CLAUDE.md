# HyperFrames Student Kit: workspace guide

Turn a talking-head recording into an intentional edit using local HyperFrames
rendering, transcript-driven cuts, and reusable motion graphics.

## Runtime routing

`AGENTS.md` and `CLAUDE.md` contain the same standing guide. Keep them synchronized.
Claude Code uses `.claude/skills/`. Codex uses the generated `.agents/skills/`.
Edit canonical skills in `.claude/skills/`, then run `npm run sync:skills`.
Use `$edit-video` in Codex, `/edit-video` in Claude Code, or natural language.
Model and permission choices belong to the user; `.codex/config.toml` only adds
document loading defaults. Work locally unless the user requests subagents.

## Start and route

Read `README.md` for installation and `docs/WORKFLOW.md` for a complete edit.
Use `edit-video` to coordinate transcription, cuts, design, and verification.
For one stage, load the matching local skill:

| Need | Skill |
| --- | --- |
| Reels, Shorts, and short advertisements | `short-form-edit` |
| Motion-design showreels and brand reels cut to music | `motion-showreel` |
| Existing May Shorts example maintenance | `short-form-video` |
| New motion-graphics video from a brief | `make-a-video` |
| Website-inspired compositions | `website-to-hyperframes` |
| Full raw-video edit | `edit-video` |
| Silence removal | `cut-silences` |
| Retakes, false starts, or stutters | `cut-mistakes` |
| Narrative arc, persistent world, and visual callbacks | `video-storytelling` |
| Overlay beats, paper takeovers, and glass cards | `hyperframes-video-beats` |
| Select or extend styles and templates | `style-library` |
| HTML compositions and media timing | `hyperframes` |
| Preview, lint, and rendering | `hyperframes-cli` |
| Timeline animation | `gsap` |
| Install HyperFrames catalog blocks | `hyperframes-registry` |

Before a creative session read `MOTION_PHILOSOPHY.md` and the project's DESIGN.md.
The philosophy's fast sizzle pacing is a style reference. Give educational speech
room to breathe. The project brief controls pacing, palette, and typography.
Framework skill contracts override historical code recipes in the style guide.

## Workspace

Create a project with `npm run new-video -- my-video`. Keep source media, EDLs,
transcripts, compositions, and renders together under `video-projects/<slug>/`.
Run HyperFrames from that project's directory. The root `scripts/` utilities
accept paths from the working directory. `style-library/registry.json` indexes
cards; each style has a DESIGN.md, CSS tokens, and named text slots.
See `style-templates/README.md` for whole-scene templates.

Preserve raw files. Use a new output filename for each editing stage. Archive
obsolete work. Video projects, personal footage, transcripts, credentials, and
renders are gitignored. The 12 already-published projects are retained as teaching examples; new private
projects stay ignored. Do not treat existing public examples as permission to add
new personal footage. Never print secrets or copy private media into library examples.

## Editing and timing

Before choosing a transcription, asset-generation, or voiceover service, read
`docs/TOOLS-AND-API-KEYS.md` and check the user's provider choice and local setup.
ElevenLabs Scribe is Nate's default; honor requests for OpenAI Whisper, local
Whisper, or another provider. Normalize verified word timestamps for the cutting
tools. The included transcription script is ElevenLabs-only. Kie.ai is optional
and needs a configured integration and credits. Reuse existing transcripts and
assets; make any unapproved uploads or paid calls concrete before asking.

Cut silences first; use its edited video AND retimed transcript for cut-mistakes.
Review each mistake in context. Intentional repetition is not a mistake. Record
the reviewed decisions before applying them. If no cuts are needed, preserve the
input or use an empty cuts list. Never mix original timestamps with edited footage.

Load the relevant skills before changing HTML. Root compositions use a visible
div with id, data-composition-id, data-start, duration, width, and height. Timed
elements carry data-start, data-duration, and data-track-index; same-track clips
must not overlap. Visible timed divs use class="clip"; videos do not.
Mute videos and use sibling audio for the mix. Animate a non-timed video wrapper.
Register one synchronous paused GSAP timeline per composition in window.__timelines
using its exact composition ID. Keep finite timelines and explicit durations.
HyperFrames owns media playback. Use deterministic animation and local assets.

## Verification and approvals

Run `node scripts/preflight.mjs <project>` and HyperFrames lint. For anchored
sub-compositions, run `node scripts/validate-beat-sync.mjs <project>`; each beat
needs data-anchor with an exact transcript phrase. Enter between 0.2 seconds after
and 1.8 seconds before that word. Inline timelines require manual timing review.

Review Studio before draft rendering. Review the encoded draft, extract and
inspect hero frames and transition boundaries, and listen to the audio joins.
Check cropped faces, overflow, black flashes, readable labels, clipping, and A/V
sync. Resolve problems before the final render. Save evidence in VERIFY.md.
Use a Range-capable preview server for MP4 scrubbing (for example `npx serve`).

Honor approvals already provided. When review approval is missing, prepare the
concrete preview or cut proposal first. Never claim a lint result proves visual
quality. Only publish or upload a finished video when the user authorizes it.
Automated browser checks must be headless, with Pointer Lock and cursor capture
disabled; synthetic input must remain inside the virtual browser.

For short-form edits, read `docs/SHORT-FORM.md` and use the plan and footage
validators. Structural checks supplement rendered video and audio review.

## Base & Beyond studio notes

Standing preferences learned in earlier sessions. Update this section when they change.

- Transcribe locally with `python3 scripts/transcribe-local-whisper.py <file>
  --model medium.en`; it writes the ElevenLabs-shaped JSON the cutting tools read.
  Its filler prompt can invent "um/hmm" on clips with no speech; check the audio.
- Cloud sessions run `.claude/hooks/session-start.sh` (npm ci, FFmpeg 7+,
  faster-whisper + medium.en, render browser). The cut tools need FFmpeg 7+.
- Business: Base & Beyond (@baseandbeyondltd), roof tent hire at Setmurthy,
  Bassenthwaite Lake, Lake District. Pre-launch; bookings open 25 March 2027. Read
  `.claude/product-marketing.md` (audience, offer, voice, guardrails) before any copy.
  Overnight stays: don't promote or discourage wild camping; captions advise checking
  locations, respecting no-overnight signs, and asking landowners if unsure.
  Possible future Moby Mountain reselling: say nothing until the owner confirms.
- Default deliverable is a 1080x1920 Instagram Reel with natural sound only; the owner
  adds trending audio in Instagram. Default CTA "Follow for more". Show TentBox and Moby
  branding as filmed and never imply a partnership.
- Clips without narration: tell the story with on-screen text (Anton headlines,
  Caveat script, tent orange #ff6b1f, warm white #fff8ee) in the top safe zone.
  reel-01 "Bedroom with a view" established this house style.
- Check vehicle direction in every driving shot. Footage filmed while reversing
  should be played in reverse so the car moves forward.
- Flag legible number plates and ask before publishing them.
- The send-file tool limit is 30 MiB. Send a share copy encoded at CRF 22 (about 25 MiB
  for a 30s reel) and check its size before sending; raise the CRF if it's over (reel-03,
  40s of detailed landscape, needed CRF 24 for 27.6 MB).
- Make the first frame meaningful: hook text must be visible at 0.0s.
- Check every frame of an end-card build, not just the last one: panels and boxes
  must animate in with their text. Phone footage in shade often needs a gentle lift
  (reel-02 "option B": eq gamma 1.18, brightness +0.035, saturation x1.32, warm
  colorbalance); compare clip brightness and offer a side-by-side before full renders.
- On-screen copy: avoid self-answered questions ("That box? It's...") and "No X. No Y."
  lists. Use white text over the orange tent interior (orange text disappears there).
  Brand slogan: "Rent | Roam | Return" (straight-line separators). End card (reel-02,
  owner-approved): "BASE & BEYOND" with a slightly smaller "&", the slogan, "Bookings
  opening soon.", "Follow to be the first to know". Keep end cards simple.
- On-screen timers always show real elapsed time. When cuts remove footage, the
  timer jumps forward to the true time. Mark start/stop with a clap, a spoken
  cue, a described action, or timestamps.
- Skill routing: editing footage into a reel always goes through `short-form-edit`
  (and the kit pipeline). `social`, `copywriting` and `marketing-psychology` supply
  hooks, on-screen lines, captions, hashtags and content plans that feed that edit.
- `impeccable` (pbakaus/impeccable) is for websites, landing pages and static designs
  (e.g. baseandbeyond.uk, covers, carousels) and as a critique pass on reel graphics;
  reel building stays with the kit skills. Its brand context comes from
  `.claude/product-marketing.md`; don't create a separate PRODUCT.md without asking.
  The installed copy is the repo's Claude variant (`.claude/skills/impeccable`), not
  the Codex variant `npx skills add` picks, so don't run `npx skills update` on it.
- New skills from skills.sh (via `find-skills`): read the whole SKILL.md first,
  get the owner's approval, then install project-level, never `-g`, because cloud
  machines are wiped: `npx skills add <owner/repo> --skill <name> --agent
  claude-code --copy -y`, then `npm run sync:skills` and `npm run check`.
- Style references from other accounts go into `style-library/` as new packs.
  Capture tokens, motion and copy patterns, never their media, logos or exact wording.
- Source footage lives in the owner's public Google Drive folder "Claude Edits"
  (https://drive.google.com/drive/folders/1QLv7f6Nl26BNHvXAznj2ViFlzbqzcv49).
  For a new reel use only the loose photos and videos at its top level; ignore
  subfolders (archived past reels, named by reel title) unless the owner names one.
  List it via `https://drive.google.com/embeddedfolderview?id=<id>`; download into
  the reel's project folder and keep originals untouched.
