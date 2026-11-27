import pygame
from src import config
import math
from src.engine.enemies.base import Enemy

class BombChaser(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="bomb_chaser")

        self.is_exploding = False
        self.is_charging = False
        self.is_running = False
        
        self.charge_end_time = 0
        self.explosion_end_time = 0        

        self.distance_to_player = 0
        self.charge_distance = 150
        self.last_player_pos = None

        self.walk_speed = config.BOMB_CHASER_SPEED * 0.7
        self.run_speed = config.BOMB_CHASER_SPEED
        self.charge_speed = config.BOMB_CHASER_SPEED * 1.


    def get_distance_to_player(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        return math.hypot(dx, dy)


    def determine_state(self, player):        
        self.distance_to_player = self.get_distance_to_player(player)
        
        if self.distance_to_player < self.charge_distance:
            if not self.is_charging:
                self.is_charging = True
        
        if self.last_player_pos :
            moved = abs(player.rect.centerx - self.last_player_pos[0]) > 5
            if moved and self.distance_to_player > 100:
                self.is_running = True
            self.is_walking = True
        

    def update_animation_state(self):
        next_state = "idle"  
        
        if self.is_dead:
            next_state = "dead"
        elif self.is_hurt:
            next_state = "hurt"
        elif self.is_exploding:
            next_state = "explosion"
        elif self.is_walking:
            next_state = "walk"
        elif self.is_charging:
            next_state = "charge"
        elif self.is_running:
            next_state = "run"

        self.change_animation_state(next_state)
 

    def handle_timers(self):
        super().handle_timers()
        now = pygame.time.get_ticks()
        if self.explosion_end_time and now > self.explosion_end_time:
            self.is_exploding = False
            self.explosion_end_time = 0
            self.is_dead = True

        if self.charge_end_time and now > self.charge_end_time:
            self.is_charging = False
            self.charge_end_time = 0


    def move(self, player):
        if self.is_exploding or self.is_hurt or self.is_dead:
            return
        
        speed_map = {
           "run": self.run_speed ,
           "walk" : self.walk_speed ,
           "charge": self.charge_speed ,
        }
        current_speed = speed_map.get(self.current_state, 0)
        self.direction[0] = 1 if player.rect.centerx > self.rect.centerx else -1

        if current_speed > 0:
            self.rect.x += current_speed * self.direction[0]

        self.last_player_pos = (player.rect.centerx, player.rect.centery)


    def explode(self, player):
        if self.is_exploding:
            return
        if player.rect.colliderect(self.rect):
            self.is_exploding = True
            player.take_damage(config.BOMB_CHASER_DAMAGE)
            self.explosion_end_time = pygame.time.get_ticks() + 1400


    def update(self, tiles, player):
        super().update(tiles, player)
        self.determine_state(player)
        self.handle_timers()
        self.update_animation_state()
        self.explode(player)
        self.move(player)

    
    def draw(self, surface, scroll_x, scroll_y):
        super().draw(surface, scroll_x, scroll_y)
