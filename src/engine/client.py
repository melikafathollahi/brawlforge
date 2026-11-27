import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.engine.player import Player
from src.engine.map import TileMap
import socket
import pickle
import threading
import pygame
import time
import config
import json
from typing import Dict, List, Any








'''class Player:
    """کلاس موقت برای Player (باید از فایل اصلی import شود)"""
    def __init__(self, player_id, name, team, appearance, position):
        self.player_id = player_id
        self.name = name
        self.team = team
        self.appearance = appearance
        self.position = position
        self.health = 100
        self.status = "alive"
    
    def update(self):
        """بروزرسانی بازیکن"""
        # منطق بروزرسانی بازیکن
        pass
    
    def draw(self, screen, camera_offset=(0, 0)):
        """رسم بازیکن"""
        x = self.position[0] - camera_offset[0]
        y = self.position[1] - camera_offset[1]
        
        # رنگ بر اساس تیم
        color = (255, 0, 0) if self.team == "red" else (0, 0, 255)
        pygame.draw.circle(screen, color, (int(x), int(y)), 20)
        
        # نمایش نام
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, (255, 255, 255))
        screen.blit(text, (x - 30, y - 40))

class TileMap:
    """کلاس موقت برای TileMap (باید از فایل اصلی import شود)"""
    def __init__(self, width=1000, height=600):
        self.width = width
        self.height = height
    
    def draw(self, screen, camera_offset=(0, 0)):
        """رسم نقشه"""
        # رسم زمین ساده
        pygame.draw.rect(screen, (100, 100, 100), 
                        (0 - camera_offset[0], 500 - camera_offset[1], 
                         self.width, 100))'''

