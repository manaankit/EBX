"""
Configuration file for Instagram Reel Generator
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Crown Carnival Settings
    CROWN_CARNIVAL_URL = "https://crowncarnival.shop"
    
    # Video Settings
    VIDEO_WIDTH = 1080
    VIDEO_HEIGHT = 1920  # Instagram Reel dimensions
    VIDEO_FPS = 30
    VIDEO_DURATION = 15  # seconds
    
    # Output Settings
    OUTPUT_DIR = "generated_reels"
    TEMP_DIR = "temp"
    
    # Instagram Settings
    MAX_HASHTAGS = 30
    MAX_CAPTION_LENGTH = 2200
    
    # AI Generation Settings
    AI_MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 500
    TEMPERATURE = 0.7
    
    # Scraping Settings
    REQUEST_DELAY = 1  # seconds between requests
    MAX_RETRIES = 3
    TIMEOUT = 30
    
    # Product Categories
    PRODUCT_CATEGORIES = [
        "crowns",
        "tiaras", 
        "headpieces",
        "necklaces",
        "bracelets",
        "rings",
        "accessories",
        "jewelry"
    ]
    
    # Video Templates
    VIDEO_TEMPLATES = {
        "luxury": {
            "background_color": (20, 20, 40),
            "text_color": (255, 215, 0),  # Gold
            "accent_color": (255, 255, 255),  # White
            "font_size": 60
        },
        "elegant": {
            "background_color": (40, 20, 40),
            "text_color": (255, 192, 203),  # Pink
            "accent_color": (255, 255, 255),
            "font_size": 55
        },
        "modern": {
            "background_color": (10, 10, 10),
            "text_color": (0, 255, 255),  # Cyan
            "accent_color": (255, 255, 255),
            "font_size": 65
        }
    }
    
    # Trending Hashtags for Jewelry/Fashion
    TRENDING_HASHTAGS = [
        "#luxury", "#jewelry", "#crown", "#tiara", "#fashion", 
        "#style", "#elegant", "#glamour", "#accessories", "#bling",
        "#royal", "#princess", "#queen", "#wedding", "#bridal",
        "#handmade", "#unique", "#sparkle", "#diamonds", "#gold",
        "#silver", "#crystals", "#pearls", "#vintage", "#modern",
        "#instafashion", "#fashionista", "#styleinspo", "#trendy", "#chic"
    ]
    
    # Music Suggestions by Category
    MUSIC_SUGGESTIONS = {
        "crowns": ["Royal/Classical music", "Epic orchestral", "Luxury brand music"],
        "tiaras": ["Wedding music", "Romantic ballads", "Classical piano"],
        "necklaces": ["Fashion show music", "Upbeat pop", "Trendy beats"],
        "bracelets": ["Modern pop", "R&B", "Chill beats"],
        "rings": ["Love songs", "Romantic music", "Soft pop"],
        "accessories": ["Trendy pop", "Fashion music", "Upbeat tracks"]
    }

# Validation
def validate_config():
    """Validate configuration settings"""
    errors = []
    
    if not Config.OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is required")
    
    if not os.path.exists(Config.OUTPUT_DIR):
        try:
            os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create output directory: {e}")
    
    if not os.path.exists(Config.TEMP_DIR):
        try:
            os.makedirs(Config.TEMP_DIR, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create temp directory: {e}")
    
    return errors

if __name__ == "__main__":
    errors = validate_config()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Configuration is valid!")

