import pygame
from src import utils

class SpriteSheet:
    """Handle sprite sheet loading and frame extraction"""
    def __init__(self, image_path):
        self.sheet = utils.load_image(image_path)
    

    def get_frames(self, frame_width, frame_height, num_frames, start_x=0, start_y=0):
        """Extract frames from sprite sheet"""
        frames = []
        
        for i in range(num_frames):
            # Calculate frame position
            x = start_x + (i * frame_width)
            y = start_y
            
            # Create frame rectangle with specified dimensions
            frame_rect = pygame.Rect(x, y, frame_width, frame_height)
            
            # Create a surface with SRCALPHA for transparency
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA) 
            frame.blit(self.sheet, (0, 0), frame_rect)            
            frames.append(frame)

        return frames
    
    
    def get_single_frame(self, x, y, width, height):
        """Extract a single frame at specific position"""
        frame_rect = pygame.Rect(x, y, width, height)
        frame = pygame.Surface((width, height), pygame.SRCALPHA)
        frame.blit(self.sheet, (0, 0), frame_rect)
        return frame