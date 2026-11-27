import pygame
from src import config
from src.engine.healthbar import HealthBar
from src import utils
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, health_bar_width, health_bar_height, max_health = 100):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(x, y, width, height) 
        self.mask = pygame.mask.Mask((width, height), True)
        self.old_rect = self.rect.copy()


        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.is_jumping = False
        self.jump_count = 0

        self.max_health = max_health
        self.current_health = max_health
        self.health_bar = HealthBar (70, 70, max_health, 
                                     width = health_bar_width, 
                                     height = health_bar_height)
        
        self.animations = {}
        self.current_animation = None
        self.current_state = "idle"
        self.direction = [1, 1]

        self.is_dead = False
        self.is_dying = False
        self.is_hurt = False
        self.is_attacking = False
        self.is_walking = False

        self.hurt_end_time = 0
        self.attack_end_time = 0
        self.dying_end_time = 0


    def load_animations(self):
        pass


    def change_animation_state(self, new_state):
        if new_state != self.current_state and new_state in self.animations:
            old_animation = self.current_animation
            self.current_state = new_state
            self.current_animation = self.animations[new_state]

            if old_animation != self.current_animation:
                self.current_animation.reset()


    def handle_timers(self):
        now = pygame.time.get_ticks()
        
        if self.hurt_end_time and now > self.hurt_end_time:
            self.is_hurt = False
            self.hurt_end_time = 0
            
        if self.attack_end_time and now > self.attack_end_time:
            self.is_attacking = False
            self.attack_end_time = 0

        if self.dying_end_time and now > self.dying_end_time:
            self.is_dying = False
            self.is_dead = True
            self.dying_end_time = 0


    def take_damage(self, amount):
        if amount > 0 and not self.is_dead:
          self.current_health -= amount
          self.is_hurt = True
          self.hurt_end_time = pygame.time.get_ticks() + 600

          if self.current_health <= 0:
              self.current_health = 0
              self.is_dying = True
              self.dying_end_time = pygame.time.get_ticks() + 250


    def draw(self, surface, scroll_x, scroll_y):    
        if not self.is_dead:

            if self.current_animation:
                current_frame = self.current_animation.get_image()
                scaled_image = pygame.transform.smoothscale(current_frame, (self.width, self.height))
        
                if self.direction[0] == -1:
                    scaled_image = pygame.transform.flip(scaled_image, True, False)
                    self.mask = pygame.mask.from_surface(scaled_image)
                draw_pos = (self.rect.x - scroll_x, self.rect.y - scroll_y)
                surface.blit(scaled_image, draw_pos)

            # Draw health bar
            health_bar_x = self.rect.x - scroll_x + (self.rect.width - self.health_bar.width) // 2
            health_bar_y = self.rect.y - scroll_y - self.health_bar.height - 5
            
            old_x, old_y = self.health_bar.x, self.health_bar.y
            self.health_bar.x = health_bar_x
            self.health_bar.y = health_bar_y
            self.health_bar.draw(surface)
            self.health_bar.x, self.health_bar.y = old_x, old_y
        else:
            self.kill()


    def stay_in_bounds(self): 
        if self.rect.left < config.LEFT:
          self.rect.left = config.LEFT
        elif self.rect.right > config.RIGHT:
          self.rect.right = config.RIGHT

        if self.rect.top < 0:
          self.rect.top = 0
        elif self.rect.bottom > config.BOTTOM:
          self.rect.bottom = config.BOTTOM
    

    def apply_gravity(self):
        self.velocity_y += config.GRAVITY
        if self.velocity_y > config.MAX_FALL_SPEED:
            self.velocity_y = config.MAX_FALL_SPEED


    def check_tile_collisions(self, tiles):
        # Horizontal movement
        old_x = self.rect.x
        self.rect.x += int(self.velocity_x)

        for tile in tiles:
            tile_rect = tile.rect if hasattr(tile, 'rect') else tile

            if not self.rect.colliderect(tile_rect):   # skip if rects don't overlap
                continue

            # create a filled mask for the tile
            tile_mask = pygame.mask.Mask((tile_rect.width, tile_rect.height), fill=True)
            
            if not self.mask:
                continue  # Skip if no mask is available

            offset_x = tile_rect.x - self.rect.x
            offset_y = tile_rect.y - self.rect.y

            overlap = self.mask.overlap(tile_mask, (offset_x, offset_y))
            
            if overlap:
                if self.rect.x > old_x:  # moving right
                    self.rect.right = tile_rect.left
                    self.velocity_y = 0
                elif self.rect.x < old_x:  # moving left
                    self.rect.left = tile_rect.right
                    self.velocity_y = 0

        # Vertical movement
        self.rect.y += int(self.velocity_y)

        for tile in tiles:
            tile_rect = tile.rect if hasattr(tile, 'rect') else tile

            if not self.rect.colliderect(tile_rect):
                continue

            tile_mask = pygame.mask.Mask((tile_rect.width, tile_rect.height), fill=True)
            
            if not self.mask:
                continue

            offset_x = tile_rect.x - self.rect.x
            offset_y = tile_rect.y - self.rect.y

            overlap = self.mask.overlap(tile_mask, (offset_x, offset_y))
            
            if overlap:
                if self.velocity_y > 0:  # falling
                    self.rect.bottom = tile_rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jump_count = 0
                elif self.velocity_y < 0:  # jumping up
                    self.rect.top = tile_rect.bottom
                    self.velocity_y = 0


    def update(self, tiles, *args, **kwargs): 
      self.old_rect = self.rect.copy()
      if self.current_animation:
        self.current_animation.update()

      self.apply_gravity()
      self.check_tile_collisions(tiles)

      # place the healthbar above the entity
      self.health_bar.current_value = self.current_health
      self.health_bar.x = self.rect.x + (self.rect.width - self.health_bar.width) // 2
      self.health_bar.y = self.rect.y - self.health_bar.height - 5

      self.handle_timers()   
      self.stay_in_bounds()
