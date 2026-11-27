import pygame
from src import config

class GameState:
    """Base class for all game states"""
    def __init__(self, game):
        self.game = game
        self.transition_active = False
        self.transition_type = None
        self.transition_progress = 0
        self.transition_speed = 5 
        self.transition_surface = None

        self.selected_character = None
        self.multi_selected_characters = {"Player 1": None, "Player 2": None}
        self.players_names = {"Player 1": None, "Player 2": None}
        self.enrolled_players = {}
        

    def draw(self, surface):
        """Override in subclasses"""
        pass
    
    def handle_events(self):
        """Override in subclasses"""
        pass
    
    def update(self):
        """Override in subclasses"""
        pass
    
    def run(self, surface, events):
        """Main run method that calls all other methods"""
        self.handle_events()
        self.update()
        self.draw(surface)
        if self.transition_active:
            self.handle_transition(surface)
    

    def start_transition(self, transition_type="fade"):
        """Start a transition effect"""
        self.transition_active = True
        self.transition_type = transition_type
        self.transition_progress = 0 
        self.transition_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.transition_surface.set_alpha(0)
    

    def handle_transition(self, surface):
        """Handle transition effects"""
        if self.transition_type == "fade":
            self.handle_fade_transition(surface)
        elif self.transition_type == "slide_left":
            self.handle_slide_transition(surface, "left")
        elif self.transition_type == "slide_right":
            self.handle_slide_transition(surface, "right")
        elif self.transition_type == "slide_up":
            self.handle_slide_transition(surface, "up")
        elif self.transition_type == "slide_down":
            self.handle_slide_transition(surface, "down")
    

    def handle_fade_transition(self, surface):
        """Handle fade transition"""
        self.transition_progress += self.transition_speed
        if self.transition_progress <= 100:

            alpha = int((self.transition_progress / 100) * 255)

            if self.transition_surface is not None:
                self.transition_surface.set_alpha(alpha)
                self.transition_surface.fill((0, 0, 0))
                surface.blit(self.transition_surface, (0, 0))

        elif self.transition_progress <= 200:
            if self.transition_progress == 105:  
                self.game.state_manager.update()
    
            alpha = int(((200 - self.transition_progress) / 100) * 255)
            if self.transition_surface is not None:

                self.transition_surface.set_alpha(alpha)
                self.transition_surface.fill((0, 0, 0))
            surface.blit(self.transition_surface, (0, 0))
        else:
            self.transition_active = False
    

    def handle_slide_transition(self, surface, direction):
        """Handle slide transition"""
        self.transition_progress += self.transition_speed
        
        max_offset = config.SCREEN_WIDTH if direction in ["left", "right"] else config.SCREEN_HEIGHT
        
        if self.transition_progress <= 100:
           
            if direction == "left":
                offset = -int((self.transition_progress / 100) * max_offset)
                surface.scroll(offset, 0)
            elif direction == "right":
                offset = int((self.transition_progress / 100) * max_offset)
                surface.scroll(offset, 0)
            elif direction == "up":
                offset = -int((self.transition_progress / 100) * max_offset)
                surface.scroll(0, offset)
            elif direction == "down":
                offset = int((self.transition_progress / 100) * max_offset)
                surface.scroll(0, offset)

        elif self.transition_progress <= 200:
            if self.transition_progress == 105:  
                self.game.state_manager.update()
        
            progress = (self.transition_progress - 100) / 100
            if direction == "left":
                offset = int((1 - progress) * max_offset)
                surface.scroll(offset, 0)
            elif direction == "right":
                offset = -int((1 - progress) * max_offset)
                surface.scroll(offset, 0)
            elif direction == "up":
                offset = int((1 - progress) * max_offset)
                surface.scroll(0, offset)
            elif direction == "down":
                offset = -int((1 - progress) * max_offset)
                surface.scroll(0, offset)
        else:
            self.transition_active = False
