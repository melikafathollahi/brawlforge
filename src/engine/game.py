import sys
import pygame
from src import config
from src.states import StateManager, LoadingScreen, SelectMode, SelectMap, SelectNetworking
from src.states import GameType, MatchMaking, WaitingRoom, SearchID, CountDown
from src.states.multiplayer_game import MultiPlayerGame
from src.engine.c import GameClient

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Brawlforge")
        self.clock = pygame.time.Clock()

        #self.client = GameClient()

        self.state_manager = StateManager(self)
        self.state_manager.register_state("loading_screen", LoadingScreen(self))
        self.state_manager.register_state("select_networking", SelectNetworking(self))
        self.state_manager.register_state("select_mode", SelectMode(self))
        self.state_manager.register_state("select_map", SelectMap(self))
        self.state_manager.register_state("game_type", GameType(self))
        self.state_manager.register_state("match_making", MatchMaking(self))
        self.state_manager.register_state("search_id", SearchID(self))
        self.state_manager.register_state("waiting_room", WaitingRoom(self))
        #self.state_manager.register_state("multi_game", MultiPlayerGame(self))

        self.state_manager.set_state("loading_screen")

        # Game data storage for passing between states
        self.selected_character = None
        self.character_data = None  
        self.selected_map = None


        self.running = True
        self.pressed_keys = None


    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            self.pressed_keys = pygame.key.get_pressed()
            
            # Handle state changes
            if self.state_manager.next_state_name:
                self.state_manager.set_state(self.state_manager.next_state_name)
                self.state_manager.next_state_name = None

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # get server messages


            self.handle_events()
            self.state_manager.update()
            self.state_manager.run(self.screen, events)
            
            pygame.display.update()
            self.clock.tick(config.FPS)
          

    def handle_events(self):
        pass
    
