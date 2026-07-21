# 🦅 EagleArtistAI Studio (v2 — Streamlit)

A multipage Streamlit rebuild of the AI Video Editor prototype, restructured
for growth: pluggable AI providers, a rule-based prompt engine, and a real
Project → Scene timeline data model.

## Structure

```
app.py                 Landing page / dashboard shortcut, sets page config
pages/                 Streamlit auto-routed multipage app
  1_Dashboard.py        New Video, My Projects, Credits, Templates
  2_AI_Video_Studio.py  Canvas + Timeline + upgraded AI panel (the original UI)
  3_Music_Generator.py  Standalone AI music tool
  4_Image_Generator.py  Standalone AI image tool
  5_Project_Manager.py  List/open/create projects
  6_Settings.py          Provider key status + credits
components/             Reusable Streamlit UI pieces (header, canvas, timeline,
                        ai_panel, sidebar, voice_panel, caption_panel, export_panel)
ai_engine/              Prompt expansion, scene splitting, camera motion,
                        clip extension, style presets
api/                    Provider registry + per-category dispatch
                        (video/image/voice/music), each pluggable per-provider
database/               timeline_model.py (Project/Scene dataclasses) +
                        db.py (SQLite persistence: users.db, projects.db, credits.db)
storage/                videos/, images/, audio/, thumbnails/
assets/                 logo.png, templates/
```

## Run it

```bash
git clone https://github.com/<your-username>/EagleArtistAI.git
cd EagleArtistAI
cp .env.example .env        # fill in real API keys as you wire providers up
pip install -r requirements.txt
streamlit run app.py
```

Streamlit auto-discovers everything in `pages/` as navigation — no router
config needed. `state.py` holds the session's active project/scene in
`st.session_state`, backed by the dataclasses in `database/timeline_model.py`.

## AI Video Panel (upgraded)

```
Create Video
├── Text → Video
├── Image → Video
├── Story → Video
├── Character Video
└── Product Video

Edit Video
├── Change Style      (ai_engine/style_engine.py)
├── Change Camera     (ai_engine/camera_motion.py)
├── Remove Object
└── Replace Scene

Extend
├── Continue Scene    (ai_engine/video_extend.py)
├── Add Action
└── Add Ending
```

## Prompt Engine

`ai_engine/prompt_builder.py::expand_prompt()` turns a short prompt into a
detailed, production-ready one:

```python
>>> expand_prompt("attack goat")
"A mountain goat running aggressively through snowy mountains, cinematic
 wildlife documentary, drone camera, slow motion, 8 seconds, 4K, natural
 lighting"
```

This is a rule-based stand-in — swap it for an LLM call via
`api/openai_api.py::expand_prompt_with_llm()` once `OPENAI_API_KEY` is set.

## Timeline data model

```
Project
 |
 ├── Scene 1
 │    ├── Video    (assets.video_url)
 │    ├── Voice    (assets.voice_url)
 │    ├── Music    (assets.music_url)
 │    └── Caption  (assets.caption_text)
 |
 ├── Scene 2
 |
 └── Export        (resolution, format, download_url)
```

Defined in `database/timeline_model.py`; `database/db.py` persists a summary
to SQLite (`projects.db`, `users.db`, `credits.db`).

## AI providers

All four categories are registered in `api/providers.py` with `enabled: False`
stubs. Set the matching key in `.env` and flip `enabled=True` once a provider
is actually wired into its `api/*_api.py` module:

| Category | Providers |
|---|---|
| AI Video | Google Veo, OpenAI Video, Runway, Kling AI, Pika |
| AI Image | OpenAI Image, Midjourney, Flux |
| Voice | OpenAI Voice, ElevenLabs, Google Voice |
| Music | Suno, Udio, AI Music API |

Check `pages/6_Settings.py` for a live status table of which keys are found.

## Branding

Header now reads **🦅 EagleArtistAI Studio**, with a Credits pill, Projects,
Templates, Play, and Share actions (`components/header.py`).

## Next step (as recommended)

This Streamlit build is the fast prototyping surface. The natural next step
is porting `components/` → React components and `api/` → Express routes,
using the same shape — that mapping is already close to 1:1, which is what
makes the earlier `EagleArtistAI` React/Node scaffold a straightforward
target once you're ready to go full SaaS.
