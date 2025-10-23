# resources.py
import os
import pygame

#get the absolute mathto the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# add on the path from the file to the assets folder
ASSET_DIR = os.path.join(BASE_DIR, "Assets")

def asset_path(*parts):
    #join all parts of the path together
    """Join path parts under assets/ directory."""
    return os.path.join(ASSET_DIR, *parts)

def load_image(filename):
    #get the path to the file in images using asset_path
    return pygame.image.load(asset_path("images", filename))














def load_sound(filename):
    return pygame.mixer.Sound(asset_path("sounds", filename))

def load_font(filename, size):
    return pygame.font.Font(asset_path("fonts", filename), size)
