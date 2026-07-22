import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Media Directories
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"
ASSETS_DIR = BASE_DIR / "assets"

# Specific Output Paths
RENDERS_DIR = OUTPUTS_DIR / "renders"
PREVIEWS_DIR = OUTPUTS_DIR / "previews"
EXPORTS_DIR = OUTPUTS_DIR / "exports"

# Application Settings
SUPPORTED_VIDEO_FORMATS = [".mp4", ".mov", ".webm"]
SUPPORTED_IMAGE_FORMATS = [".png", ".jpg", ".jpeg"]