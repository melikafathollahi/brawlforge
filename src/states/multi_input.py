import pygame
from src import config
from src import utils
from src.engine.button import Button
from src.states.game_state import GameState

class NameInput(GameState):
    def __init__(self, game, mode = "offline"):
        super().__init__(game)
        self.mode = mode

        self.background = utils.load_image(config.MULTI_PLAYER_INPUT_BACKGROUND)
        self.background = pygame.transform.smoothscale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

        self.user_text = ''
        self.players_names = {}
        self.current_player = "Player 1"
        self.input_box = utils.load_image(config.MULTI_PLAYER_INPUT_BOX)
        self.input_box = pygame.transform.smoothscale(self.input_box, (498, 330))

        self.input_rect = Button(495, 330, 280, 40, config.INPUT_RECT)
        self.input_active = False
        self.active_input_rect = utils.load_image(config.INPUT_SELECTED_RECT) 
        self.active_input_rect = pygame.transform.smoothscale(self.active_input_rect, (283, 43))

        title_font = pygame.font.Font(config.FONT_PATH, 80)
        self.title_text = title_font.render("Input Names", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH // 2, 100))

        self.input_font = pygame.font.Font(config.ENTER_NAME_FONT, 40)
        self.command_text = self.input_font.render("Enter Your Name:", True, (255, 255, 255))
        self.command_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH // 2 + 30, 270))

        self.player_font = pygame.font.Font(config.ENTER_NAME_FONT, 24)
        self.current_player_text = self.player_font.render(f"{self.current_player}", True, (255, 255, 255))
        self.current_player_rect= self.current_player_text.get_rect(center=(config.SCREEN_WIDTH // 2, 295))

        self.PLAYER_COUNTER = 1000
        self.ID_created = False

        self.OK_button = Button(590 , 400, 77, 35, config.OK_BUTTON)
        self.back_button = Button(
            50, config.SCREEN_HEIGHT - 120,
            200, 70,
            config.BACK_BUTTON_IMAGE,
        )

        self.play_button = Button(
            config.SCREEN_WIDTH//2 - 80, config.SCREEN_HEIGHT - 127,
            140, 37,
            config.PLAY_BUTTON,
            )


    def name_input(self, events):
        if not self.input_active:
            return
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    self.user_text += event.unicode 


    def handle_offline_events(self):
        if self.current_player =="Player 1":
            self.players_names["Player 1"] = self.user_text
            self.current_player = "Player 2"
            self.current_player_text = self.player_font.render(f"{self.current_player}", True, (255, 255, 255))
            self.user_text =''

        elif self.current_player == "Player 2":
            self.players_names["Player 2"] = self.user_text
            self.game.state_manager.change_state("multi_game")
            self.start_transition("fade")


    def handle_online_events(self):
        self.PLAYER_COUNTER +=1
        player_id = self.PLAYER_COUNTER
        self.enrolled_players[self.user_text] = player_id
        self.ID_created = True

        self.player_id_text = self.player_font.render(f"Your Player ID: {player_id}", True, (255, 255, 255))
        self.player_id_rect = self.player_id_text.get_rect(center=(config.SCREEN_WIDTH // 2 - 8, 468))


    def handle_events(self):
        if self.OK_button.handle_events():
            if self.mode == "offline":
                self.handle_offline_events()
            elif self.mode == "online":
                self.handle_online_events()

        if self.input_rect.handle_events():
            self.input_active = True
        
        if self.play_button.handle_events():
            self.game.state_manager.change_state("game_type")

        if self.back_button.handle_events():
            from src.states.character_selection import CharacterSelection
            if self.mode == "offline":
                self.game.state_manager.register_state(
                    "character_selection", CharacterSelection(self.game, mode="multi"))
                self.game.state_manager.change_state("character_selection")
            
            elif self.mode =="online":
                self.game.state_manager.register_state(
                    "character_selection", CharacterSelection(self.game, mode="online"))
                self.game.state_manager.change_state("character_selection")


    def draw(self, surface):
        surface.blit(self.background, self.background.get_rect())
        surface.blit(self.title_text, self.title_rect)
        surface.blit(self.input_box, self.input_box.get_rect(center=(config.SCREEN_WIDTH // 2, 350)))
        surface.blit(self.command_text, self.command_rect)

        if self.mode =="offline":
            surface.blit(self.current_player_text, self.current_player_rect)
        if self.ID_created:
            surface.blit(self.player_id_text, self.player_id_rect)
            self.play_button.draw(surface)

        self.OK_button.draw(surface)
        self.input_rect.draw(surface)
        self.back_button.draw(surface)

        if self.input_active:
            surface.blit(self.active_input_rect, self.active_input_rect.get_rect(center=(config.SCREEN_WIDTH // 2 - 5, 347)))

        name_font = pygame.font.Font(config.NAME_FONT, 30)
        text_surface = name_font.render(self.user_text, True, (0, 0, 0))
        surface.blit(text_surface, (config.SCREEN_WIDTH // 2 - 50, 339))


    def run(self, surface, events):
        super().run(surface, events)
        self.name_input(events)
