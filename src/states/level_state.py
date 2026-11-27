import pygame
import config
import random
from src import config
from src.engine import Button, TileMap, Player, PowerUp
from src.states.pause_state import PauseState
from src.states.game_state import GameState
from src.engine.enemies import BombChaser, Freezer, Sniper, SwiftStriker
from src.engine.enemies.boss_fight import Boss, TauntGenerator, VisionSystem
class LevelState(GameState):
    def __init__(self, game, map_path):
        super().__init__(game)
        self.map = TileMap(map_path)
        self.collision_tiles = self.map.get_collision_tiles()
        
        selected_character = getattr(game, 'selected_character', 'kitsune')
        character_data = getattr(game, 'character_data', None)
        
        self.player = Player(
            x=1100, 
            y=400, 
            character=selected_character,
            character_data=character_data
        )

        self.powerups = pygame.sprite.Group() 
        self.last_powerup_spawn_time = pygame.time.get_ticks()
        self.POWERUP_SPAWN_INTERVAL = 15000
        self.powerup_spawn_locations = []
        
        self.enemies = pygame.sprite.Group()
        self.scroll_x = 0
        self.scroll_y = 0
        self.paused = False
        self.finished = False  
        self.pause_button = Button(1100, 50, 100, 40, config.PAUSE_IMG)

        self.name_level = "Level1"  
        
        
    def play_music(self):
        """play different music for each level""" 
        music_path = config.LEVEL_MUSIC.get(self.name_level)
        if music_path:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)  
    

    def stop_music(self):
        pygame.mixer.music.stop()
    

    def pause_music(self):
        pygame.mixer.music.set_volume(0.0)
        

    def resume_music(self):
        pygame.mixer.music.set_volume(1.0)


    def load_objects(self):   
        for obj in self.map.tmx_data.objects:
            if obj.name == "player":
                selected_character = getattr(self.game, 'selected_character', 'kitsune')
                character_data = getattr(self.game, 'character_data', None)
                self.player = Player(obj.x, obj.y, selected_character, character_data)
            elif obj.name == "bomb":
                self.enemies.add(BombChaser(obj.x, obj.y))
            elif obj.name == "freezer":
                self.enemies.add(Freezer(obj.x, obj.y))
            elif obj.name == "sniper":
                self.enemies.add(Sniper(obj.x, obj.y))   
            elif obj.name == "swiftstriker":
                self.enemies.add(SwiftStriker(obj.x, obj.y))
            elif obj.name == "powerup": 
                self.powerup_spawn_locations.append((obj.x, obj.y))


    def handle_events(self):
        if self.pause_button.handle_events():
            self.game.state_manager.register_state("pause_state", 
            PauseState(self.game, self.game.state_manager.current_state))
            pause_state = PauseState(self.game, self.game.state_manager.current_state)
            self.game.state_manager.states["pause_state"] = pause_state
            self.game.state_manager.change_state("pause_state")
            self.pause_music()


    def get_level_number(self):
        """Override in subclasses to return the level number"""
        raise NotImplementedError


    def get_next_level_state(self):
        """Override in subclasses to return the next level state name"""
        raise NotImplementedError
    

    def spawn_powerups(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_powerup_spawn_time > self.POWERUP_SPAWN_INTERVAL:
            if self.powerup_spawn_locations: 
                spawn_x, spawn_y = random.choice(self.powerup_spawn_locations)
                
                new_powerup = PowerUp(spawn_x, spawn_y)
                self.powerups.add(new_powerup)

                new_powerup.powerup_spawn_sound.play() 
                self.last_powerup_spawn_time = current_time 

        self.powerups.update(current_time)
        
    
    def update_enemies(self):
        for enemy in list(self.enemies):
            if not enemy.is_dead:
                enemy.update(self.collision_tiles, self.player)
            else:
                self.enemies.remove(enemy)

    
    def check_win_state(self):
        if not self.enemies:
            self.finished = True
            self.stop_music()
            win_state = self.game.state_manager.states.get("win_state")
            if win_state:
                win_state.set_previous_state(self.name_level)
            self.game.state_manager.change_state("win_state")


    def check_game_over(self):
        if self.player.is_dead:
            self.stop_music()
            self.game.state_manager.change_state("game_over")


    def update_camera(self):
        self.scroll_x = self.player.rect.centerx - 300
        self.scroll_y = self.player.rect.centery - 400


    def update(self):
        if self.paused or self.finished:
            return
        if not pygame.mixer.music.get_busy():
            self.play_music()

        self.check_game_over()
        self.check_win_state()

        self.player.update(self.collision_tiles)

        self.spawn_powerups()
        
        self.update_enemies()

        self.update_camera()

        self.player.bullet_handler.update(self.enemies, self.player)
        self.player.reset_movement_state()
        self.handle_input()
        self.player.check_other_collisions(self.enemies, self.powerups)


    def handle_input(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_ESCAPE]:
            self.pause_music()  
            self.game.state_manager.register_state("pause_state", 
            PauseState(self.game, self.game.state_manager.current_state))
            pause_state = PauseState(self.game, self.game.state_manager.current_state)
            self.game.state_manager.states["pause_state"] = pause_state
            self.game.state_manager.change_state("pause_state")
        if pressed_keys[pygame.K_a]:
            self.player.move_left()
        elif pressed_keys[pygame.K_d]:
            self.player.move_right()
        if pressed_keys[pygame.K_SPACE]:
            self.player.jump(self.collision_tiles)
        if pressed_keys[pygame.K_f] or pygame.mouse.get_pressed()[0]:
            self.player.shoot()


    def draw(self, surface):
        self.map.draw_map(surface, self.scroll_x, self.scroll_y)
        self.player.draw(surface, self.scroll_x, self.scroll_y)  
        for enemy in self.enemies:
            enemy.draw(surface, self.scroll_x, self.scroll_y)
        self.pause_button.draw(surface)

        for powerup in self.powerups:
            powerup.draw(surface, self.scroll_x, self.scroll_y)

        self.player.bullet_handler.draw(surface, self.scroll_x, self.scroll_y)
       

class Level1State(LevelState):
    def __init__(self, game):
        super().__init__(game, config.LEVEL1_MAP)
        self.load_objects()  
        self.game.state_manager.current_state = "Level1"
        self.name_level="Level1"
        
        

    def get_level_number(self):
        return 1


    def get_next_level_state(self):
        return "Level2"


    def go_to_next_level(self):
        self.game.state_manager.change_state("level2")

class Level2State(LevelState):
    def __init__(self, game):
        super().__init__(game, config.LEVEL2_MAP)
        self.name_level="Level2"
        self.load_objects()  
        self.game.state_manager.current_state = "Level2"

    def get_level_number(self):
        return 2

    def get_next_level_state(self):
        return "Level3"
    
    def go_to_next_level(self):
        self.game.state_manager.change_state("level3")

class Level3State(LevelState):
    def __init__(self, game):
        super().__init__(game, config.LEVEL3_MAP)
        self.name_level="Level3"
        self.load_objects()  
        self.game.current_state = "Level3"

    def get_level_number(self):
        return 3


    def get_next_level_state(self):
        return "Level4"


    def go_to_next_level(self):
        self.game.state_manager.change_state("level4")


class Level4State(LevelState):
    def __init__(self, game):
        super().__init__(game, config.LEVEL4_MAP)
        self.name_level = "Level4"
        self.game.current_state = "Level4"

        self.phase_minions = {}
        self.dialogue_box = None
        self.current_phase = 1
        self.active_minion = None

        self.vision_system = VisionSystem(radius=200)
        self.taunt_generator = TauntGenerator(self.on_taunt_ready)

        self.load_objects()  

        self.boss = Boss(self.boss_position[0], self.boss_position[1],
                         self.vision_system,
                         self.taunt_generator)
        self.boss.taunt_generator.on_taunt_callback = self.boss.on_taunt_generated
        self.boss.enemy_group = self.enemies
        self.boss.phase_minions = self.phase_minions
        self.boss.start_phase()

        self.enemies.add(self.boss)

        self.active_minion = self.phase_minions.get(self.current_phase)
        if self.active_minion:
            self.active_minion.active = True
            self.enemies.add(self.active_minion)


    def load_objects(self):
        for obj in self.map.tmx_data.objects:
            if obj.name == "player":
                selected_character = getattr(self.game, 'selected_character', 'kitsune')
                character_data = getattr(self.game, 'character_data', None)
                self.player = Player(obj.x, obj.y, selected_character, character_data)
            elif obj.name == "boss":
                self.boss_position = (obj.x, obj.y)
            elif obj.name in ["sniper", "freezer", "bomb", "swiftstriker"]:
                enemy_class = {
                    "sniper": Sniper,
                    "freezer": Freezer,
                    "bomb": BombChaser,
                    "swiftstriker": SwiftStriker
                }[obj.name]
                enemy = enemy_class(obj.x, obj.y)
                enemy.active = False
                phase_index = ["sniper", "freezer", "bomb", "swiftstriker"].index(obj.name) + 1
                self.phase_minions[phase_index] = enemy


    def on_taunt_ready(self, taunt_text):
        # handled via callback in boss
        pass


    def update(self):
        super().update()
        self.vision_system.update()

        if self.boss:
            self.boss.update(self.collision_tiles, self.player)

        if self.active_minion and self.active_minion.active:
            self.active_minion.update(self.collision_tiles, self.player)

        if self.active_minion and self.active_minion.is_dead:
            self.current_phase += 1
            self.active_minion = self.phase_minions.get(self.current_phase)
            if self.active_minion:
                self.active_minion.active = True
                self.enemies.add(self.active_minion)
                self.boss.phase = self.current_phase
                self.boss.start_phase()
            else:
                self.go_to_next_level()

        if self.boss and self.boss.is_dead:
            self.go_to_next_level()


    def draw(self, surface):
        super().draw(surface)

        if self.boss:
            self.boss.draw(surface, self.scroll_x, self.scroll_y)

        if self.active_minion and self.active_minion.active:
            self.active_minion.draw(surface, self.scroll_x, self.scroll_y)

        self.vision_system.draw(surface, self.player.rect.center)


    def get_level_number(self):
        return 4


    def go_to_next_level(self):
        self.game.state_manager.change_state("win_state")