class GameClient:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        
        # اطلاعات بازیکن
        self.player_id = None
        self.game_id = None
        
        # آبجکت‌های بازی
        self.this_player = None
        self.other_players_list = []
        self.tilemap = None
        
        # اطلاعات بازی
        self.game_data = {}
        self.bullets = []
        
        # pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Multi Game Client")
        self.clock = pygame.time.Clock()
        
        # ورودی‌ها
        self.keys = {
            'left': False,
            'right': False,
            'up': False,
            'down': False,
            'shoot': False
        }
        
        # دوربین
        self.camera_offset = [0, 0]
        self.map_add="src/assets/map/tileset_4/map4.tmx"
        # وضعیت کلاینت
        self.running = True
        self.in_game = False
    
    def connect_to_server(self) -> bool:
        """اتصال به سرور"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            
            # شروع thread برای دریافت پیام‌ها
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
            
            print(f"✅ متصل شد به سرور {self.host}:{self.port}")
            return True
            
        except Exception as e:
            print(f"❌ خطا در اتصال: {e}")
            return False
    
    def send_message(self, message: Dict[str, Any]):
        """ارسال پیام به سرور"""
        try:
            data = json.dumps(message).encode('utf-8')
            # ارسال طول پیام ابتدا
            length = len(data)
            self.socket.send(length.to_bytes(4, byteorder='big'))
            # ارسال خود پیام
            self.socket.send(data)
        except Exception as e:
            print(f"❌ خطا در ارسال پیام: {e}")
    
    def receive_message(self) -> Dict[str, Any]:
        """دریافت پیام از سرور"""
        try:
            # دریافت طول پیام
            length_data = self.socket.recv(4)
            if not length_data:
                return None
            
            length = int.from_bytes(length_data, byteorder='big')
            
            # دریافت خود پیام
            data = b''
            while len(data) < length:
                chunk = self.socket.recv(length - len(data))
                if not chunk:
                    return None
                data += chunk
            
            return json.loads(data.decode('utf-8'))
        except Exception as e:
            return None
    
    def receive_messages(self):
        """دریافت مداوم پیام‌ها از سرور"""
        while self.connected:
            try:
                message = self.receive_message()
                if message:
                    self.handle_server_message(message)
                else:
                    break
            except Exception as e:
                print(f"❌ خطا در دریافت پیام: {e}")
                break
        
        self.connected = False
    
    def handle_server_message(self, message: Dict[str, Any]):
        """مدیریت پیام‌های دریافتی از سرور"""
        msg_type = message.get("type")
        
        if msg_type == "game_update":
            self.update_game_data(message.get("data", {}))
    
    def update_game_data(self, game_data: Dict[str, Any]):
        """بروزرسانی اطلاعات بازی"""
        self.game_data = game_data
        self.bullets = game_data.get("bullets", [])
        
        # بروزرسانی بازیکن‌ها
        players_data = game_data.get("players", [])
        
        # پیدا کردن خودم
        my_data = None
        others_data = []
        
        for player_data in players_data:
            if player_data["player_id"] == self.player_id:
                my_data = player_data
            else:
                others_data.append(player_data)
        
        # بروزرسانی this_player
        if my_data and self.this_player:
            self.this_player.position = my_data["position"]###############################################################33
            self.this_player.health = my_data["health"]
            self.this_player.status = my_data["status"]
        
        # بروزرسانی other_players
        # ابتدا لیست جدید می‌سازیم
        new_other_players = []
        for other_data in others_data:
            # بررسی اینکه این بازیکن قبلاً وجود داشته یا نه
            existing_player = None
            for existing in self.other_players_list:
                if existing.player_id == other_data["player_id"]:
                    existing_player = existing
                    break
            
            if existing_player:
                # بروزرسانی بازیکن موجود
                existing_player.position = other_data["position"]##################################################################3
                existing_player.health = other_data["health"]
                existing_player.status = other_data["status"]
                new_other_players.append(existing_player)
            else:
                # ایجاد بازیکن جدی
                pos=other_data["position"]

                new_player = Player(pos[0],pos[1])
                '''player_id=other_data["player_id"],
                    name=other_data["name"],
                    team=other_data["team"],
                    appearance=other_data["appearance"],'''
                new_other_players.append(new_player)
        
        self.other_players_list = new_other_players
    
    def join_game(self, game_id: str, player_name: str, team: str = "red"):
        """پیوستن به بازی"""
        message = {
            "type": "join_game",
            "game_id": game_id,
            "player_name": player_name,
            "team": team,
            "appearance": "default",
            "initial_position": [700, 700]
        }
        
        self.send_message(message)
        
        # انتظار برای پاسخ (در حالت واقعی باید async باشد)
        time.sleep(0.1)
        
        # اگر join موفق بود، player_id را از پاسخ سرور دریافت می‌کنیم
        # اینجا فرض می‌کنیم موفق بوده
        self.game_id = game_id
        # player_id باید از پاسخ سرور دریافت شود
    
    def game_loop(self, game_id: str):
        """حلقه اصلی بازی"""
        self.game_id = game_id
        
        # مقداردهی اولیه (فرضی)
        if not self.this_player:
            '''self.this_player = Player("temp_id", "Me", "red", "default", [100, 100])'''
            pos=[700,700]
            self.this_player=Player(pos[0],pos[1])
        
        if not self.tilemap:
            self.tilemap = TileMap(self.map_add)
        
        self.in_game = True
        
        while self.running and self.in_game:
            # 1. هندل ورودی کاربر و ارسال به سرور
            self.handle_input_and_send_to_server()
            
            # 2. دریافت اطلاعات جدید از سرور (انجام می‌شود در thread جداگانه)
            
            # 3. آپدیت تیرها (شلیک و برخورد)
            self.update_bullets()
            
            # 4. آپدیت بازیکن‌ها (با اطلاعات جدید)
            if self.this_player:
                self.this_player.update(self.tilemap.get_collision_tiles())
            
            for player in self.other_players_list:
                player.update(self.tilemap.get_collision_tiles())
            
            # 5. رسم همه چیز
            '''self.draw_everything()'''
            
            # کنترل FPS
            '''self.clock.tick(60)'''
        
        self.in_game = False
    
    def handle_input_and_send_to_server(self):
        """مدیریت ورودی و ارسال به سرور"""
        # بروزرسانی کلیدها
        keys = pygame.key.get_pressed()
        
        self.keys['left'] = keys[pygame.K_LEFT] or keys[pygame.K_a]
        self.keys['right'] = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        self.keys['up'] = keys[pygame.K_UP] or keys[pygame.K_w]
        self.keys['down'] = keys[pygame.K_DOWN] or keys[pygame.K_s]
        self.keys['shoot'] = keys[pygame.K_SPACE]
        
        # محاسبه موقعیت جدید بر اساس ورودی
        if self.this_player:
            new_position = self.this_player.rect.center
            
            if self.keys['left']:
                new_position[0] -= 5
            if self.keys['right']:
                new_position[0] += 5
            if self.keys['up']:
                new_position[1] -= 5
            if self.keys['down']:
                new_position[1] += 5
            
            # ارسال موقعیت جدید به سرور
            input_message = {
                "type": "player_input",
                "player_id": self.player_id,
                "input_data": {
                    "position": new_position,
                    "keys": self.keys
                }
            }
            
            self.send_message(input_message)
            
            # اگر شلیک زده شد
            if self.keys['shoot']:
                shoot_message = {
                    "type": "player_action",
                    "player_id": self.player_id,
                    "action": "shoot",
                    "action_data": {
                        "position": self.this_player.rect.center,###############################################3
                        "direction": [1, 0],  # سمت راست (باید بر اساس جهت بازیکن باشد)
                        "speed": 10,
                        "damage": 25
                    }
                }
                
                self.send_message(shoot_message)
    
    def update_bullets(self):
        """بروزرسانی تیرها"""
        # منطق بروزرسانی موقعیت تیرها
        # بررسی برخوردها
        # حذف تیرهای منقضی شده
        pass
    
    def update_camera(self):
        """بروزرسانی دوربین"""
        if self.this_player:
            target_x = self.this_player.centerx - 400  # وسط صفحه
            target_y = self.this_player.centery- 300
            
            # صاف کردن حرکت دوربین
            self.camera_offset[0] += (target_x - self.camera_offset[0]) * 0.1
            self.camera_offset[1] += (target_y - self.camera_offset[1]) * 0.1

    def draw_everything(self):
        """رسم همه عناصر بازی"""
        # پاک کردن صفحه
        self.screen.fill((50, 50, 100))  # پس‌زمینه آبی تیره
        
        # بروزرسانی دوربین
        self.update_camera()
        
        # رسم نقشه
        if self.tilemap:
            self.tilemap.draw(self.screen, self.camera_offset)
        
        # رسم تیرها
        for bullet in self.bullets:
            bullet_x = bullet["position"][0] - self.camera_offset[0]
            bullet_y = bullet["position"][1] - self.camera_offset[1]
            pygame.draw.circle(self.screen, (255, 255, 0), (int(bullet_x), int(bullet_y)), 3)
        
        # رسم بازیکن‌های دیگر
        for player in self.other_players_list:
            player.draw(self.screen, self.camera_offset)

# رسم خودم
        if self.this_player:
            self.this_player.draw(self.screen, self.camera_offset)
        
        # رسم UI
        self.draw_ui()
        
        # نمایش صفحه
        pygame.display.flip()
    
    def draw_ui(self):
        """رسم رابط کاربری"""
        font = pygame.font.Font(None, 36)
        
        if not self.in_game:
            # منوی اصلی
            title = font.render("Multi Game Client", True, (255, 255, 255))
            self.screen.blit(title, (300, 200))
            
            instruction = font.render("Press ENTER to join game", True, (255, 255, 255))
            self.screen.blit(instruction, (250, 300))
        else:

# اطلاعات بازی
            if self.this_player:
                health_text = f"Health: {self.this_player.health}"
                health_surface = font.render(health_text, True, (255, 255, 255))
                self.screen.blit(health_surface, (10, 10))
            
            players_count = len(self.other_players_list) + (1 if self.this_player else 0)
            players_text = f"Players: {players_count}"
            players_surface = font.render(players_text, True, (255, 255, 255))
            self.screen.blit(players_surface, (10, 50))
    
    '''def handle_events(self):
        """مدیریت رویدادهای pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.in_game:
                        self.in_game = False
                    else:
                        self.running = False
                        return False

                
                elif event.key == pygame.K_RETURN and not self.in_game:
                    # پیوستن به بازی
                    if self.connect_to_server():
                        self.join_game("default_game", "Player1")
                        # شروع game loop در thread جداگانه
                        game_thread = threading.Thread(
                            target=self.game_loop, 
                            args=("default_game",), 
                            daemon=True
                        )
                        game_thread.start()
                        self.game_loop("default_game")
        
        return True

    


    def run(self):
        """اجرای کلاینت"""
        print("🎮 کلاینت شروع شد!")
        print("ENTER: پیوستن به بازی")
        print("ESC: خروج")
        
        while self.running:
            # مدیریت رویدادها
            if not self.handle_events():
                break
            
            # اگر در بازی نیستیم، فقط منو نشان بده
            if not self.in_game:
                self.screen.fill((50, 50, 100))
                self.draw_ui()
                pygame.display.flip()
            else:
                self.handle_events()
            # کنترل FPS
            self.clock.tick(60)

