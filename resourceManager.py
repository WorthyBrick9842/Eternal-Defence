# resources.py
import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "Assets")

def asset_path(*parts):
    """Join path parts under assets/ directory."""
    print(os.path.join(ASSET_DIR, *parts))
    return os.path.join(ASSET_DIR, *parts)

def load_image(filename):
    return pygame.image.load(asset_path("images", filename))

def load_sound(filename):
    return pygame.mixer.Sound(asset_path("sounds", filename))

def load_font(filename, size):
    return pygame.font.Font(asset_path("fonts", filename), size)
