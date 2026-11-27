# Display configuration
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 660
FPS = 60    

# UI Configuration
DIALOGUE_BOX_IMAGE = "src/assets/images/enemies/boss/BossUI/dialogue_box.png"
FONT_PATH = "src/assets/fonts/Diviko.ttf"
DIJON_YELLOW = (193, 150, 40)
BUTTON_TEXT_COLOR = (255, 255, 255)

#map
TILESIZE = 16
LEFT= 200
RIGHT= 2600
BOTTOM= 20000

# Player configuration
PLAYER_SPEED = 7
PLAYER_WIDTH = 100 # Adjusted for player sprite size
PLAYER_HEIGHT = 100  # Adjusted for player sprite size
PLAYER_DAMAGE = 10
PLAYER_BULLET_SPEED = 15
PLAYER_JUMP_HEIGHT = 16
PLAYER_HEALTH_WIDTH = 80
PLAYER_HEALTH_HEIGHT = 18

# Player physics
GRAVITY = 0.5
MAX_FALL_SPEED = 10

#bullet
BULLET_IMAGE = "src/assets/images/bullet.png"
BULLET_COLOR = (255, 0, 0)
BULLET_WIDTH = 30
BULLET_HEIGHT = 30
BULLET_DAMAGE = 12
SHOOT_SOUND = "src/assets/sounds/shoot.wav"   #ADD IT LATER
PLAYER_SHOOT_COOLDOWN = 500  # milliseconds

# Enemies configuration
ENEMY_WIDTH = 48
ENEMY_HEIGHT = 48
ENEMY_DAMAGE = 1

BOMB_CHASER_SPEED = 2
BOMB_CHASER_DAMAGE = 20

SNIPER_SHOOT_DELAY = 1000  # milliseconds
SNIPER_BULLET_SPEED = 3
SNIPER_BULLET = "src/assets/images/enemies/Archer/Arrow.png"

FREEZER_SPEED = 1.5
FREEZER_BULLET_SPEED = 5
FREEZER_SHOOT_DELAY = 3000  # milliseconds
FREEZE_DURATION = 3000  # milliseconds
FREEZER_BULLET = "src/assets/images/enemies/freezer/freezer_bullet.png" 

SWIFT_STRIKER_SPEED = 4.5
SWIFT_STRIKER_SHOOT_DELAY = 200 #milliseconds
SWIFT_STRIKER_BULLET_SPEED = 12
SWIFT_STRIKER_BULLET = "src/assets/images/enemies/Swordsman/swordsman_bullet.png"

# Boss configuration
BOSS_HEALTH = 500
BOSS_BAR_WIDTH = 300
BOSS_BAR_HEIGHT = 30
BOSS_WIDTH = 200
BOSS_HEIGHT = 200
BOSS_BULLET = "src/assets/images/enemies/boss/boss_bullet.png"
BOSS_BULLET_SPEED = 6
BOSS_BULLET_COOLDOWN = 200

# OpenAI configuration
OPENAI_API_KEY = "tpsg-il6maQ8wpicDZcIAXP07JZqVJ3qGu4m"
OPENAI_BASE_URL = "https://api.metisai.ir/openai/v1"
OPENAI_MODEL = "gpt-4o-mini"

# NPC Health Bar
NPC_BAR_COLOR = (0, 255, 0)
NPC_BAR_BACK_COLOR = (100, 100, 100)
ENEMY_BAR_WIDTH = 50
ENEMY_BAR_HEIGHT = 10
BULLET_DAMAGE = 0
ENEMY_DAMAGE_COOLDOWN = 1000

#Player Health Bar
HEALTH_BAR_COLOR = (0, 255, 0)
HEALTH_BAR_BACK_COLOR = (100, 100, 100)
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 25

MAX_HEALTH = 100

LEVEL1_MAP = "src/assets/map/tileset_1/map1.tmx"
LEVEL2_MAP = "src/assets/map/tileset_2/map2.tmx"
LEVEL3_MAP = "src/assets/map/tileset_3/map3.tmx"
LEVEL4_MAP = "src/assets/map/tileset_4/map4.tmx"   


