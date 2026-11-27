import socket
import threading
import time
import json
import uuid
from typing import Dict, List, Any

class GameServer:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # لیست بازی‌ها
        self.games: Dict[str, Dict[str, Any]] = {}
        
        # لیست کلاینت‌های متصل
        self.clients: Dict[str, socket.socket] = {}  # player_id -> socket
        
        # نگاشت بازیکن به بازی
        self.player_to_game: Dict[str, str] = {}  # player_id -> game_id
    
    def create_game(self, game_id: str, mode: str) -> bool:
        """ایجاد بازی جدید"""
        if game_id in self.games:
            return False
            
        self.games[game_id] = {
            "mode": mode,
            "players": [],
            "status": "waiting",  # waiting, playing, finished
            "bullets": [],
            "game_data": {}  # اطلاعات اضافی بازی
        }
        
        print(f"✅ بازی جدید ایجاد شد: {game_id} (mode: {mode})")
        return True
    
    def add_player_to_game(self, game_id: str, player_data: Dict[str, Any]) -> bool:
        """اضافه کردن بازیکن به بازی"""
        if game_id not in self.games:
            return False
            
        # بررسی اینکه بازیکن قبلاً در بازی نباشد
        for player in self.games[game_id]["players"]:
            if player["player_id"] == player_data["player_id"]:
                return False
        
        self.games[game_id]["players"].append(player_data)
        self.player_to_game[player_data["player_id"]] = game_id
        
        print(f"✅ بازیکن {player_data['name']} به بازی {game_id} اضافه شد")
        return True
    
    def remove_player_from_game(self, player_id: str):
        """حذف بازیکن از بازی"""
        if player_id not in self.player_to_game:
            return
            
        game_id = self.player_to_game[player_id]
        if game_id in self.games:
            # حذف از لیست بازیکن‌ها
            self.games[game_id]["players"] = [
                p for p in self.games[game_id]["players"] 
                if p["player_id"] != player_id
            ]
            
            # اگر بازی خالی شد، حذفش کن
            if len(self.games[game_id]["players"]) == 0:
                del self.games[game_id]
                print(f"🗑️ بازی خالی {game_id} حذف شد")
        
        del self.player_to_game[player_id]
        print(f"🚪 بازیکن {player_id} از بازی خارج شد")
    
    def handle_game(self, game_id: str):
        """مدیریت یک بازی و پخش اطلاعات به بازیکن‌ها"""
        if game_id not in self.games:
            return
            
        game = self.games[game_id]
        
        # جمع‌آوری اطلاعات بازی
        game_state = {###############################################################################         loc?
            "game_id": game_id,
            "mode": game["mode"],
            "status": game["status"],
            "players": game["players"],
            "bullets": game.get("bullets", []),
            "timestamp": time.time()
        }
        
        # ارسال به همه بازیکن‌های این بازی
        message = {
            "type": "game_update",
            "data": game_state
        }
        
        disconnected_players = []
        for player in game["players"]:
            player_id = player["player_id"]
            if player_id in self.clients:
                try:
                    self.send_message(self.clients[player_id], message)
                except:
                    # اگر ارسال ناموفق بود، بازیکن رو برای حذف علامت‌گذاری کن
                    disconnected_players.append(player_id)
        
        # حذف بازیکن‌های قطع شده
        for player_id in disconnected_players:
            self.remove_player_from_game(player_id)
            if player_id in self.clients:
                del self.clients[player_id]
    
    def handle_client(self, client_socket: socket.socket, address):
        """مدیریت کلاینت"""
        player_id = None
        
        try:
            while True:
                # دریافت پیام
                message = self.receive_message(client_socket)
                if not message:
                    break
                
                response = self.process_message(message, client_socket)
                
                # ثبت کلاینت اگر پیام join_game بود
                if message.get("type") == "join_game" and response.get("success"):
                    player_id = response.get("player_id")
                    self.clients[player_id] = client_socket
                
                # ارسال پاسخ
                if response:
                    self.send_message(client_socket, response)
                    
        except Exception as e:
            print(f"❌ خطا در مدیریت کلاینت {address}: {e}")
        
        finally:
            # پاکسازی
            if player_id:
                self.remove_player_from_game(player_id)
                if player_id in self.clients:
                    del self.clients[player_id]
            
            try:
                client_socket.close()
            except:
                pass
            
            print(f"🔌 کلاینت {address} قطع شد")
    
    def process_message(self, message: Dict[str, Any], client_socket: socket.socket) -> Dict[str, Any]:
        """پردازش پیام دریافتی"""
        msg_type = message.get("type")
        
        if msg_type == "create_game":
            return self.handle_create_game(message)
        elif msg_type == "join_game":
            return self.handle_join_game(message)
        elif msg_type == "player_input":
            return self.handle_player_input(message)
        elif msg_type == "player_action":
            return self.handle_player_action(message)
        else:
            return {"success": False, "error": "نوع پیام نامعلوم"}
    
    def handle_create_game(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """مدیریت درخواست ایجاد بازی"""
        game_id = message.get("game_id", str(uuid.uuid4()))
        mode = message.get("mode", "deathmatch")
        
        if self.create_game(game_id, mode):
            return {
                "success": True,
                "game_id": game_id,
                "message": "بازی با موفقیت ایجاد شد"
            }
        else:
            return {
                "success": False,
                "error": "بازی با این شناسه وجود دارد"
            }
    
    def handle_join_game(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """مدیریت درخواست پیوستن به بازی"""
        game_id = message.get("game_id")
        player_name = message.get("player_name", f"Player_{uuid.uuid4().hex[:6]}")
        team = message.get("team", "red")
        appearance = message.get("appearance", "default")
        initial_position = message.get("initial_position", [100, 100])
        
        # اگر بازی وجود نداره، ایجادش کن
        if game_id not in self.games:
            if not self.create_game(game_id, "deathmatch"):
                return {"success": False, "error": "خطا در ایجاد بازی"}
        
        # ایجاد player_id یکتا
        player_id = f"player_{uuid.uuid4().hex[:8]}"
        
        player_data = {
            "player_id": player_id,
            "name": player_name,
            "team": team,
            "appearance": appearance,
            "initial_position": initial_position,
            "health": 100,
            "position": initial_position.copy(),
            "status": "alive"
        }
        
        if self.add_player_to_game(game_id, player_data):
            return {
                "success": True,
                "player_id": player_id,
                "game_id": game_id,
                "message": "با موفقیت به بازی پیوستید"
            }
        else:
            return {
                "success": False,
                "error": "خطا در پیوستن به بازی"
            }
    
    def handle_player_input(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """مدیریت ورودی بازیکن"""
        player_id = message.get("player_id")
        input_data = message.get("input_data", {})
        
        if player_id not in self.player_to_game:
            return {"success": False, "error": "بازیکن در بازی‌ای نیست"}
        
        game_id = self.player_to_game[player_id]
        
        # به‌روزرسانی اطلاعات بازیکن در بازی
        if game_id in self.games:
            for player in self.games[game_id]["players"]:
                if player["player_id"] == player_id:
                    # به‌روزرسانی موقعیت و وضعیت بازیکن
                    if "position" in input_data:
                        player["position"] = input_data["position"]
                    if "health" in input_data:
                        player["health"] = input_data["health"]
                    if "status" in input_data:
                        player["status"] = input_data["status"]
                    break
        
        return {"success": True}
    
    def handle_player_action(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """مدیریت اکشن‌های بازیکن (شلیک، حرکت و ...)"""
        player_id = message.get("player_id")
        action = message.get("action")
        action_data = message.get("action_data", {})
        
        if player_id not in self.player_to_game:
            return {"success": False, "error": "بازیکن در بازی‌ای نیست"}
        
        game_id = self.player_to_game[player_id]
        
        if action == "shoot":
            # اضافه کردن گلوله به بازی
            bullet_data = {
                "id": str(uuid.uuid4()),
                "owner_id": player_id,
                "position": action_data.get("position", [0, 0]),
                "direction": action_data.get("direction", [1, 0]),
                "speed": action_data.get("speed", 10),
                "damage": action_data.get("damage", 25)
            }
            
            if game_id in self.games:
                self.games[game_id]["bullets"].append(bullet_data)
        
        return {"success": True}
    
    def send_message(self, client_socket: socket.socket, message: Dict[str, Any]):#####################################################################
        """ارسال پیام به کلاینت"""
        try:
            data = json.dumps(message).encode('utf-8')
            # ارسال طول پیام ابتدا
            length = len(data)
            client_socket.send(length.to_bytes(4, byteorder='big'))
            # ارسال خود پیام
            client_socket.send(data)
        except Exception as e:
            raise e
    
    def receive_message(self, client_socket: socket.socket) -> Dict[str, Any]:##############################################
        """دریافت پیام از کلاینت"""
        try:
            # دریافت طول پیام
            length_data = client_socket.recv(4)
            if not length_data:
                return None
            
            length = int.from_bytes(length_data, byteorder='big')
            
            # دریافت خود پیام
            data = b''
            while len(data) < length:
                chunk = client_socket.recv(length - len(data))
                if not chunk:
                    return None
                data += chunk
            
            return json.loads(data.decode('utf-8'))
        except Exception as e:
            return None
    
    def game_loop(self):
        """حلقه اصلی بازی"""
        while True:
            try:
                # مدیریت همه بازی‌ها
                for game_id in list(self.games.keys()):##########################################################################################
                    self.handle_game(game_id)
                
                # انتظار کوتاه
                time.sleep(1/60)  # 60 FPS
                
            except Exception as e:
                print(f"❌ خطا در حلقه بازی: {e}")
    
    def start(self):
        """شروع سرور"""
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print(f"🚀 {self.host}:{self.port} ")
            
            # شروع حلقه بازی در thread جداگانه
            game_thread = threading.Thread(target=self.game_loop, daemon=True)
            game_thread.start()
            
            # پذیرش کلاینت‌ها
            while True:
                client_socket, address = self.socket.accept()
                print(f"🔌 کلاینت جدید متصل شد: {address}")
                
                # مدیریت کلاینت در thread جداگانه
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n🛑 سرور بسته شد")
        except Exception as e:
            print(f"❌ خطای سرور: {e}")
        finally:
            self.socket.close()

# اجرای سرور
if __name__ == "__main__":
    server = GameServer("localhost", 5000)
    server.start()