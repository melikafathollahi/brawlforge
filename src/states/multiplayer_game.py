import pygame
from src import config
from src import utils
from src.engine.powerup import PowerUp
from src.states.game_state import GameState
from src.engine.player import Player

class MultiPlayerGame(GameState):
    def __init__(self,game, p1_name, p2_name, p1_char, p2_char):
        super().__init__(game)
        self.player1 = Player(x=1100, y=400, character="kitsune")
        self.player2 = Player(x=100, y=400, character="kunoichi")

        self.player1.name = p1_name
        self.player2.name = p2_name

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.state_manager.change_state("pause", previous_state = "multiplayer")



    def update(self):
        keys = pygame.key.get_pressed()

        # WASD + SPACE for player1 (Kitsune)
        player1_keys = {
            pygame.K_a: keys[pygame.K_a],
            pygame.K_d: keys[pygame.K_d],
            pygame.K_w: keys[pygame.K_w],
            pygame.K_s: keys[pygame.K_s],
            pygame.K_SPACE: keys[pygame.K_SPACE]
        }

        # Arrow keys + RSHIFT for player2 (Kunoichi)
        player2_keys = {
            pygame.K_LEFT: keys[pygame.K_LEFT],
            pygame.K_RIGHT: keys[pygame.K_RIGHT],
            pygame.K_UP: keys[pygame.K_UP],
            pygame.K_DOWN: keys[pygame.K_DOWN],
            pygame.K_RSHIFT: keys[pygame.K_RSHIFT]
        }
        self.player1.update(player1_keys, self.collision_tiles)
        self.player2.update(player2_keys, self.platforms, None, None)
        self.player1.bullet_handler.update(self.platforms, [], self.player2)
        self.player2.bullet_handler.update(self.platforms, [], self.player1)
        self.check_collisions()
        if self.player1.is_dead or self.player2.is_dead:
            self.game.state_manager.change_state("game_over")

    def draw(self, surface):
        self.player1.draw(surface)
        self.player2.draw(surface)
        self.player1.bullet_handler.draw(surface)
        self.player2.bullet_handler.draw(surface)
        self.player1.healthbar.draw(surface)
        self.player2.healthbar.draw(surface)

    def check_collisions(self):
        for bullet in self.player2.bullet_handler.bullets:
            if self.player1.rect.colliderect(bullet.rect):
                self.player1.take_damage(bullet.damage)
                bullet.kill()