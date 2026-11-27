import pygame
from src import config
from src import utils
            
class Button:
    def __init__(self, x, y, width, height, image_path, text="",
                 font_size=30, text_color=(255, 255, 255),
                 elevation=6, image_highlighted_path=None):
        
        self.original_x = x
        self.original_y = y
        self.width = width
        self.height = height
        
        self.is_hovered = False
        self.is_clicked = False
        self.pressed = False
        
        self.elevation = elevation
        self.dynamic_elevation = elevation
        
        self.image = utils.load_image(image_path)
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        
        if image_highlighted_path:
            self.highlight_image = utils.load_image(image_highlighted_path)
            self.highlight_image = pygame.transform.smoothscale(self.highlight_image, (width, height))
        else:
            self.highlight_image = self.image.copy()
            shadow_overlay = pygame.Surface((width, height))
            shadow_overlay.fill((0, 0, 0))
            shadow_overlay.set_alpha(100) 
            self.highlight_image.blit(shadow_overlay, (0, 0))
        
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(config.FONT_PATH, self.font_size)
        self.text_color = text_color
        
        self.update_rects()
    
    
    def update_rects(self):
        """Update rectangle positions based on current elevation"""
        self.top_rect = pygame.Rect(
            self.original_x, 
            self.original_y - self.dynamic_elevation, 
            self.width, 
            self.height
        )
        
        self.bottom_rect = pygame.Rect(
            self.original_x,
            self.original_y - self.dynamic_elevation,
            self.width,
            self.height + self.dynamic_elevation
        )
        self.bottom_rect.midtop = self.top_rect.midtop
    

    def draw(self, screen):
        """Draw the button with elevation effect"""
        self.update_rects()
        
        if self.dynamic_elevation > 0:
            screen.blit(self.highlight_image, self.bottom_rect) 
 
        screen.blit(self.image, self.top_rect)
        
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.top_rect.center)
            screen.blit(text_surface, text_rect)
    

    def handle_events(self):
        """Handle mouse events and update button state"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        self.is_hovered = self.top_rect.collidepoint(mouse_pos)
        
        if self.is_hovered:
            self.image = pygame.transform.smoothscale(self.image, (self.width + 2, self.height + 2))
            self.font = pygame.font.Font(config.FONT_PATH, self.font_size + 4)
            if mouse_pressed:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.pressed = False
                    return True  
        else:
            self.font = pygame.font.Font(config.FONT_PATH, self.font_size)
            self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
            self.dynamic_elevation = self.elevation
            self.pressed = False
        
        return False