# پاکسازی
        if self.connected:
            self.socket.close()
        pygame.quit()
        print("👋 کلاینت بسته شد")
        self.handle_events()'''
   
   
    def handle_events(self):
        """مدیریت رویدادهای pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.in_game:
                        self.in_game = False
                    else:
                        self.running = False
                        return False
            
                elif event.key == pygame.K_RETURN and not self.in_game:
                    # پیوستن به بازی
                    if self.connect_to_server():
                        self.join_game("default_game", "Player1")
                        # شروع game loop در thread جداگانه
                        game_thread = threading.Thread(
                            target=self.game_loop, 
                            args=("default_game",), 
                            daemon=True
                        )
                        game_thread.start()
    
        return True



    def run(self):
         """اجرای کلاینت"""
         print("🎮 کلاینت شروع شد!")
         print("ENTER: پیوستن به بازی")
         print("ESC: خروج")
    
         while self.running:
        # مدیریت رویدادها
            if not self.handle_events():
                break
        
        # اگر در بازی نیستیم، فقط منو نشان بده
            if not self.in_game:
              self.screen.fill((50, 50, 100))
              self.draw_ui()
              pygame.display.flip()
        
        # کنترل FPS
            self.clock.tick(60)

    # پاکسازی
         if self.connected:
            self.socket.close()
         pygame.quit()
         print("👋 کلاینت بسته شد")

# اجرای کلاینت
#if name == "main":
'''client = GameClient("localhost", 5000)
try:
        client.handle_events()
except KeyboardInterrupt:
        print("\n🛑 کلاینت متوقف شد")
except Exception as e:
        print(f"❌ خطا: {e}")'''
client=GameClient()
'''if client.connect_to_server():
    client.join_game("test_game","player1")
    client.game_loop("test_game")'''
client.run()