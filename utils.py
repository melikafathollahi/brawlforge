import os
import pygame
from src import config

BASE_IMG_PATH = 'src/assets/images/'
BASE_SOUND_PATH = 'src/assets/sounds/'

def load_image(path, default_size=(64,64)):
    try:
        if path == "placeholder":
            surface = pygame.Surface(default_size)
            surface.fill((225, 0, 225))
            return surface
        
        if os.path.exists(path):
            Image = pygame.image.load(path).convert_alpha()
            return Image
        else:
            surface = pygame.Surface(default_size)
            surface.fill((225, 0, 0))
            return surface
    except Exception as e:

        surface = pygame.Surface(default_size)
        surface.fill((128, 128, 128))
        return surface
       

def load_sound(path):
    try:
        sound = pygame.mixer.Sound(BASE_SOUND_PATH + path)
        return sound
    except:
        return None


def check_collision(sprite1, sprite2):
    """
    Two-step collision check:
    1. First check rect collision (fast)
    2. If rects collide and both are sprites with masks, do pixel-perfect check
    
    Handles both sprite-sprite and rect-rect collisions
    """

    rect1 = sprite1.rect if hasattr(sprite1, 'rect') else sprite1
    rect2 = sprite2.rect if hasattr(sprite2, 'rect') else sprite2
    
    if not rect1.colliderect(rect2):
        return False
    
    if hasattr(sprite1, 'mask') and hasattr(sprite2, 'mask') and \
       sprite1.mask is not None and sprite2.mask is not None:
        offset_x = rect2.x - sprite1.rect.x
        offset_y = rect2.y - sprite1.rect.y
        return sprite1.mask.overlap(sprite2.mask, (offset_x, offset_y)) is not None
    
    return True


def draw(screen, image, rect):
    screen.blit(image, rect)
    