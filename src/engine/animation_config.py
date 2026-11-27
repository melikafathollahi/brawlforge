import os
from src import config

class AnimationConfig:
    """Helper class to manage sprite sheet animations"""
    
    BASE_ASSETS_PATH = "src/assets/images"
    PLAYER_PATH = os.path.join(BASE_ASSETS_PATH, "player")
    ENEMIES_PATH = os.path.join(BASE_ASSETS_PATH, "enemies")
    
    @staticmethod
    def get_player_sprite_configs(character="kitsune"):
        """Get sprite sheet configurations for player"""
        
        character = character.lower()   # Ensure character is lowercase
        
        base_path = os.path.join(AnimationConfig.PLAYER_PATH, character)
        
        frame_width = 128
        frame_height = 128
        
        if character == "kitsune":
            sprite_configs = {
                "idle": {
                    "path": os.path.join(base_path, "Idle.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "idle_2": {
                    "path": os.path.join(base_path, "Idle_2.png"),
                    "frames": 6,
                    "width": frame_width,
                    "height": frame_height
                },
                "walk": {
                    "path": os.path.join(base_path, "Walk.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "run": {
                    "path": os.path.join(base_path, "Run.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "jump": {
                    "path": os.path.join(base_path, "Jump.png"),
                    "frames": 10,
                    "width": frame_width,
                    "height": frame_height
                },
                "attack": {
                    "path": os.path.join(base_path, "Attack_1.png"),
                    "frames": 10,
                    "width": frame_width,
                    "height": frame_height
                },
                "attack_2": {
                    "path": os.path.join(base_path, "Attack_2.png"),
                    "frames": 10,
                    "width": frame_width,
                    "height": frame_height
                },
                "attack_3": {
                    "path": os.path.join(base_path, "Attack_3.png"),
                    "frames": 7,
                    "width": frame_width,
                    "height": frame_height
                },
                "hurt": {
                    "path": os.path.join(base_path, "Hurt.png"),
                    "frames": 2,
                    "width": frame_width,
                    "height": frame_height
                },
                "death": {
                    "path": os.path.join(base_path, "Dead.png"),
                    "frames": 10,
                    "width": frame_width,
                    "height": frame_height
                },
                "fire_1": {
                    "path": os.path.join(base_path, "Fire_1.png"),
                    "frames": 14,
                    "width": frame_width,
                    "height": frame_height
                },
                "fire_2": {
                    "path": os.path.join(base_path, "Fire_2.png"),
                    "frames": 11,
                    "width": frame_width,
                    "height": frame_height
                }
            }
        
        elif character == "magican":
            sprite_configs = {
                "idle": {
                    "path": os.path.join(base_path, "Idle.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "walk": {
                    "path": os.path.join(base_path, "Walk.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "run": {
                    "path": os.path.join(base_path, "Run.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "jump": {
                    "path": os.path.join(base_path, "Jump.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "attack": {
                    "path": os.path.join(base_path, "Attack_1.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "attack_2": {
                    "path": os.path.join(base_path, "Attack_2.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "hurt": {
                    "path": os.path.join(base_path, "Hurt.png"),
                    "frames": 4,
                    "width": frame_width,
                    "height": frame_height
                },
                "death": {
                    "path": os.path.join(base_path, "Dead.png"),
                    "frames": 5,
                    "width": frame_width,
                    "height": frame_height
                },
                "charge_1": {
                    "path": os.path.join(base_path, "Charge_1.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "charge_2": {
                    "path": os.path.join(base_path, "Charge_2.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                }
            }
            
        elif character == "kunoichi":
            sprite_configs = {
                "idle": {
                    "path": os.path.join(base_path, "Idle.png"),
                    "frames": 9,
                    "width": frame_width,
                    "height": frame_height
                },
                "walk": {
                    "path": os.path.join(base_path, "Walk.png"), 
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "run": {
                    "path": os.path.join(base_path, "Run.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "jump": {
                    "path": os.path.join(base_path, "Jump.png"),
                    "frames": 10,
                    "width": frame_width,
                    "height": frame_height
                },
                "attack": {
                    "path": os.path.join(base_path, "Attack_1.png"),
                    "frames": 6,
                    "width": frame_width,
                    "height": frame_height
                },
                "hurt": {
                    "path": os.path.join(base_path, "Hurt.png"),
                    "frames": 2,
                    "width": frame_width,
                    "height": frame_height
                },
                "death": {
                    "path": os.path.join(base_path, "Dead.png"),
                    "frames": 5,
                    "width": frame_width,
                    "height": frame_height
                },
                # Additional animations specific to Kunoichi
                "cast": {
                    "path": os.path.join(base_path, "Cast.png"),
                    "frames": 6,
                    "width": frame_width,
                    "height": frame_height
                },
                "attack_2": {
                    "path": os.path.join(base_path, "Attack_2.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "eating": {
                    "path": os.path.join(base_path, "Eating.png"),
                    "frames": 9,
                    "width": frame_width,
                    "height": frame_height
                }
            }
        else:
            # Default fallback
            sprite_configs = {
                "idle": {
                    "path": None,
                    "frames": 1,
                    "width": frame_width,
                    "height": frame_height
                }
            }
        
        return sprite_configs
    
    @staticmethod
    def get_enemy_sprite_configs(enemy_type):
        """Get sprite sheet configurations for enemies with correct frame counts"""
        enemy_folders = {
            "bomb_chaser": "Fire_Spirit",
            "freezer": "freezer", 
            "sniper": "Archer",
            "swift_striker": "Swordsman",
        }
        
        if enemy_type not in enemy_folders:
            return {}
            
        folder = enemy_folders[enemy_type]
        base_path = os.path.join(AnimationConfig.ENEMIES_PATH, folder)
        
        # Special sizes for different enemies
        if enemy_type in ["bomb_chaser", "swift_striker", "sniper"]:
            frame_width = 128
            frame_height = 128
        elif enemy_type == "freezer":
            frame_width = 96
            frame_height = 96
        else:
            frame_width = config.ENEMY_WIDTH
            frame_height = config.ENEMY_HEIGHT
        
        if enemy_type == "bomb_chaser":  
            
            sprite_configs = {
                "idle": {
                    "path": os.path.join(base_path, "Idle.png"),
                    "frames": 6,
                    "width": frame_width,
                    "height": frame_height
                },
                "idle_2": {
                    "path": os.path.join(base_path, "Idle_2.png"),
                    "frames": 6,
                    "width": frame_width,
                    "height": frame_height
                },
                "walk": {
                    "path": os.path.join(base_path, "Walk.png"),
                    "frames": 7,
                    "width": frame_width,
                    "height": frame_height
                },
                "run": {
                    "path": os.path.join(base_path, "Run.png"),
                    "frames": 7,
                    "width": frame_width,
                    "height": frame_height
                },
                "charge": {
                    "path": os.path.join(base_path, "Charge.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "attack": {
                    "path": os.path.join(base_path, "Attack.png"),
                    "frames": 14,
                    "width": frame_width,
                    "height": frame_height
                },
                "explosion": {
                    "path": os.path.join(base_path, "Explosion.png"),
                    "frames": 11,
                    "width": frame_width,
                    "height": frame_height
                },
                "flame": {
                    "path": os.path.join(base_path, "Flame.png"),
                    "frames": 13,
                    "width": frame_width,
                    "height": frame_height
                },
                "shot": {
                    "path": os.path.join(base_path, "Shot.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "hurt": {
                    "path": os.path.join(base_path, "Hurt.png"),
                    "frames": 3,
                    "width": frame_width,
                    "height": frame_height
                },
                "dead": {
                    "path": os.path.join(base_path, "Dead.png"),
                    "frames": 5,
                    "width": frame_width,
                    "height": frame_height
                }
            }
            
        elif enemy_type == "sniper":  
            sprite_configs = {
                "idle": {
                    "path": os.path.join(base_path, "Idle.png"),
                    "frames": 6,
                    "width": frame_width,
                    "height": frame_height
                },
                "idle_2": {
                    "path": os.path.join(base_path, "Idle_2.png"),
                    "frames": 4,
                    "width": frame_width,
                    "height": frame_height
                },
                "walk": {
                    "path": os.path.join(base_path, "Walk.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "run": {
                    "path": os.path.join(base_path, "Run.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "jump": {
                    "path": os.path.join(base_path, "Jump.png"),
                    "frames": 9,
                    "width": frame_width,
                    "height": frame_height
                },
                "attack": {
                    "path": os.path.join(base_path, "Attack_1.png"),
                    "frames": 4,
                    "width": frame_width,
                    "height": frame_height
                },
                "shot_1": {
                    "path": os.path.join(base_path, "Shot_1.png"),
                    "frames": 14,
                    "width": frame_width,
                    "height": frame_height
                },
                "shot_2": {
                    "path": os.path.join(base_path, "Shot_2.png"),
                    "frames": 13,
                    "width": frame_width,
                    "height": frame_height
                },
                "arrow": {
                    "path": os.path.join(base_path, "Arrow.png"),
                    "frames": 1,
                    "width": frame_width,
                    "height": frame_height
                },
                "hurt": {
                    "path": os.path.join(base_path, "Hurt.png"),
                    "frames": 3,
                    "width": frame_width,
                    "height": frame_height
                },
                "dead": {
                    "path": os.path.join(base_path, "Dead.png"),
                    "frames": 3,
                    "width": frame_width,
                    "height": frame_height
                }
            }
            
        elif enemy_type == "freezer":
            sprite_configs = {
                "idle": {
                    "path": os.path.join(base_path, "Idle.png"),
                    "frames": 4,
                    "width": frame_width,
                    "height": frame_height
                },
                "walk": {
                    "path": os.path.join(base_path, "Walk.png"),
                    "frames": 4,
                    "width": frame_width,
                    "height": frame_height
                },
                "bomb": {
                    "path": os.path.join(base_path, "Bomb.png"),
                    "frames": 6,
                    "width": frame_width,
                    "height": frame_height
                },
                "landing": {
                    "path": os.path.join(base_path, "Landing.png"),
                    "frames": 16,
                    "width": frame_width,
                    "height": frame_height
                },
                "dead": {
                    "path": os.path.join(base_path, "Death.png"),
                    "frames": 6,
                    "width": frame_width,
                    "height": frame_height
                }
            }
            
        elif enemy_type == "swift_striker":  # Swordsman
            sprite_configs = {
                "idle": {
                    "path": os.path.join(base_path, "Idle.png"),
                    "frames": 5,
                    "width": frame_width,
                    "height": frame_height
                },
                "move": {  # Use enabling animation for movement
                    "path": os.path.join(base_path, "Enabling.png"),
                    "frames": 5,
                    "width": frame_width,
                    "height": frame_height
                },
                "attack": {
                    "path": os.path.join(base_path, "Attack_1.png"),
                    "frames": 4,
                    "width": frame_width,
                    "height": frame_height
                },
                "attack_2": {
                    "path": os.path.join(base_path, "Attack_2.png"),
                    "frames": 2,
                    "width": frame_width,
                    "height": frame_height
                },
                "attack_3": {
                    "path": os.path.join(base_path, "Attack_3.png"),
                    "frames": 2,
                    "width": frame_width,
                    "height": frame_height
                },
                "attack_4": {
                    "path": os.path.join(base_path, "Attack_4.png"),
                    "frames": 2,
                    "width": frame_width,
                    "height": frame_height
                },
                "enabling": {
                    "path": os.path.join(base_path, "Enabling.png"),
                    "frames": 5,
                    "width": frame_width,
                    "height": frame_height
                },
                "shutdown": {
                    "path": os.path.join(base_path, "Shutdown.png"),
                    "frames": 5,
                    "width": frame_width,
                    "height": frame_height
                },
                "pick_up": {
                    "path": os.path.join(base_path, "Pick_up.png"),
                    "frames": 8,
                    "width": frame_width,
                    "height": frame_height
                },
                "hurt": {
                    "path": os.path.join(base_path, "Hurt.png"),
                    "frames": 3,
                    "width": frame_width,
                    "height": frame_height
                },
                "dead": {
                    "path": os.path.join(base_path, "Dead.png"),
                    "frames": 4,
                    "width": frame_width,
                    "height": frame_height
                }
            }
        else:
            # Default fallback
            sprite_configs = {
                "idle": {
                    "path": None,
                    "frames": 1,
                    "width": frame_width,
                    "height": frame_height
                }
            }
        
        return sprite_configs

    @staticmethod
    def get_boss_sprite_configs():
        """Get sprite sheet configurations for boss"""
        base_path = os.path.join(AnimationConfig.ENEMIES_PATH, "boss")
        
        frame_width = 96
        frame_height = 96
        
        sprite_configs = {
            "idle": {
                "path": os.path.join(base_path, "Idle.png"),
                "frames": 4,
                "width": frame_width,
                "height": frame_height
            },
            "walk": {
                "path": os.path.join(base_path, "Walk.png"),
                "frames": 6,
                "width": frame_width,
                "height": frame_height
            },
            "attack_1": {
                "path": os.path.join(base_path, "Attack1.png"),
                "frames": 6,
                "width": frame_width,
                "height": frame_height
            },
            "attack_2": {
                "path": os.path.join(base_path, "Attack2.png"),
                "frames": 6,
                "width": frame_width,
                "height": frame_height
            },
            "attack_3": {
                "path": os.path.join(base_path, "Attack3.png"),
                "frames": 6,
                "width": frame_width,
                "height": frame_height
            },
            "attack_4": {
                "path": os.path.join(base_path, "Attack4.png"),
                "frames": 6,
                "width": frame_width,
                "height": frame_height
            },
            "hurt": {
                "path": os.path.join(base_path, "Hurt.png"),
                "frames": 4,
                "width": frame_width,
                "height": frame_height
            },
            "special": {
                "path": os.path.join(base_path, "Special.png"),
                "frames": 4,
                "width": frame_width,
                "height": frame_height
            },
            "death": {
                "path": os.path.join(base_path, "Death.png"),
                "frames": 6,
                "width": frame_width,
                "height": frame_height
            }
        }    
        return sprite_configs
    
    @staticmethod
    def validate_sprite_configs(sprite_configs):
        """Check if sprite sheet files exist"""
        validated = {}
        missing_files = []
        
        for state, config in sprite_configs.items():
            if config["path"] and os.path.exists(config["path"]):
                validated[state] = config
            else:
                if config["path"]:
                    missing_files.append(config["path"])
                # Create fallback config with proper dimensions
                validated[state] = {
                    "path": None,
                    "frames": config.get("frames", 1),
                    "width": config["width"],
                    "height": config["height"]
                }
        
        if missing_files:
            for file in missing_files:
                print(f"  - {file}")
                
        return validated
    