# Game states
# Loading screen
LOADING_SCREEN_BACKGROUND = "src/assets/images/UI/Loading_Screen/Background.png"
LOADING_Bar = "src/assets/images/UI/Loading_Screen/Loading_Bar.png"
LOADING_BAR_BG = "src/assets/images/UI/Loading_Screen/Loading_Bar_BG.png"
LOADING_ICON = "src/assets/images/UI/Loading_Screen/Loading_icon.png"

# select mode
SELECT_MODE_BACKGROUND = "src/assets/images/UI/Settings/Description_Area.png"
BUTTON_IMAGE = "src/assets/images/UI/Main_menu/Button_BG.png"
BUTTON_HIGHLIGHT_IMAGE = "src/assets/images/UI/Main_menu/Button_BG_shadow.png"


# Win/Lose states
WIN_BACKGROUND = "src/assets/images/UI/Victory/Victory panel Preset.png"
GAME_OVER_BACKGROUND = "src/assets/images/UI/Mission Failed/BG Preset.png"
WIN_MENU_BUTTON = "src/assets/images/UI/Victory/BTN MENU.png"
RETRY_BUTTON = "src/assets/images/UI/Mission Failed/BTN Retry.png"


# Pause menu
PAUSE_MENU_BACKGROUND = "src/assets/images/UI/Pause_menu/PAUSE_PRESET.png"
PAUSE_IMG = "src/assets/images/UI/Pause_menu/Pause.png"
PAUSE_BACKGROUND = "src/assets/images/UI/Pause_menu/BG.png"
RESUME_BUTTON_IMAGE = "src/assets/images/UI/Pause_menu/BTN_BACK.png"
QUIT_BUTTON_IMAGE = "src/assets/images/UI/Pause_menu/BTN MENU.png"


# Back Button
BACK_BUTTON_IMAGE = "src/assets/images/UI/Pause_menu/BTN_BACK.png"

#Continue Button
CONTINUE_BUTTON_IMAGE = "src/assets/images/UI/Pause_menu/Continue.png"

#Start Button
START_BUTTON_IMAGE = "src/assets/images/UI/Pause_menu/Start.png"

SELECT_MAP_BACKGROUND = "src/assets/images/UI/Pause_menu/BG.png"
SELECT_PLAYER_BACKGROUND = "src/assets/images/UI/Pause_menu/BG.png"

# multi ui
MULTI_PLAYER_INPUT_BACKGROUND = "src/assets/images/UI/Bonus/Bonus 03.png"
MULTI_PLAYER_INPUT_BOX = "src/assets/images/UI/Minimap/Minimap BG.png"
ENTER_NAME_FONT = "src/assets/fonts/Toonway.ttf"
NAME_FONT = "src/assets/fonts/Sline.ttf"
INPUT_RECT = "src/assets/images/UI/Settings/Bar BG.png"
INPUT_SELECTED_RECT = "src/assets/images/UI/Settings/Bar.png"
OK_BUTTON = "src/assets/images/UI/Victory/BTN OK.png"

# online multi ui
PLAY_BUTTON = "src/assets/images/UI/Main_menu/BTN PLAY.png"
SEARCH_BG = "src/assets/images/UI/search_bg.png"

# Power-ups
PU_SHIELD_IMG = "src/assets/images/power_up/Life.png"
PU_DOUBLE_JUMP_IMG = "src/assets/images/power_up/Star.png"
PU_BOOST_DAMAGE_IMG = "src/assets/images/power_up/boost_damage.png"

POWERUP_DAMAGE_BOOST = 15

POWERUP_SPAWN_SOUND = "src/assets/sounds/spawn.wav"
POWERUP_COLLECTED_SOUNT = "src/assets/sounds/collected.wav"

LEVEL_MUSIC= {
    "Level1" : "src/assets/sounds/map1.mp3",
    "Level2" : "src/assets/sounds/map2.mp3",
    "Level3" : "src/assets/sounds/map3.mp3",
    "Level4" : "src/assets/sounds/map4.mp3"
}

RESTART_BUTTON_IMAGE = "src/assets/images/UI/restart_button.png"
QUIT_BUTTON_IMAGE = "src/assets/images/UI/quit_button.png"
NEXT_BUTTON_IMAGE = "src/assets/images/UI/next_button.png"