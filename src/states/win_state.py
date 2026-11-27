import pygame
from src import config
from src import utils
from src.engine.button import Button
from src.states.game_state import GameState
from src.states.level_state import Level1State, Level2State, Level3State, Level4State

class WinState(GameState):
    def set_previous_state(self, state_name):
        """Set the previous state name when transitioning to win state"""
        self.previous_state = state_name.replace('State', '')
        
    def __init__(self, game):
        super().__init__(game)
        self.previous_state = None  

        self.background = utils.load_image(config.WIN_BACKGROUND)
        self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        button_width = 200
        button_height = 70
        
        center_x = config.SCREEN_WIDTH // 2 - button_width // 2
        center_y = config.SCREEN_HEIGHT // 2 - button_height // 2

        self.next_button = Button(
            center_x, center_y,
            button_width, button_height,
            "src/assets/images/UI/Victory/NEXT_LEVEL.png",
            font_size=32,
            text_color=config.DIJON_YELLOW,
            elevation=6
        )
        
        self.quit_button = Button(
            50, config.SCREEN_HEIGHT - 120,
            button_width, button_height,
            "src/assets/images/UI/Victory/BTN MENU.png",
            font_size=32,
            text_color=config.DIJON_YELLOW,
            elevation=6
        )
        
        self.restart_button = Button(
            config.SCREEN_WIDTH - 250, config.SCREEN_HEIGHT - 120,
            button_width, button_height,
            "src/assets/images/UI/Victory/RESTART.png",
            font_size=32,
            text_color=config.DIJON_YELLOW,
            elevation=6
        )


    def handle_events(self):
        if self.restart_button.handle_events():
            if self.previous_state:
                new_state = None
                if "Level1" in self.previous_state:
                    new_state = Level1State(self.game) 
                if "Level2" in self.previous_state:
                    new_state = Level2State(self.game) 
                if "Level3" in self.previous_state:
                    new_state = Level3State(self.game) 
                if "Level4" in self.previous_state:
                    new_state = Level4State(self.game) 

                self.game.state_manager.states[self.previous_state] = new_state
                self.game.state_manager.change_state(self.previous_state)
            
        elif self.quit_button.handle_events():
            self.game.state_manager.change_state("select_mode")
            
        elif self.next_button.handle_events():

            if self.previous_state == "Level1":
                self.game.state_manager.change_state("Level2")
            elif self.previous_state == "Level2":
                self.game.state_manager.change_state("Level3")
            elif self.previous_state == "Level3":
                self.game.state_manager.change_state("Level4")
            elif self.previous_state == "Level4":
                self.game.state_manager.change_state("select_mode")

                
    def draw(self, surface):
        utils.draw(surface, self.background, self.background.get_rect())
        
        self.quit_button.draw(surface)
        self.restart_button.draw(surface)
        
        # Only show next button if not in the last level
        if self.previous_state != "Level4":
            self.next_button.draw(surface)