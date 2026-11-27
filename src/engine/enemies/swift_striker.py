import pygame
from src import config
from src.engine.enemies.base import Enemy
from src.engine import Animation, BulletHandler, AnimationConfig

# needs refactoring
class SwiftStriker(Enemy):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, "swift_striker")
        
        self.speed = config.SWIFT_STRIKER_SPEED
        self.shoot_delay = config.SWIFT_STRIKER_SHOOT_DELAY
        self.bullet_speed = config.SWIFT_STRIKER_BULLET_SPEED
        self.last_shot_time = 0

        self.bullet_handler = BulletHandler()
        self.current_attack = None

        self.load_animations()

    def load_animations(self):
        configs = AnimationConfig.get_enemy_sprite_configs("swift_striker")
        validated = AnimationConfig.validate_sprite_configs(configs)

        for state, paths in validated.items():
            duration = 100 if "attack" in state else 120
            anim_state = "attack_1" if state == "attack" else state
            self.animations[anim_state] = Animation(paths, duration)

        self.current_animation = self.animations.get("idle")
        if self.current_animation:
            self.current_frame = 0
            self.animation_timer = pygame.time.get_ticks()

    def move(self, player):
        if self.is_dead or self.is_hurt:
            return

        self.direction[0] = 1 if player.rect.centerx > self.rect.centerx else -1
        self.rect.x += int(self.direction[0] * self.speed)


    def shoot(self, player):
        """SwiftStriker shoots rapidly at the player"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            striker_pos = pygame.Vector2(self.rect.centerx, self.rect.centery)
            player_pos = pygame.Vector2(player.rect.centerx, player.rect.centery)
            velocity = player_pos - striker_pos
            if velocity.length() > 0:
                velocity.scale_to_length(self.bullet_speed)
                self.bullet_handler.fire(self.rect.centerx, self.rect.centery, velocity, bullet_type='swift_striker')
                self.last_shot_time = current_time


    def update_animation_state(self):
        if self.is_dead:
            state = "dead"
        elif self.is_hurt:
            state = "hurt"
        elif self.is_attacking and self.current_attack:
            state = self.current_attack
        else:
            state = "move" if self.is_walking else "idle"

        self.change_animation_state(state)

    def update(self, tiles, player):
        super().update(tiles, player)

        if not self.active:
            return

        distance = ((player.rect.centerx - self.rect.centerx) ** 2 +
                    (player.rect.centery - self.rect.centery) ** 2) ** 0.5

        if not self.is_attacking or (self.current_animation and self.current_animation.is_finished()):
            self.is_attacking = True
            attack_num = (pygame.time.get_ticks() % 4) + 1
            self.current_attack = f"attack_{attack_num}"

        if self.current_animation and self.current_animation.is_finished():
            self.is_attacking = False

        if not self.is_attacking and not self.is_dead and not self.is_hurt:
            self.move(player)

        self.shoot(player)
        self.bullet_handler.update([], player)
        self.update_animation_state()

    def draw(self, surface, scroll_x, scroll_y):
        if not self.active:
            return

        super().draw(surface, scroll_x, scroll_y)
        self.bullet_handler.draw(surface, scroll_x, scroll_y)