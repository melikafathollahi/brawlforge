import pygame
from src import config
from src.engine import Entity, Animation, AnimationConfig

class Enemy(Entity):
    def __init__(self, x=0, y=0, enemy_type="bomb_chaser"):
        
        if enemy_type in ["bomb_chaser", "swift_striker"]:
            width = 128
            height = 128
        elif enemy_type in ["sniper"]:
            width = 70
            height = 75
        elif enemy_type in ["boss"]:
            width = 200
            height = 180
        elif enemy_type in ["freezer"]:
            width = 96
            height = 96
        else:
            width = getattr(config, 'ENEMY_WIDTH', 48)
            height = getattr(config, 'ENEMY_HEIGHT', 48)
            
        bar_width = getattr(config, 'ENEMY_BAR_WIDTH', 40)
        bar_height = getattr(config, 'ENEMY_BAR_HEIGHT', 5)
        
        super().__init__(x, y, width, height, bar_width, bar_height)

        self.enemy_type = enemy_type
        self.active = True

        self.load_animations()


    def load_animations(self):     
        sprite_configs = AnimationConfig.get_enemy_sprite_configs(self.enemy_type)
        validated_configs = AnimationConfig.validate_sprite_configs(sprite_configs)

        for state, config in validated_configs.items():
            frame_duration = 200
            if state in ["walk", "run"]:
                frame_duration = 120
            elif state == "attack":
                frame_duration = 80
            elif state == "explosion":
                frame_duration = 100
            elif state in ["shot_1", "shot_2", "shot"]:
                frame_duration = 100
            elif state == "charge":
                frame_duration = 100

            self.animations[state] = Animation(config, frame_duration)

        self.current_animation = self.animations.get("idle")
        self.current_state = "idle"


    def change_animation_state(self, new_state):
        if new_state != self.current_state:
            self.current_state = new_state
            if new_state in self.animations:
                self.current_animation = self.animations[new_state]
                old_animation = self.current_animation
                if old_animation != self.current_animation:
                    self.current_animation.reset()
            else:
                # Try some common alternatives
                alternatives = {
                    "dead": ["death", "die"],
                    "death": ["dead", "die"],
                    "hurt": ["damage", "hit"],
                    "attack": ["attacking", "shoot"],
                    "walk": ["walking", "move"],
                    "run": ["running", "sprint"],
                    "idle": ["idle_1", "idle_2", "standing"]
                }
    
                if new_state in alternatives:
                    for alt in alternatives[new_state]:
                        if alt in self.animations:
                            old_animation = self.current_animation
                            self.current_animation = self.animations[alt]
                            if old_animation != self.current_animation:
                                self.current_animation.reset()
                            break
                

    def update(self, tiles, player):
        self.stay_in_bounds()
        # Adjust the position above the Enemy
        self.health_bar.x = self.rect.x + (self.rect.width - config.ENEMY_BAR_WIDTH) // 2
        self.health_bar.y = self.rect.y - config.ENEMY_BAR_HEIGHT - 25  
        self.health_bar.current_value = self.current_health

        if self.current_animation:
            self.current_animation.update()

        self.check_tile_collisions(tiles)
        self.apply_gravity()
        self.old_rect = self.rect.copy()
        self.handle_timers()


    def draw(self, surface, scroll_x, scroll_y):
        super().draw(surface, scroll_x, scroll_y)
        if not self.is_dead and self.current_animation:
            current_frame = self.current_animation.get_image()
            
            # Scale frame to match rect size if needed
            if (current_frame.get_width() != self.rect.width or 
                current_frame.get_height() != self.rect.height):
                current_frame = pygame.transform.smoothscale(
                    current_frame, (self.rect.width, self.rect.height)
                )
    

