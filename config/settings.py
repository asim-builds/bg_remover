import os
from pathlib import Path

# Application Configuration
APP_TITLE = "Background Remover Pro"
WINDOW_SIZE = "1000x800"
APPEARANCE_MODE = "Dark"
COLOR_THEME = "dark-blue"

# Default processing settings
DEFAULT_SETTINGS = {
    "smooth_edges": 0,      # No smoothing by default (cleaner results)
    "resize_percent": 100,  # Keep original size
    "upscale_factor": 1     # No upscaling by default
}

# File handling
SUPPORTED_FORMATS = ["PNG", "JPEG", "WEBP"]
DEFAULT_FORMAT = "PNG"
INPUT_FILETYPES = [("Image files", "*.png *.jpg *.jpeg")]
DEFAULT_OUTPUT_DIR = str(Path.home() / "Desktop" / "output_images")

# UI Configuration
PREVIEW_FRAME_HEIGHT = 300
THUMBNAIL_SIZE = (140, 140)
CONTAINER_SIZE = {"width": 160, "height": 180}

# Slider configurations
SLIDER_CONFIGS = {
    "smooth_edges": {
        "label": "Smooth Edges",
        "from_": 0,
        "to": 5,
        "tooltip": "Smooths out jagged edges after removing background.\n0 = No smoothing (recommended)\n2 = Light smoothing\n5 = Heavy smoothing"
    },
    "resize_percent": {
        "label": "Resize Image (%)",
        "from_": 10,
        "to": 200,
        "tooltip": "Scales the final image size.\n100 = Original size (recommended)\n150 = 1.5× bigger\n50 = Half size"
    },
    "upscale_factor": {
        "label": "Upscale Factor",
        "from_": 1,
        "to": 4,
        "tooltip": "Uses AI to enhance resolution.\n1 = No upscaling (recommended)\n2 = Double resolution\n4 = Quadruple resolution"
    }
}

# Tooltip texts
TOOLTIP_TEXTS = {
    "format_info": "Choose the output file format.\nPNG keeps transparency, JPEG doesn't.",
    "default_settings": "Uses optimal settings for background removal:\n• No smoothing (cleaner edges)\n• Original size maintained\n• No upscaling\n• Format selection remains independent"
}