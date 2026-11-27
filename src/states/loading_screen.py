import pygame
from src import config
from src import utils
from src.engine import Button, HealthBar
from src.states.game_state import GameState

# don't forget to uncomment the loading bar and change the next state
class LoadingScreen(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.loading_progress = 0
        self.loading_bar = HealthBar(326, 350, 300, img_path = config.LOADING_Bar, bg_path = config.LOADING_BAR_BG)
        self.background = utils.load_image(config.LOADING_SCREEN_BACKGROUND)
        self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

        self.start_button = Button(1000, 550,
                                180, 60, config.START_BUTTON_IMAGE, " ", 60
                                , config.DIJON_YELLOW, 6) 
        self.loading_icon = utils.load_image(config.LOADING_ICON)
        self.loading_icon = pygame.transform.smoothscale(self.loading_icon, (400, 96))
    

    def handle_events(self):
        if self.start_button.handle_events():
            self.game.state_manager.change_state("select_mode")  #change it later
            self.start_transition("fade")


    def update(self):
        self.loading_bar.current_value = self.loading_progress
        if self.loading_progress < 300:
            self.loading_progress += 1
        


    def draw(self, surface):
        utils.draw(surface, self.background, self.background.get_rect())
        if self.loading_bar.current_value >= 300:
            self.start_button.draw(surface)
        self.loading_bar.draw(surface)
        utils.draw(surface, self.loading_icon, (config.SCREEN_WIDTH//2 - 220, config.SCREEN_HEIGHT//2 - 85))
  

    