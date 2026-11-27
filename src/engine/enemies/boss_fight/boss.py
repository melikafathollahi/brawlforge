import pygame
from src import config
from typing import Optional, Iterable
from src.engine.enemies.base import Enemy
from src.engine.enemies.boss_fight import DialogueBox, VisionSystem, TauntGenerator
from src.engine import Animation, AnimationConfig, BulletHandler

class Boss(Enemy):
    def __init__(self, x, y, vision_system, taunt_generator):
        super().__init__(x, y, enemy_type="boss")

        self.max_health = config.BOSS_HEALTH
        self.current_health = self.max_health
        self.last_health = self.max_health

        self.phase = 1
        self.max_phase = 4
        self.name = "Boss"

        self.attack_phase = 1
        self.current_attack = None
        self.is_special = False
        self.bullet_handler = BulletHandler()
        self.last_shot_time = 0

        self.vision_system = vision_system
        self.taunt_generator = taunt_generator
        self.minion_alive = False
        self.dialogue_box = None

        self.enemy_group = None          #type: Optional[Iterable]
        self.phase_minions = None        #type: Optional[Iterable]
        self.player = None

        font = pygame.font.Font(config.FONT_PATH, 24)
        self.name_text = font.render(self.name, True, (255, 0, 0))

        self.load_animations()


    def load_animations(self):
        sprite_configs = AnimationConfig.get_boss_sprite_configs()
        validated = AnimationConfig.validate_sprite_configs(sprite_configs)

        frame_durations = {
            "idle": 200,
            "walk": 120,
            "attack_1": 80,
            "attack_2": 80,
            "attack_3": 80,
            "attack_4": 120,
            "hurt": 100,
            "special": 120,
            "death": 200,
        }

        for state, config in validated.items():
            duration = frame_durations.get(state, 150)
            self.animations[state] = Animation(config, duration)

        self.current_animation = self.animations.get("idle")
        self.current_state = "idle"
        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()


    def update_animation_state(self):
        next_state = "idle"
        if self.is_dying:
            next_state = "death"
        elif self.is_hurt:
            next_state = "hurt"
        elif self.is_special:
            next_state = "special"
        elif self.is_attacking:
            next_state = f"attack_{self.attack_phase}"
        elif self.is_walking:
            next_state = "walk"

        self.change_animation_state(next_state)


    def handle_phase_logic(self):
        self.vision_system.update()

        if self.current_health < self.last_health - 50:
            self.last_health = self.current_health
            if self.current_health < self.max_health * 0.25:
                self.taunt_generator.generate_taunt("boss_low_health")
            else:
                self.taunt_generator.generate_taunt("boss_took_damage")

        if self.player and self.player.current_health < self.player.last_health - 20:
            self.player.last_health = self.player.current_health
            self.taunt_generator.generate_taunt("player_took_damage")

        if self.enemy_group and self.phase_minions:
            if self.minion_alive and not any(getattr(e, "active", False) and e != self for e in self.enemy_group):
                self.minion_alive = False
                self.phase += 1
                if self.phase <= self.max_phase:
                    self.taunt_generator.generate_taunt(f"phase_{self.phase}")
                    self.start_phase()
                    self.spawn_minion(self.phase_minions)

        if self.dialogue_box:
            self.dialogue_box.typing_effect()


    def start_phase(self):
        print("phase sstarting!")
        self.vision_system.start()
        reason = "phase_transition" if self.phase > 1 else "intro"
        self.taunt_generator.generate_taunt(reason)


    def spawn_minion(self, phase_minions):
        if not self.minion_alive and self.phase in phase_minions:
            minion = phase_minions[self.phase]
            minion.active = True
            self.minion_alive = True


    def shoot(self, player):
        if self.is_attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > config.BOSS_BULLET_COOLDOWN:
                boss_pos = pygame.Vector2(self.rect.centerx, self.rect.centery)
                player_pos = pygame.Vector2(player.rect.centerx, player.rect.centery)
                velocity = player_pos - boss_pos
                if velocity.length() > 0:
                    velocity.scale_to_length(config.BOSS_BULLET_SPEED)
                    self.bullet_handler.fire(self.rect.centerx, self.rect.centery, velocity, bullet_type='boss')
                    self.last_shot_time = current_time


    def on_dialogue_complete(self):
        self.taunt_generator.taunt_active = False


    def on_taunt_generated(self, taunt_text):
        pos = (self.rect.centerx - 100, self.rect.top - 180)
        self.dialogue_box = DialogueBox(pos, taunt_text, on_finish_typing = self.on_dialogue_complete)


    def update(self, tiles, player):
        super().update(tiles, player)
        self.player = player
        self.handle_phase_logic()
        self.shoot(player)

        if self.is_dead or self.is_hurt:
            pass
        else:
            distance = abs(player.rect.centerx - self.rect.centerx)
            if distance > 500:
                self.is_walking = True
                self.rect.x += 3 * (1 if player.rect.centerx > self.rect.centerx else -1)
            else:
                self.is_walking = False

            if distance < 200 and not self.is_attacking and not self.is_special:
                if pygame.time.get_ticks() % 100 < 10:
                    self.is_special = True
                    self.taunt_generator.generate_taunt("special_attack")
                else:
                    self.is_attacking = True
                    self.taunt_generator.generate_taunt(f"attack_{self.attack_phase}")

        now = pygame.time.get_ticks()
        if self.current_animation and now - self.animation_timer >= self.current_animation.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.current_animation.frames)
            self.animation_timer = now

        if player.rect.centerx < self.rect.centerx:
            self.direction[0] = 1
        else:
            self.direction[0] = -1

        if self.is_attacking and self.current_animation and self.current_frame >= len(self.current_animation.frames) - 1:
            self.is_attacking = False
            if self.attack_phase != 4:
                self.attack_phase = (self.attack_phase % 4) + 1
        elif self.is_special and self.current_animation and self.current_frame >= len(self.current_animation.frames) - 1:
            self.is_special = False
        elif self.is_hurt and self.current_animation and self.current_frame >= len(self.current_animation.frames) - 1:
            self.is_hurt = False

        self.update_animation_state()


    def draw(self, surface, scroll_x, scroll_y):
        super().draw(surface, scroll_x, scroll_y)

        if hasattr(self, 'name_text'):
            name_x = self.rect.centerx - self.name_text.get_width() // 2 - scroll_x
            name_y = self.rect.top - 40 - scroll_y
            surface.blit(self.name_text, (name_x, name_y))

        if self.vision_system.fog_active:
            self.vision_system.draw(surface, (
                self.rect.center[0] - scroll_x,
                self.rect.center[1] - scroll_y))

        if self.dialogue_box:
            self.dialogue_box.pos = (self.rect.centerx - 100 - scroll_x, self.rect.top - 180 - scroll_y)
            self.dialogue_box.draw(surface)
