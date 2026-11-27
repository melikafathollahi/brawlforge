import pygame
from src.engine.sprite_sheet import SpriteSheet 

class Animation:
    def __init__(self, sprite_config, frame_duration):
        """
        frames_or_config: either list of image paths OR sprite config dict
        frame_duration: milliseconds per frame
        """
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.state = "playing"
        
        self.frames = self.load_sprite_sheet_frames(sprite_config)
        self.masks = [pygame.mask.from_surface(frame) for frame in self.frames]


    def load_sprite_sheet_frames(self, config):
        """Load frames from a sprite sheet configuration"""
        frames = []
        sprite_sheet = SpriteSheet(config["path"])     
        frames = sprite_sheet.get_frames(
            frame_width = config["width"],
            frame_height = config["height"],
            num_frames = config["frames"]
        )
        return frames
    

    def update(self):
        """Update animation frame"""
        if self.state == "playing":
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_duration:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.last_update = now


    def is_finished(self):
        """Check if animation has completed one full cycle
        Return true if we're on the last frame AND enough time has passed"""
        now = pygame.time.get_ticks()
        return (self.current_frame == len(self.frames) - 1 and 
                now - self.last_update > self.frame_duration)
    

    def get_image(self):
        """Get current animation frame"""
        return self.frames[self.current_frame]
    
    
    def get_mask(self):
        """Get current frame's collision mask"""
        return self.masks[self.current_frame]


    def reset(self):
        """Reset animation to beginning"""
        self.current_frame = 0
        self.state = "playing"
        self.last_update = pygame.time.get_ticks()
