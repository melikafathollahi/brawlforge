import pygame
from src import config
from src import utils
from src.states.game_state import GameState
from src.engine.button import Button
from src.states.level_state import Level1State, Level2State, Level3State, Level4State

class SelectMap(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.background = utils.load_image(config.SELECT_MAP_BACKGROUND)
        self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

        font = pygame.font.Font(config.FONT_PATH, 80)
        self.title_text = font.render("Select Map", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH // 2, 70))

        # Map data
        self.maps = {
            "Level1": {
                "name": "Forest Temple",
                "description": "A mystical forest with ancient temples",
                "preview": "src/assets/images/UI/Levels Menu/1.png" #should be replaced by the real preview!
            },
            "Level2": {
                "name": "Mountain Peak",
                "description": "High altitude combat zone",
                "preview": "src/assets/images/UI/Levels Menu/2.png"
            },
            "Level3": {
                "name": "number 3",
                "description": "map number 3",
                "preview": "src/assets/images/UI/Levels Menu/3.png"
            },
            "Level4": {
                "name": "number 4",
                "description": "map number 4",
                "preview": "src/assets/images/UI/Levels Menu/4.png"
            }
            
        }
        
        self.selected_map = None

        # Create map buttons in 2x2 grid
        self.map_buttons = {}
        button_width = 300
        button_height = 200
        horizontal_spacing = 100
        vertical_spacing = 50

        buttons_per_row = 2
        total_rows = 2

        # Calculate horizontal centering
        row_width = buttons_per_row * button_width + (buttons_per_row - 1) * horizontal_spacing
        start_x = (config.SCREEN_WIDTH - row_width) // 2
        start_y = 180

        # Place buttons
        for index, (map_id, map_data) in enumerate(self.maps.items()):
            row = index // buttons_per_row
            col = index % buttons_per_row

            x = start_x + col * (button_width + horizontal_spacing)
            y = start_y + row * (button_height + vertical_spacing)

            button = Button(
                x, y,
                button_width, button_height,
                map_data["preview"],
                font_size=32,
                text_color=config.DIJON_YELLOW,
                elevation=6
            )
            self.map_buttons[map_id] = button

        self.back_button = Button(
            50, config.SCREEN_HEIGHT - 120,
            200, 70,
            config.BACK_BUTTON_IMAGE,
            font_size=32,
            text_color=config.DIJON_YELLOW,
            elevation=6
        )

        self.start_button = Button(
            config.SCREEN_WIDTH - 250, config.SCREEN_HEIGHT - 120,
            200, 70,
            config.START_BUTTON_IMAGE,
            font_size=32,
            text_color=config.DIJON_YELLOW,
            elevation=6
        )
        
        self.description_font = pygame.font.Font(config.FONT_PATH, 24)
        self.description_text = ""
        self.description_surface = None

    def handle_events(self):
        for map_id, button in self.map_buttons.items():
            if button.handle_events():
                self.selected_map = map_id
                self.description_text = self.maps[map_id]["description"]
                self.description_surface = self.description_font.render(
                    self.description_text, True, (255, 255, 255)
                )
        
        if self.back_button.handle_events():
            self.game.state_manager.change_state("character_selection")
            #self.start_transition("slide_right")
        
        if self.selected_map and self.start_button.handle_events():
            self.game.selected_map = self.selected_map
            self.game.state_manager.change_state(f"{self.selected_map}")

    def update(self):
        pass

    def draw(self, surface):
        utils.draw(surface, self.background, self.background.get_rect())
        utils.draw(surface, self.title_text, self.title_rect)
        
        for map_id, button in self.map_buttons.items():
            if self.selected_map == map_id:         # Draw selection highlight
                highlight_rect = pygame.Rect(
                    button.original_x - 5,
                    button.original_y - 5,
                    button.width + 10,
                    button.height + 10
                )
                pygame.draw.rect(surface, config.DIJON_YELLOW, highlight_rect, 3)
            button.draw(surface)
        
        if self.description_surface and self.selected_map:
            desc_rect = self.description_surface.get_rect(center=(config.SCREEN_WIDTH//2, 405))
            utils.draw(surface, self.description_surface, desc_rect)
        
        self.back_button.draw(surface)
        if self.selected_map:
            self.start_button.draw(surface)
