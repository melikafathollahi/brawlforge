import pygame
from src import config
from src import utils

class HealthBar:
    def __init__(self, x, y, max_value, *, img_path = None, bg_path = None, width = None, height = None):
        self.x = x
        self.y = y
        self.bar_img = None
        self.bar_bg_img = None
        if img_path and bg_path :
            self.bar_img = utils.load_image(img_path)
            self.bar_bg_img = utils.load_image(bg_path)
            self.height = height if height else self.bar_img.get_height()
            self.width = width if width else self.bar_img.get_width()
            self.bar_img = pygame.transform.smoothscale(self.bar_img, (self.width, self.height))
            self.bar_bg_img = pygame.transform.smoothscale(self.bar_bg_img, (self.width, self.height))
        else:
            self.height = height if height else 20
            self.width = width if width else 100

        self.current_value = max_value
        self.max_value = max_value


    def draw(self, screen):
        ratio = self.current_value / self.max_value
        bar_width = int(self.width * ratio)
        if self.bar_img:
            screen.blit(self.bar_bg_img, (self.x, self.y))
            if bar_width > 0:
                bar_surface = self.bar_img.subsurface((0, 0, bar_width, self.height))
                screen.blit(bar_surface, (self.x, self.y))

        else:
            bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            bar_rect = pygame.Rect(self.x, self.y, bar_width, self.height)
            pygame.draw.rect(screen, config.HEALTH_BAR_BACK_COLOR, bg_rect)
            if bar_width > 0:
                pygame.draw.rect(screen, config.HEALTH_BAR_COLOR, bar_rect)