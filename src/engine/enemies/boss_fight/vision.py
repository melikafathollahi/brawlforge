import pygame
from src import config
from itertools import repeat # for screen shake
import random

class VisionSystem:
    def __init__(self, radius):
       self.fog_start = 0
       self.fog_duration = 3000
       self.fog_end_time = 0
       self.radius = radius
       self.fog_active = True

       self.dark_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT),pygame.SRCALPHA)
       self.dark_surface.fill((0,0,0,255))

       self.gradient_light = self.create_gradient_light(radius)

    def start(self):
        print("start fog system")
        self.fog_active = True
        self.fog_start = pygame.time.get_ticks()

    def update(self):
        if self.fog_active and pygame.time.get_ticks() - self.fog_start > self.fog_duration:
            self.fog_active = False

    def draw(self, surface, player_pos):
        if not self.fog_active:
            return

        self.dark_surface.fill((0, 0, 0, 180))

        light_rect = self.gradient_light.get_rect(center=player_pos)
        self.dark_surface.blit(self.gradient_light, light_rect, special_flags=pygame.BLEND_RGBA_SUB)

        surface.blit(self.dark_surface, (0, 0))

    def create_gradient_light(self, radius):
        size = radius * 2
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        for r in range(radius, 0, -1):
            alpha = int(255 * (1 - r / radius)) 
            pygame.draw.circle(surf, (0, 0, 0, alpha), (radius, radius), r)

        return surf

"""     def screen_shake(self, screen):
        if config.SCREEN_SHAKE:
            shake_offset = pygame.Vector2(
                config.SHAKE_OFFSET * (0.5 - pygame.math.random.random()),
                config.SHAKE_OFFSET * (0.5 - pygame.math.random.random())
            )
            screen.blit(screen, shake_offset)
        else:
            screen.fill((0, 0, 0)) """