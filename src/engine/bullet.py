import pygame
from src import config
from src import utils
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, bullet_type='normal'):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        if bullet_type == 'sniper':
            self.image = utils.load_image(config.SNIPER_BULLET)
        elif bullet_type == 'freezer':
            self.image = utils.load_image(config.FREEZER_BULLET)
        elif bullet_type == 'boss':
            self.image = utils.load_image(config.BOSS_BULLET)
        elif bullet_type == 'swift_striker':
            self.image = utils.load_image(config.SWIFT_STRIKER_BULLET)
        elif bullet_type =='normal':
            self.image = pygame.Surface((config.BULLET_WIDTH, config.BULLET_HEIGHT), pygame.SRCALPHA)
            for radius in range(15, 5, -2):
                color = (0, 191, 255, 150 - (15-radius)*10)  # Blue with fading alpha
                pygame.draw.circle(
                    self.image,
                    color,
                    (config.BULLET_WIDTH // 2, config.BULLET_HEIGHT // 2),
                    radius
                )
        
        if self.image:
            self.image = pygame.transform.smoothscale(self.image, (config.BULLET_WIDTH, config.BULLET_HEIGHT))
            self.rect = self.image.get_rect(topleft=(x, y))
        if not hasattr(self, 'image'):
            self.image = pygame.Surface((config.BULLET_WIDTH, config.BULLET_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0), (config.BULLET_WIDTH//2, config.BULLET_HEIGHT//2), 5)

        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = velocity
        self.bullet_type = bullet_type  # 'normal', 'sniper', 'freezer', etc.
        

    def move(self):
        self.pos += self.velocity
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))



    def draw(self, screen , scroll_x=0, scroll_y=0):
        if not self.image:
            return
        draw_pos = (self.rect.x - scroll_x, self.rect.y - scroll_y)
        screen.blit(self.image, draw_pos)


    def update(self):
        self.move()
