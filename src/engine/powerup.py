import pygame
from src import config
import random
from src import utils
class PowerUp(pygame.sprite.Sprite):
    TYPES = ["boost_damage", "double_jump", "shield"]
    LIFETIME = 15000  
    DURATION = {
        "boost_damage": 10000,
        "double_jump": 12000,
        "shield": 8000
    }

    def __init__(self, x, y, kind = None):
        super().__init__()
        self.kind = kind or random.choice(self.TYPES)
        self.spawn_time = pygame.time.get_ticks()
        self.picked = False
        self.pick_time = None
        self.powerup_spawn_sound = pygame.mixer.Sound(config.POWERUP_SPAWN_SOUND)
        self.powerup_collected_sound = pygame.mixer.Sound(config.POWERUP_COLLECTED_SOUNT)

        self.world_x = x
        self.world_y = y
        
        img_path = getattr(config, f"PU_{self.kind.upper()}_IMG")
        self.image = utils.load_image(img_path)
        self.image = pygame.transform.smoothscale(self.image, (32, 32))
      
        self.rect = self.image.get_rect(center = (self.world_x, self.world_y))


    def update(self, now=None):
        now = now or pygame.time.get_ticks()
        if not self.picked and now - self.spawn_time > self.LIFETIME:
            self.kill()

        if self.picked:
            if self.pick_time and now - self.pick_time > self.DURATION[self.kind]:
                self.kill()
    

    def apply_to(self, player):
        """Grant effect and start timer."""
        self.picked = True
        self.powerup_collected_sound.play()
        self.pick_time = pygame.time.get_ticks()
        if self.kind == "boost_damage":
            player.damage += config.POWERUP_DAMAGE_BOOST

        elif self.kind == "double_jump":
            player.can_double_jump = True

        elif self.kind == "shield":
            player.shield_active = True


    def draw(self, surface, scroll_x, scroll_y):
        if not self.picked:
            draw_x = self.world_x - scroll_x
            draw_y = self.world_y - scroll_y
            
            draw_rect = self.image.get_rect(center=(draw_x, draw_y))
            
            utils.draw(surface, self.image, draw_rect)
