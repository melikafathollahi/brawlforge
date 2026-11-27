import pygame
import math
from src import config
from src.engine.enemies.base import Enemy
from src.engine import BulletHandler

class Sniper(Enemy):
    def __init__(self, x, y, max_distance = 300 , angle_deg = 120 , max_angle_deg = 50):
        super(). __init__(x, y, "sniper")
        self.max_distance = max_distance
        self.angle = angle_deg
        self.max_angle = max_angle_deg
        self.bullet_handler = BulletHandler()
        self.last_shot_time = 0               
        self.patrol_speed = 5

        self.is_shooting = False
        self.shooting_end_time = 0
        self.direction[0] = -1


    def can_detect_player(self, player):
        player_pos = pygame.Vector2(player.rect.center)
        sniper_pos = pygame.Vector2(self.rect.center)
        to_player = pygame.Vector2(player_pos) - sniper_pos

        if to_player.length() > self.max_distance:
            return False

        sniper_direction = pygame.Vector2(math.cos(math.radians(self.angle)),
                                          -math.sin(math.radians(self.angle)))
        
        angle_diff = sniper_direction.angle_to(to_player)
        if abs(angle_diff) > self.max_angle/2:
            return False
        
        return True
    

    def update_rotation(self, player):
        player_pos = (player.rect.x, player.rect.y)
        direction = pygame.Vector2(player_pos) - pygame.Vector2(self.x, self.y)
        if direction.length() > 0:
            self.angle = -math.degrees(math.atan2(direction.y, direction.x)) 

    
    def shoot(self, player):
        current_time = pygame.time.get_ticks()
        if self.can_detect_player(player):
            if current_time - self.last_shot_time > config.SNIPER_SHOOT_DELAY:
                rad = math.radians(self.angle)
                velocity = pygame.Vector2(math.cos(rad), -math.sin(rad)) * config.SNIPER_BULLET_SPEED
                self.is_shooting = True
                self.bullet_handler.fire(self.rect.centerx, self.rect.centery, velocity, self.enemy_type)
                self.last_shot_time = current_time
                self.shooting_end_time = current_time + 300


    def handle_timers(self):
        super().handle_timers()
        now = pygame.time.get_ticks()
        if self.shooting_end_time and now > self.shooting_end_time:
            self.is_shooting = False
            self.shooting_end_time = 0


    def update_animation_state(self):
        next_state = "idle"  
        
        if self.is_dying:
            next_state = "dead"
        elif self.is_hurt:
            next_state = "hurt"
        elif self.is_shooting:
            next_state = "shot_1"
        elif self.is_walking:
            next_state = "walk"

        self.change_animation_state(next_state)
 

    def move(self, player):
        self.is_walking = False
        patrol_start = self.x - 5
        patrol_end = self.x - 550
        if not self.can_detect_player(player):
            self.rect.x += int(self.patrol_speed * self.direction[0])
            if self.rect.x >= patrol_start or self.rect.x <= patrol_end:
                self.direction[0] *=-1
            self.is_walking = True
        else:
            self.is_walking = False

   
    def update(self, tiles, player):
        super().update(tiles, player)
        self.move(player)
        self.update_rotation(player)
        self.shoot(player)
        self.bullet_handler.update(None, player)
        self.update_animation_state()
        self.handle_timers()


    def draw(self, surface, scroll_x, scroll_y):
        self.bullet_handler.draw(surface , scroll_x, scroll_y)
        super().draw(surface, scroll_x, scroll_y)



