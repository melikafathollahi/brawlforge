import pygame
from src import config
from src import utils
from src.engine.bullet import Bullet

class BulletHandler:
    def __init__(self, pool_size=50):
        self.bullets = pygame.sprite.Group()
        self.pool_size = pool_size


    def fire(self, x, y, direction, bullet_type='normal'):
        if len(self.bullets) < self.pool_size:
            velocity = pygame.Vector2(direction)
            bullet = Bullet(x, y, velocity, bullet_type)
            self.bullets.add(bullet)


    def update(self, enemies_group, player):
        for bullet in self.bullets:      # Move all bullets
            bullet.update()
        self.check_collisions(enemies_group, player)  # Then check collisions


    def draw(self, screen, scroll_x=0 , scroll_y=0):
        for bullet in self.bullets:
            bullet.draw(screen, scroll_x, scroll_y)


    def check_collisions(self, enemies_group, player):
        bullets_to_remove = []
        for bullet in self.bullets:

            if bullet.bullet_type == 'normal':
                for enemy in enemies_group:
                    if utils.check_collision(enemy, bullet) and not enemy.is_dead:
                        enemy.take_damage(player.damage)
                        bullets_to_remove.append(bullet)
                        break

            else:
                if utils.check_collision(player, bullet) and not player.is_dead:
                    if not player.shield_active:
                        if bullet.bullet_type == 'freezer':
                            player.freeze()
                        else:
                            player.take_damage(config.ENEMY_DAMAGE)
                    bullets_to_remove.append(bullet)

        # add a swift striker bullet type!!
      
         # Remove bullets after iteration
        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
      
