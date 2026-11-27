import pygame
from src import config, utils
from src.states.game_state import GameState
from src.engine.button import Button

class GameType(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.background = utils.load_image(config.SELECT_MODE_BACKGROUND)
        self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        font = pygame.font.Font(config.FONT_PATH, 80)
        self.title_text = font.render("Choose Game Type", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH//2, 150))

        button_width = 400
        button_height = 100
        button_spacing = 50
        center_x = config.SCREEN_WIDTH // 2 - button_width // 2
        start_y = config.SCREEN_HEIGHT // 2 - 50

        self.one_by_one_button = Button(
            center_x, start_y,
            button_width, button_height,
            config.BUTTON_IMAGE,
            "1 vs 1",
            font_size= 54,
            text_color = config.DIJON_YELLOW,
            elevation=8,
            image_highlighted_path=config.BUTTON_HIGHLIGHT_IMAGE
        )
        
        self.two_by_two_button = Button(
            center_x, start_y + button_height + button_spacing,
            button_width, button_height,
            config.BUTTON_IMAGE,
            "2 vs 2",
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
        if self.one_by_one_button.handle_events():
            self.game.state_manager.change_state("match_making")
            pass # store this selection somewhere send it to client

        elif self.two_by_two_button.handle_events():
            self.game.state_manager.change_state("match_making")
            pass

    
    def draw(self, surface):
        utils.draw(surface, self.background, self.background.get_rect())
        utils.draw(surface, self.title_text, self.title_rect)
        self.one_by_one_button.draw(surface)
        self.two_by_two_button.draw(surface)
        self.back_button.draw(surface)


class MatchMaking(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.background = utils.load_image(config.SELECT_MODE_BACKGROUND)
        self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        font = pygame.font.Font(config.FONT_PATH, 80)
        self.title_text = font.render("Find Opponents", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH//2, 150))

        button_width = 400
        button_height = 100
        button_spacing = 50
        center_x = config.SCREEN_WIDTH // 2 - button_width // 2
        start_y = config.SCREEN_HEIGHT // 2 - 50

        self.search_button = Button(
            center_x, start_y,
            button_width, button_height,
            config.BUTTON_IMAGE,
            "Search Player ID",
            font_size= 54,
            text_color = config.DIJON_YELLOW,
            elevation=8,
            image_highlighted_path=config.BUTTON_HIGHLIGHT_IMAGE
        )
        
        self.waiting_button = Button(
            center_x, start_y + button_height + button_spacing,
            button_width, button_height,
            config.BUTTON_IMAGE,
            "Join Waiting Room",
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
        if self.search_button.handle_events():
            self.game.state_manager.change_state("search_id")
        
        elif self.waiting_button.handle_events():
            self.game.state_manager.change_state("waiting_room")

        elif self.back_button.handle_events():
            self.game.state_manager.change_state("game_type")


    def draw(self, surface):
        utils.draw(surface, self.background, self.background.get_rect())
        utils.draw(surface, self.title_text, self.title_rect)
        self.search_button.draw(surface)
        self.waiting_button.draw(surface)
        self.back_button.draw(surface)


class SearchID(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.background = utils.load_image(config.SEARCH_BG)
        self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

        font = pygame.font.Font(config.FONT_PATH, 80)
        self.title_text = font.render("Search ID", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH//2, 80))

        self.input_font = pygame.font.Font(config.ENTER_NAME_FONT, 60)
        self.command_text = self.input_font.render("Enter Player ID:", True, (128, 128, 128))
        self.command_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH // 2 - 50, 310))

        self.user_text = ''
        self.input_rect = pygame.Rect(392, 390, 522, 60)
        self.active_input_img = utils.load_image(config.INPUT_SELECTED_RECT) 
        self.active_input_img = pygame.transform.smoothscale(self.active_input_img, (545, 76))
        self.input_active = False

        self.result_msg = ''
        result_font = pygame.font.Font(config.ENTER_NAME_FONT, 40)
        self.result_text = result_font.render(self.result_msg, True, (255, 255, 255))
        self.result_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH // 2 - 50, 500))

        self.retry_button = Button(600, 550, 77, 35, config.RETRY_BUTTON)
        self.OK_button = Button(600, 550, 77, 35, config.OK_BUTTON)
        self.back_button = Button(
            50, config.SCREEN_HEIGHT - 120,
            200, 70,
            config.BACK_BUTTON_IMAGE,
        )


    def ID_input(self, events):
        if not self.input_active:
            return
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    self.user_text += event.unicode 


    def search_ID(self):
        for key in self.enrolled_players:
            if key == self.user_text.strip():
                return True
            else:
                return False
            

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        is_hovered = self.input_rect.collidepoint(mouse_pos)
        if is_hovered and mouse_pressed:
            self.input_active = True

        if self.retry_button.handle_events():
            self.user_text = ''

        if self.OK_button.handle_events():
            # send message to that player!!
            # shall i go to the waiting room? 
            # and wait till the player accept?
            pass


    def draw(self, surface):
        utils.draw(surface, self.background, self.background.get_rect())
        utils.draw(surface, self.title_text, self.title_rect)
        surface.blit(self.command_text, self.command_rect)
        self.back_button.draw(surface)

        if self.input_active:
            surface.blit(self.active_input_img, 
            self.active_input_img.get_rect(center=(660, 422)))

        id_font = pygame.font.Font(config.NAME_FONT, 50)
        text_surface = id_font.render(self.user_text, True, (0, 0, 0))
        surface.blit(text_surface, (600, 400))

        if self.search_ID():
            self.result_text = "Send Challenge"
            self.OK_button.draw(surface)
        else:
            self.result_msg = "No player found with that ID."
            self.retry_button.draw(surface)


    def run(self, surface, events):
        super().run(surface, events)
        self.ID_input(events)


class WaitingRoom(GameState):
    def __init__(self, game):
        super().__init__(game)


class CountDown(GameState):
    def __init__(self, game):
        super().__init__(game)