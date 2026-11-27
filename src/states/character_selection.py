import pygame
from src import config
from src import utils
from src.engine import Button, Animation
from src.states.level_state import Level1State, Level2State, Level3State, Level4State
from src.states.game_state import GameState
from src.states.win_state import WinState
from src.states.game_over import GameOverState
from src.states.multi_input import NameInput
class CharacterSelection(GameState):
    def __init__(self, game, mode):
        super().__init__(game)
        self.mode = mode
        self.current_player = "Player 1" if mode == "multi" else None

        self.background = utils.load_image(config.SELECT_PLAYER_BACKGROUND)
        self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        title_text = f"{self.current_player} Select Character" if mode=="multi" else "Select Character"
        font = pygame.font.Font(config.FONT_PATH, 80)
        self.title_text = font.render(title_text, True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH//2, 80))
        
        self.characters = {
            "Kitsune": {
                "name": "Kitsune",
                "portrait": "src/assets/images/UI/Character_menu/Kitsune.png",
                "button": "src/assets/images/UI/Character_menu/Kitsune_button.png",
                "description": "A mystical fox spirit with fire abilities"
            },
            "Magican": {
                "name": "Magican",
                "portrait": "src/assets/images/UI/Character_menu/Magican.png",
                "button": "src/assets/images/UI/Character_menu/Magican_button.png",
                "description": "A powerful mage who wields arcane magic"
            },
            "Kunoichi": {
                "name": "Kunoichi", 
                "portrait": "src/assets/images/UI/Character_menu/Kunoichi.png",
                "button": "src/assets/images/UI/Character_menu/Kunoichi_button.png",
                "description": "A skilled ninja warrior with stealth abilities"
            }
        }
        

        if mode in ("single", "online"):
            self.selected_character = None
        else: 
            self.selected_characters = {
                "Player 1": None,
                "Player 2": None
            }
            self.selected_character = None

        self.character_buttons = {}
        self.character_portraits = {}
        self.character_animations = {}
        self.character_rects = {}
        
        character_width = 200
        character_height = 250
        spacing = 100
        total_width = len(self.characters) * character_width + (len(self.characters) - 1) * spacing
        start_x = (config.SCREEN_WIDTH - total_width) // 2
        character_y = 200
        
        x_offset = start_x
        for char_id, char_data in self.characters.items():
            portrait = utils.load_image(char_data["portrait"])
            portrait = pygame.transform.scale(portrait, (character_width, character_height - 80))
            self.character_portraits[char_id] = portrait
            
            button = Button(
                x_offset, character_y + character_height - 70,
                character_width, 60,
                char_data["button"],
                font_size=32,
                text_color=config.DIJON_YELLOW,
                elevation=6
            )
            self.character_buttons[char_id] = button
            
            try:
                char_path = char_id.lower()
                idle_animation = Animation({
                        "path": f"src/assets/images/player/{char_path}/idle_menu.png",
                        "width": 128,
                        "height": 128,
                        "frames": 8  
                }, frame_duration=120)
                self.character_animations[char_id] = idle_animation
            except:
                self.character_animations[char_id] = None

            anim_rect = pygame.Rect(x_offset, character_y, character_width, character_height)
            self.character_rects[char_id] = anim_rect
            
            x_offset += character_width + spacing
        

        self.back_button = Button(
            50, config.SCREEN_HEIGHT - 120,
            200, 70,
            config.BACK_BUTTON_IMAGE,
            font_size=32,
            text_color=config.DIJON_YELLOW,
            elevation=6
        )
        
        self.continue_button = Button(
            config.SCREEN_WIDTH - 250, config.SCREEN_HEIGHT - 120,
            200, 70,
            config.CONTINUE_BUTTON_IMAGE,
            font_size=32,
            text_color=config.DIJON_YELLOW,
            elevation=6
        )
        
        self.description_font = pygame.font.Font(config.FONT_PATH, 24)
        self.description_text = ""
        self.description_surface = None
        
        
    def handle_multi_events(self):
        if self.current_player == "Player 1" and self.selected_character:
            self.selected_characters["Player 1"] = self.selected_character.lower()
            self.current_player = "Player 2"
            self.selected_character = None
            self.title_text = pygame.font.Font(config.FONT_PATH, 80).render(
                f"{self.current_player} Select Character", True, (255, 255, 255)
            )
        elif self.current_player == "Player 2" and self.selected_character:
            self.selected_characters["Player 2"] = self.selected_character.lower()

            self.game.multi_selected_characters = self.selected_characters.copy()
            self.game.state_manager.register_state("multi_input", NameInput(self.game))
            self.game.state_manager.change_state("multi_input")


    def handle_single_events(self):
        if self.selected_character:
            self.game.selected_character = self.selected_character.lower()
            
            self.game.state_manager.register_state("Level1", Level1State(self.game))
            self.game.state_manager.register_state("Level2", Level2State(self.game))
            self.game.state_manager.register_state("Level3", Level3State(self.game))
            self.game.state_manager.register_state("Level4", Level4State(self.game))
            self.game.state_manager.register_state("win_state", WinState(self.game))
            self.game.state_manager.register_state("game_over", GameOverState(self.game))

            self.game.state_manager.change_state("select_map")


    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if self.mode == "multi":
            for char_id, rect in self.character_rects.items():
                if rect.collidepoint(mouse_pos) and mouse_pressed:
                    self.selected_character = char_id
        else:
            for char_id, button in self.character_buttons.items():
                if button.handle_events():
                    self.selected_character = char_id
                    self.description_text = self.characters[char_id]["description"]
                    self.description_surface = self.description_font.render(
                        self.description_text, True, (255, 255, 255)
                    )
        
        if self.back_button.handle_events():
            if self.mode == "online":
                self.game.state_manager.change_state("select_networking")
            else:
                self.game.state_manager.change_state("select_mode")
        
        if self.selected_character and self.continue_button.handle_events():
            if self.mode == "single":
                self.handle_single_events()

            elif self.mode == "multi":
                self.handle_multi_events()

            elif self.mode == "online":
                self.game.selected_character = self.selected_character.lower()
                self.game.state_manager.register_state("multi_input", NameInput(self.game, mode="online"))
                self.game.state_manager.change_state("multi_input")
    

    def update(self):
        if self.mode =="multi":
            for animation in self.character_animations.values():
                if animation:
                    animation.update()

    
    def draw(self, surface):
        surface.blit(self.background, self.background.get_rect())
        surface.blit(self.title_text, self.title_rect)
        
        if self.mode in ("single", "online"):
            self.draw_single_ui(surface)
        elif self.mode =="multi":
            self.draw_multi_ui(surface)

        self.back_button.draw(surface)
        if self.selected_character:
            self.continue_button.draw(surface)


    def draw_single_ui(self, surface):
        x_offset = (config.SCREEN_WIDTH - (len(self.characters) * 300 + (len(self.characters) - 1) * 100)) // 2
        for char_id, char_data in self.characters.items():
    
            portrait_rect = pygame.Rect(x_offset + 150, 200, 200, 200)
            utils.draw(surface, self.character_portraits[char_id], portrait_rect)
             
            if self.selected_character == char_id:  
                highlight_rect = pygame.Rect(x_offset + 145, 195, 210, 180)
                pygame.draw.rect(surface, config.DIJON_YELLOW, highlight_rect, 3)
            
            self.character_buttons[char_id].draw(surface)
            
            x_offset += 300
        
        if self.description_surface and self.selected_character:
            desc_rect = self.description_surface.get_rect(center=(config.SCREEN_WIDTH//2, 500))
            utils.draw(surface, self.description_surface, desc_rect)
    

    def draw_multi_ui(self, surface):
        for char_id, anim in self.character_animations.items():
            if not anim:
                continue
            
            image = anim.get_image()
            rect = self.character_rects[char_id].copy()

            if self.selected_character == char_id:
                scale_factor = 1.2
                new_size = (int(rect.width * scale_factor), int(rect.height * scale_factor))
                image = pygame.transform.smoothscale(image, new_size)
                rect = image.get_rect(center=rect.center)
            
            surface.blit(image, rect.topleft)

