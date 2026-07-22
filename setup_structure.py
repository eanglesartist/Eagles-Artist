import os

folders = [
    ".streamlit", "assets/thumbnails", "assets/icons", "assets/fonts", "assets/backgrounds",
    "css", "components", "models", "services", "workflows", "templates/prompts", 
    "templates/storyboards", "utils", "database", "uploads/images", "uploads/videos", 
    "uploads/audio", "uploads/references", "outputs/renders", "outputs/previews", 
    "outputs/exports", "outputs/thumbnails", "outputs/cache", "tests", "docs"
]

files = {
    "": ["app.py", "requirements.txt", "README.md", "LICENSE", ".gitignore", ".env.example"],
    ".streamlit": ["config.toml", "secrets.toml"],
    "css": ["app.css", "sidebar.css", "timeline.css", "editor.css", "buttons.css", "dialogs.css", "responsive.css"],
    "components": ["__init__.py", "ai_director.py", "prompt_builder.py", "storyboard.py", "timeline.py", "preview_canvas.py", "video_extend.py", "image_reference.py", "audio_reference.py", "camera_panel.py", "lighting_panel.py", "character_panel.py", "motion_panel.py", "export_panel.py", "settings.py", "top_toolbar.py", "left_sidebar.py", "right_sidebar.py", "project_manager.py", "asset_browser.py", "history_panel.py", "render_queue.py", "notifications.py", "footer.py"],
    "models": ["__init__.py", "movie_generator.py", "music_video_generator.py", "shortfilm_generator.py", "image_to_video.py", "text_to_video.py", "video_extend_engine.py", "storyboard_engine.py", "prompt_enhancer.py", "scene_planner.py", "character_memory.py", "camera_motion.py", "cinematic_styles.py", "subtitle_generator.py", "audio_sync.py", "upscale.py"],
    "services": ["__init__.py", "openai_service.py", "veo_service.py", "runway_service.py", "kling_service.py", "pika_service.py", "luma_service.py", "stability_service.py", "upload_service.py", "download_service.py", "storage_service.py", "auth_service.py"],
    "workflows": ["__init__.py", "movie_workflow.py", "mv_workflow.py", "shortfilm_workflow.py", "extend_workflow.py", "render_workflow.py", "export_workflow.py"],
    "templates/prompts": ["movie.txt", "music_video.txt", "shortfilm.txt", "extend.txt", "cinematic.txt", "anime.txt", "documentary.txt", "horror.txt", "fantasy.txt", "cyberpunk.txt"],
    "templates/storyboards": ["trailer.json", "music_video.json", "movie.json"],
    "utils": ["__init__.py", "config.py", "constants.py", "session.py", "cache.py", "file_manager.py", "image_utils.py", "video_utils.py", "audio_utils.py", "prompt_utils.py", "validators.py", "logger.py"],
    "database": ["__init__.py", "database.py", "projects.py", "renders.py", "history.py", "users.py", "assets.py"],
    "tests": ["test_prompt.py", "test_video.py", "test_storyboard.py", "test_extend.py", "test_export.py"],
    "docs": ["API.md", "DEPLOYMENT.md", "WORKFLOW.md", "CHANGELOG.md", "ARCHITECTURE.md"]
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    # Create .keep file for empty media directories so Git tracks them
    if "uploads" in folder or "outputs" in folder or "assets" in folder:
        open(os.path.join(folder, ".keep"), 'a').close()

# Create files
for folder, filenames in files.items():
    for filename in filenames:
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            open(filepath, 'a').close()

print("✅ Professional Architecture Generated Successfully!")