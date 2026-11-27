import pygame
from src import config
from src.engine.button import Button
from src.states.game_state import GameState
from src import utils 

class PauseState(GameState):
    def __init__(self, game, previous_state):
        super().__init__(game)
        self.previous_state = previous_state

        self.previous_state_name = previous_state.__class__.__name__.replace('State', '')
        
        # Store the current music position and set volume to 0 instead of pausing
        self.music_pos = pygame.mixer.music.get_pos()
        pygame.mixer.music.set_volume(0.0)

        self.background = utils.load_image(config.PAUSE_BACKGROUND)
        self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

        font = pygame.font.Font(config.FONT_PATH, 80)
        self.title_text = font.render("Game Paused", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH//2, 70))
        
        button_width = 400
        button_height = 100
        center_x = config.SCREEN_WIDTH // 2 - button_width // 2
        start_y = config.SCREEN_HEIGHT // 2 - 50
        
        self.resume_button = Button(
            center_x, start_y,
            button_width, button_height,
            config.RESUME_BUTTON_IMAGE,
            "",
            font_size=48,
            text_color=config.DIJON_YELLOW,
            elevation=8,
        )
        
        self.quit_button = Button(
            center_x, start_y + button_height + 50,
            button_width, button_height,
            config.WIN_MENU_BUTTON,
            "",
            font_size=48,
            text_color=config.DIJON_YELLOW,
            elevation=8,
        )


    def handle_events(self):
        if self.resume_button.handle_events():
            self.game.state_manager.change_state(self.previous_state)
            pygame.mixer.music.set_volume(1.0)
            # Switch back to the previous state using its name
            self.game.state_manager.change_state(self.previous_state_name)

        elif self.quit_button.handle_events():
            pygame.mixer.music.stop()
            self.game.state_manager.change_state("select_mode")


    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.title_text, self.title_rect)
        self.resume_button.draw(surface)
        self.quit_button.draw(surface)