"""
timeline_model.py
------------------
Data model for a Project's timeline:

Project
 |
 ├── Scene 1
 │    ├── Video
 │    ├── Voice
 │    ├── Music
 │    └── Caption
 |
 ├── Scene 2
 |
 └── Export

Kept as plain dataclasses so it works with st.session_state without a
DB round-trip; database/db.py persists these to SQLite on save.
"""
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class SceneAssets:
    video_url: str | None = None
    voice_url: str | None = None
    music_url: str | None = None
    caption_text: str | None = None


@dataclass
class Scene:
    id: str = field(default_factory=lambda: f"scene-{uuid.uuid4().hex[:8]}")
    prompt: str = ""
    expanded_prompt: str = ""
    duration_seconds: int = 8
    assets: SceneAssets = field(default_factory=SceneAssets)
    camera_motion: str | None = None
    style: str | None = None


@dataclass
class ExportSettings:
    resolution: str = "1080p"
    format: str = "MP4"
    download_url: str | None = None


@dataclass
class Project:
    id: str = field(default_factory=lambda: f"proj-{uuid.uuid4().hex[:8]}")
    title: str = "Untitled video"
    owner_email: str | None = None
    scenes: list[Scene] = field(default_factory=list)
    export: ExportSettings = field(default_factory=ExportSettings)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def add_scene(self, prompt: str, expanded_prompt: str = "") -> Scene:
        scene = Scene(prompt=prompt, expanded_prompt=expanded_prompt or prompt)
        self.scenes.append(scene)
        return scene

    def total_duration(self) -> int:
        return sum(s.duration_seconds for s in self.scenes)
