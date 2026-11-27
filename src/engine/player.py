import pygame
from src import config
from src import utils
from src.engine import Animation, AnimationConfig, BulletHandler, Entity
class Player(Entity): 
    def __init__(self, x, y, character="kitsune", character_data=None):
        super().__init__(
            x, y,
            config.PLAYER_WIDTH, config.PLAYER_HEIGHT, 
            config.PLAYER_HEALTH_WIDTH, config.PLAYER_HEALTH_HEIGHT
        )
        
        self.max_health = 300
        self.character = character
        self.character_data = character_data

        self.rect = pygame.Rect(x, y, config.PLAYER_WIDTH - 40, config.PLAYER_HEIGHT- 8)

        self.current_health = 100
        self.last_health = self.current_health

        self.jump_count = 0
        self.jump_cooldown = 0
        self.jump_cooldown_time = 6
        self.on_ground = False

        self.is_frozen = False
        self.shield_active = False
        self.can_double_jump = False

        self.bullet_handler = BulletHandler()
        self.last_shot_time = 0
        self.base_damage = config.PLAYER_DAMAGE
        self.damage = self.base_damage

        self.frozen_end_time = 0
        self.damage_end_time = 0
        self.double_jump_end_time = 0
        self.shield_end_time = 0

        self.load_animations()

    def __getitem__(self, key):
        """Allow Player to be accessed like a dict."""
        if key == "id":
            return getattr(self, "id", None)
        elif key == "username":
            return getattr(self, "username", None)
        elif key == "team":
            return getattr(self, "team", None)
        elif key == "position":
            return (self.rect.x, self.rect.y)
        elif key == "health":
            return getattr(self, "current_health", None)
        elif key == "alive":
            return not getattr(self, "is_dead", False)
        else:
             raise KeyError(f"{key} not found in Player")

    
    def load_animations(self):
        """Load player animations"""
        self.character = self.character.lower() if self.character else "kitsune"
        sprite_configs = AnimationConfig.get_player_sprite_configs(self.character)
        validated_configs = AnimationConfig.validate_sprite_configs(sprite_configs)
        
        self.animations = {}
        for state, cfg in validated_configs.items():
            frame_duration = 80 if state == "attack" else 105 if state in ["walk", "run"] else 120
            self.animations[state] = Animation(cfg, frame_duration)

        self.current_animation = self.animations.get("idle")


    def move_left(self):
        if self.is_frozen:
            return
        self.velocity_x -= config.PLAYER_SPEED
        self.direction = (-1, 1)
        self.is_walking = True

    def move_right(self):
        if self.is_frozen:
            return
        self.velocity_x += config.PLAYER_SPEED
        self.direction = (1, 1)
        self.is_walking = True

    def reset_movement_state(self):
        self.is_walking = False
        self.velocity_x = 0


    def draw(self, surface, scroll_x, scroll_y):
        if not self.is_dead:  
            super().draw(surface, scroll_x, scroll_y)

            self.bullet_handler.draw(surface, scroll_x, scroll_y)

            if self.shield_active:
                radius = max(self.rect.width, self.rect.height) // 2
                shield_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                pygame.draw.circle(shield_surface, (0, 100,255, 100), (radius, radius), radius)
                shield_pos = (self.rect.centerx - radius - scroll_x, self.rect.centery - radius - scroll_y)
                surface.blit(shield_surface, shield_pos)         
        else:
            self.kill()
    

    def update_animation_state(self):
        next_state = "idle"  
        
        if self.is_dying:
            next_state = "death"
        elif self.is_hurt:
            next_state = "hurt"
        elif self.is_attacking:
            next_state = "attack"
        elif not self.on_ground:
            next_state = "jump"
        elif self.is_walking:
            next_state = "walk"
  
        self.change_animation_state(next_state)


    def update(self, tiles):
        """Main update method"""
        super().update(tiles)  
        self.update_animation_state()
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1


    def apply_powerup(self, powerup):
        powerup.apply_to(self)
        now = pygame.time.get_ticks()
        duration = powerup.DURATION[powerup.kind]

        if powerup.kind == "boost_damage":
            self.damage_end_time = now + duration
        elif powerup.kind == "double_jump":
            self.double_jump_end_time = now + duration
        elif powerup.kind == "shield":
            self.shield_end_time = now + duration


    def handle_timers(self):
        super().handle_timers()

        now = pygame.time.get_ticks()

        if self.damage_end_time and now > self.damage_end_time:
            self.damage -= config.POWERUP_DAMAGE_BOOST
            self.damage_end_time = 0  

        if self.double_jump_end_time and now > self.double_jump_end_time:
            self.can_double_jump = False
            self.double_jump_end_time = 0

        if self.shield_end_time and now > self.shield_end_time:
            self.shield_active = False
            self.shield_end_time = 0

        if self.is_frozen and now > self.frozen_end_time:
            self.is_frozen = False
            self.frozen_end_time = 0


    def jump(self, tiles):
        if self.is_frozen or self.jump_cooldown > 0:
            return
        max_jumps = 2 if self.can_double_jump else 1
        if self.jump_count < max_jumps:
            self.velocity_y = -config.PLAYER_JUMP_HEIGHT
            self.on_ground = False
            self.jump_count += 1
            self.is_jumping = True
            self.jump_cooldown = self.jump_cooldown_time
            self.apply_gravity()
            self.check_tile_collisions(tiles)
                

    def shoot(self):
        if self.is_frozen:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > config.PLAYER_SHOOT_COOLDOWN:
            self.is_attacking = True
            velocity = pygame.Vector2(self.direction[0], 0) * config.PLAYER_BULLET_SPEED
            self.bullet_handler.fire(self.rect.centerx, self.rect.centery - 10, velocity )
            self.last_shot_time = current_time
            self.attack_end_time = current_time + 600


    def freeze(self):
        self.is_frozen = True
        self.frozen_end_time = pygame.time.get_ticks() + config.FREEZE_DURATION
        self.velocity_x = 0
        self.velocity_y = 0
    

    def check_other_collisions(self, enemies, powerups):
        from src.utils import check_collision
        now = pygame.time.get_ticks()
        self.last_damage_time = 0
        for enemy in enemies:
            if check_collision(self, enemy):
                if self.rect.left >= enemy.rect.right and self.old_rect.right <= enemy.rect.left:
                    self.rect.right = enemy.rect.left
                    self.x = self.rect.x 

                if now - self.last_damage_time > config.ENEMY_DAMAGE_COOLDOWN:
                    if not self.shield_active:
                        self.take_damage(config.ENEMY_DAMAGE)
                    self.last_damage_time = now

                if self.rect.right <= enemy.rect.left and self.old_rect.left >= enemy.rect.right:
                    self.rect.left = enemy.rect.right
                    self.x = self.rect.x 

        for powerup in powerups:
            if self.rect.colliderect(powerup.rect):
                self.apply_powerup(powerup)
                powerup.kill()