import pygame
from src import config
from src import utils
from src.engine.enemies.base import Enemy
from src.engine import BulletHandler

class Freezer(Enemy):
    def __init__(self, x , y):
        super().__init__(x, y, enemy_type="freezer")
        self.bullet_size = (13, 13) 
        self.start = self.rect.centerx
        self.bullet_handler = BulletHandler()
        self.last_shot_time = 0


    def move(self):
        """moving freezer 500 meters forward and backward in the sky"""
        travelled = abs(self.rect.centerx - self.start)
        if travelled < 500:
            self.rect.x += int(config.FREEZER_SPEED * self.direction[0]) 
        else:
            self.direction[0] *= -1
            self.rect.x += int(config.FREEZER_SPEED * self.direction[0])


    def shoot(self, player):
        """shoot towards the player's current position"""
        freezer_pos = pygame.Vector2(self.rect.centerx, self.rect.centery)
        player_pos = pygame.Vector2(player.rect.centerx, player.rect.centery)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > config.FREEZER_SHOOT_DELAY:
            velocity = pygame.Vector2(player_pos - freezer_pos)
            if velocity.length() > 0:
                velocity.scale_to_length(config.FREEZER_BULLET_SPEED)
                self.bullet_handler.fire(self.rect.centerx, self.rect.centery, velocity, bullet_type='freezer')
                self.last_shot_time = current_time
        

    def update(self, tiles, player):
        if not self.active:
            return
        super().update(tiles, player)
        self.move()
        self.shoot(player)
        self.bullet_handler.update([], player)


    def draw(self, surface, scroll_x, scroll_y):
        if not self.active:
            return

        super().draw(surface, scroll_x, scroll_y)

        self.bullet_handler.draw(surface, scroll_x, scroll_y)