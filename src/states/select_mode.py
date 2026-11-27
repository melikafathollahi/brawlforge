import pygame
from src import config
from src import utils
from src.engine.button import Button
from src.states.game_state import GameState
from src.states.character_selection import CharacterSelection

class SelectMode(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.background = utils.load_image(config.SELECT_MODE_BACKGROUND)
        self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        font = pygame.font.Font(config.FONT_PATH, 80)
        self.title_text = font.render("Select Game Mode", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH//2, 150))

        button_width = 400
        button_height = 100
        button_spacing = 50
        center_x = config.SCREEN_WIDTH // 2 - button_width // 2
        start_y = config.SCREEN_HEIGHT // 2 - 50
        
    
        self.single_player_button = Button(
            center_x, start_y,
            button_width, button_height,
            config.BUTTON_IMAGE,
            "Single Player",
            font_size= 54,
            text_color = config.DIJON_YELLOW,
            elevation=8,
            image_highlighted_path=config.BUTTON_HIGHLIGHT_IMAGE
        )
        
        self.multi_player_button = Button(
            center_x, start_y + button_height + button_spacing,
            button_width, button_height,
            config.BUTTON_IMAGE,
            "Multi Player",
            font_size= 54,
            text_color = config.DIJON_YELLOW,
            elevation=8,
            image_highlighted_path=config.BUTTON_HIGHLIGHT_IMAGE
        )
        
        self.back_button = Button(
            50, config.SCREEN_HEIGHT - 120,
            200, 70,
            config.BACK_BUTTON_IMAGE,
        )

    def handle_events(self):
        if self.single_player_button.handle_events():
            self.game.state_manager.register_state(

                "character_selection", CharacterSelection(self.game, mode="single"))
            self.game.state_manager.change_state("character_selection")

        elif self.multi_player_button.handle_events():
            self.game.state_manager.change_state("select_networking")

        elif self.back_button.handle_events():
            self.game.state_manager.change_state("loading_screen")
    
    
    def draw(self, surface):
        utils.draw(surface, self.background, self.background.get_rect())
        utils.draw(surface, self.title_text, self.title_rect)

        self.single_player_button.draw(surface)
        self.multi_player_button.draw(surface)

        self.back_button.draw(surface)


class SelectNetworking(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.background = utils.load_image(config.SELECT_MODE_BACKGROUND)
        self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        font = pygame.font.Font(config.FONT_PATH, 80)
        self.title_text = font.render("Select Multiplayer Mode", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH//2, 150))

        button_width = 400
        button_height = 100
        button_spacing = 50
        center_x = config.SCREEN_WIDTH // 2 - button_width // 2
        start_y = config.SCREEN_HEIGHT // 2 - 50

        self.offline_button = Button(
            center_x, start_y,
            button_width, button_height,
            config.BUTTON_IMAGE,
            "Offline",
            font_size= 54,
            text_color = config.DIJON_YELLOW,
            elevation=8,
            image_highlighted_path=config.BUTTON_HIGHLIGHT_IMAGE
        )
        
        self.online_button = Button(
            center_x, start_y + button_height + button_spacing,
            button_width, button_height,
            config.BUTTON_IMAGE,
            "Online",
            font_size= 54,
            text_color = config.DIJON_YELLOW,
            elevation=8,
            image_highlighted_path=config.BUTTON_HIGHLIGHT_IMAGE
        )

        self.back_button = Button(
            50, config.SCREEN_HEIGHT - 120,
            200, 70,
            config.BACK_BUTTON_IMAGE,
        )


    def handle_events(self):
        if self.offline_button.handle_events():
            self.game.state_manager.register_state(
                "character_selection", CharacterSelection(self.game, mode="multi"))
            self.game.state_manager.change_state("character_selection")

        elif self.online_button.handle_events():
            self.game.state_manager.register_state(
                "character_selection", CharacterSelection(self.game, mode="online"))
            self.game.state_manager.change_state("character_selection")

        elif self.back_button.handle_events():
            self.game.state_manager.change_state("select_mode")


    def draw(self, surface):
        utils.draw(surface, self.background, self.background.get_rect())
        utils.draw(surface, self.title_text, self.title_rect)

        self.offline_button.draw(surface)
        self.online_button.draw(surface)

        self.back_button.draw(surface)