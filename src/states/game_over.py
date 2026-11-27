import sys
import pygame
from src import config
from src import utils
from src.engine.button import Button
from src.states.game_state import GameState
from src.states.level_state import Level1State, Level2State, Level3State, Level4State

class GameOverState(GameState):
    LEVEL_STATE_CLASSES = {
        "Level1": Level1State,
        "Level2": Level2State,
        "Level3": Level3State,
        "Level4": Level4State,
    }

    def __init__(self, game):
        super().__init__(game)
        self.previous_state = None

        self.background = utils.load_image(config.GAME_OVER_BACKGROUND)
        self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        self.game_over_back = utils.load_image(config.BUTTON_IMAGE)
        self.game_over_back = pygame.transform.smoothscale(self.game_over_back, (600, 144))

        font = pygame.font.Font(config.FONT_PATH, 90)
        self.title_text = font.render("Game Over", True, config.DIJON_YELLOW)
        self.title_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH//2, 280))
        
        button_width, button_height = 200, 70

        self.retry_button = Button(
            50, config.SCREEN_HEIGHT - 120,
            button_width, button_height,
            config.WIN_MENU_BUTTON,
            font_size=48,
            text_color=config.DIJON_YELLOW,
            elevation=8,
        )
        
        self.quit_button = Button(
            config.SCREEN_WIDTH - 250, config.SCREEN_HEIGHT - 120,
            button_width, button_height,
            config.BUTTON_IMAGE ,
            "Quit",
            font_size=48,
            text_color=config.DIJON_YELLOW,
            elevation=8,
        )


    def set_previous_state(self, state_name):
        if state_name and isinstance(state_name, str):
            self.previous_state = state_name.replace('State', '')


    def handle_events(self):
        if self.retry_button.handle_events():
            self.retry_previous_level()

        if self.quit_button.handle_events():   
            pygame.quit()
            sys.exit()

            
    def retry_previous_level(self):
        state_name = self.previous_state
        if state_name in self.LEVEL_STATE_CLASSES:
            # Replace with a fresh instance
            new_state = self.LEVEL_STATE_CLASSES[state_name](self.game)
            self.game.state_manager.states[state_name] = new_state
            self.game.state_manager.change_state(state_name)
            self.previous_state = None
        elif state_name:
            # State name not recognized, fallback to character selection
            print(f"Warning: Unrecognized state '{state_name}', falling back to character_selection.")
            self.game.state_manager.change_state("character_selection")
        else:
            # No previous state, fallback
            self.game.state_manager.change_state("character_selection")


    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.game_over_back, (config.SCREEN_WIDTH//2 - 300, config.SCREEN_HEIGHT//2 - 135))
        surface.blit(self.title_text, self.title_rect)
        
        self.retry_button.draw(surface)
        self.quit_button.draw(surface)