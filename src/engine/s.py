import socket
import threading
import time
import json
import uuid
from typing import Dict, List, Any
from collections import deque
import logging

class GameServer:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.connected_players: Dict[str, Dict[str, Any]] = {}  # player_id -> player_info
        self.clients: Dict[str, socket.socket] = {}  # player_id -> socket
        
        self.games: Dict[str, Dict[str, Any]] = {}  # game_id -> game_info
        
        # Waiting rooms
        self.waiting_rooms = {
            "1v1": deque(),  # صف انتظار تک‌به‌تک
            "2v2": deque()   # صف انتظار دوبه‌دو
        }
        
        self.player_to_game: Dict[str, str] = {}  # player_id -> game_id
        
        self.request_queue = deque()
        self.lock = threading.Lock()

        self.map_path="src/assets/map/tileset_4/map4.tmx"
    
    def generate_player_id(self) -> str:
        """تولید ID یکتا برای بازیکن"""
        return f"P{str(uuid.uuid4()).upper()[:6]}"
    
    def generate_game_id(self) -> str:
        """تولید ID یکتا برای بازی"""
        return f"G{str(uuid.uuid4()).upper()[:6]}"

    def register_player(self, username: str, client_socket: socket.socket) -> str:
        """ثبت بازیکن جدید"""
        player_id = self.generate_player_id()
        
        with self.lock:
            self.connected_players[player_id] = {
                "id": player_id,
                "username": username,
                "status": "online",  # online, in_game, waiting
                "connected_at": time.time()
            }
            self.clients[player_id] = client_socket
        
        print(f"✅ بازیکن جدید ثبت شد: {username} (ID: {player_id})")
        return player_id
    
    def find_player_by_id(self, player_id: str) -> Dict[str, Any]:
        """جستجوی بازیکن با ID"""
        return self.connected_players.get(player_id)
    
    def send_game_request_to_player(self, from_player_id: str, to_player_id: str):
        """ارسال درخواست بازی به بازیکن مشخص"""
        if to_player_id not in self.clients:
            return False
            
        from_player = self.connected_players[from_player_id]
        
        message = {
            "type": "game_request",
            "from_player": {
                "id": from_player_id,
                "username": from_player["username"]
            },
            "message": f"بازیکن {from_player['username']} درخواست بازی داده است"
        }
        
        try:
            self.send_message(self.clients[to_player_id], message)
            return True
        except:
            return False
    
    def add_to_waiting_room(self, player_id: str, mode: str):
        """اضافه کردن بازیکن به صف انتظار"""
        if mode not in self.waiting_rooms:
            return False
            
        with self.lock:
            if player_id not in self.waiting_rooms[mode]:
                self.waiting_rooms[mode].append(player_id)
                self.connected_players[player_id]["status"] = "waiting"
                
        print(f"🔄 بازیکن {player_id} به صف انتظار {mode} اضافه شد")
        self.try_match_players(mode)
        return True
    
    def try_match_players(self, mode: str):
        """تلاش برای تشکیل بازی از صف انتظار"""
        required_players = 2 if mode == "1v1" else 4
        
        with self.lock:
            if len(self.waiting_rooms[mode]) >= required_players:
                # انتخاب بازیکن‌ها از صف
                players = []
                for _ in range(required_players):
                    players.append(self.waiting_rooms[mode].popleft())
                
                # ایجاد بازی جدید
                self.create_matched_game(players, mode)
    
    def create_matched_game(self, player_ids: List[str], mode: str):
        """ایجاد بازی جدید از بازیکن‌های matched شده"""
        game_id = self.generate_game_id()
        
        # تعیین تیم‌ها
        players = []
        for i, player_id in enumerate(player_ids):
            player_info = self.connected_players[player_id].copy()
            
            if mode == "1v1":
                player_info["team"] = "red" if i == 0 else "blue"
            else:  # 2v2
                player_info["team"] = "red" if i < 2 else "blue"
                
            # موقعیت اولیه
            if player_info["team"] == "red":
                player_info["position"] = [700, 1100] if i % 2 == 0 else [650, 1140]
            else:
                player_info["position"] = [750, 1120] if i % 2 == 0 else [600, 1150]
                
            player_info["health"] = 100
            player_info["alive"] = True
            players.append(player_info)
            
            # به‌روزرسانی وضعیت بازیکن
            self.connected_players[player_id]["status"] = "in_game"
            self.player_to_game[player_id] = game_id
        
        # ایجاد بازی
        self.games[game_id] = {
            "id": game_id,
            "mode": mode,
            "status": "countdown",  # countdown, playing, finished  # i change this permenantly
            "players": players,
            "bullets": [],
            "created_at": time.time(),
            "countdown_start": time.time(),
            "winner": None
        }
        
        print(f"بازی جدید ایجاد شد: {game_id} (mode: {mode})")
        
        self.broadcast_game_start(game_id)
    
    def broadcast_game_start(self, game_id: str):
        game = self.games[game_id]
        
        message = {
            "type": "game_start",
            "game_id": game_id,
            "countdown_duration": 3,
            "players": game["players"],
            "mode": game["mode"]
        }
        
        for player in game["players"]:
            player_id = player["id"]
            if player_id in self.clients:
                try:
                    self.send_message(self.clients[player_id], message)
                except:
                    pass
    
    def handle_game(self, game_id: str):#
        """مدیریت یک بازی"""
        if game_id not in self.games:
            return
            
        game = self.games[game_id]
        current_time = time.time()
    
        if game["status"] == "countdown":
            countdown_elapsed = current_time - game["countdown_start"]
            if countdown_elapsed >= 3:
                game["status"] = "playing"
                print(f" بازی {game_id} شروع شد!")

        if game["status"] == "playing":
            
            self.update_bullets(game_id)
            self.check_game_end(game_id)
        
        self.broadcast_game_state(game_id)
    
    def update_bullets(self, game_id: str):
        """آپدیت گلوله‌ها و برخوردها"""
        game = self.games[game_id]
        
        bullets_to_remove = []
        for bullet in game["bullets"]:
            bullet["position"][0] += bullet["velocity"][0]
            bullet["position"][1] += bullet["velocity"][1]
            
            if (bullet["position"][0] < 0 or bullet["position"][0] > 800 or
                bullet["position"][1] < 0 or bullet["position"][1] > 600):
                bullets_to_remove.append(bullet)
        
        for bullet in bullets_to_remove:
            game["bullets"].remove(bullet)
    
    def check_game_end(self, game_id: str):
        game = self.games[game_id]
        
        red_alive = sum(1 for p in game["players"] if p["team"] == "red" and p["alive"])
        blue_alive = sum(1 for p in game["players"] if p["team"] == "blue" and p["alive"])
        
        winner = None
        if red_alive == 0:
            winner = "blue"
        elif blue_alive == 0:
            winner = "red"
        
        if winner:
            game["status"] = "finished"
            game["winner"] = winner
            print(f"🏆 بازی {game_id} تمام شد! برنده: تیم {winner}")
            
            message = {
                "type": "game_end",
                "game_id": game_id,
                "winner": winner
            }
            
            for player in game["players"]:
                if player["id"] in self.clients:
                    try:
                        self.send_message(self.clients[player["id"]], message)
                    except:
                        pass
    
    def broadcast_game_state(self, game_id: str):
        game = self.games[game_id]
        
        message = {
            "type": "game_update",
            "data": {
                "game_id": game_id,
                "status": game["status"],
                "players": game["players"],
                "bullets": game["bullets"],
                "timestamp": time.time()
            }
        }
        
      
        if game["status"] == "countdown":
            elapsed = time.time() - game["countdown_start"]
            message["data"]["countdown_remaining"] = max(0, 3 - elapsed)
        
        disconnected_players = []
        for player in game["players"]:
            player_id = player["id"]
            if player_id in self.clients:
                try:
                    self.send_message(self.clients[player_id], message)
                except:
                    disconnected_players.append(player_id)
        
        for player_id in disconnected_players:
            self.handle_player_disconnect(player_id)
    
    def handle_client(self, client_socket: socket.socket, address):
        player_id = None
        
        try:
            while True:
                message = self.receive_message(client_socket)
                if not message:
                    break
                
                with self.lock:
                    self.request_queue.append((message, client_socket, address))
                
                response = self.process_message(message, client_socket)
                
                if message.get("type") == "register" and response.get("success"):
                    player_id = response.get("player_id")
                    #self.connected_players.append(player_id)#################

                
                if response:
                    self.send_message(client_socket, response)
                    
        except Exception as e:
            print(f"❌ خطا در مدیریت کلاینت {address}: {e}")
        
        finally:
            if player_id:
                self.handle_player_disconnect(player_id)
            
            try:
                client_socket.close()
            except:
                pass
            
            print(f"🔌 کلاینت {address} قطع شد")
    
    def process_message(self, message: Dict[str, Any], client_socket: socket.socket) -> Dict[str, Any]:
        """پردازش پیام دریافتی"""
        msg_type = message.get("type")
        
        if msg_type == "register":
            return self.handle_register(message, client_socket)
        elif msg_type == "find_player":
            return self.handle_find_player(message)
        elif msg_type == "send_game_request":
            return self.handle_send_game_request(message)
        elif msg_type == "respond_game_request":
            return self.handle_respond_game_request(message,client_socket)######################
        elif msg_type == "join_waiting_room":
            return self.handle_join_waiting_room(message)
        elif msg_type == "player_input":
            return self.handle_player_input(message)
        elif msg_type == "player_action":
            return self.handle_player_action(message)
        else:
            return {"success": False, "error": "نوع پیام نامعلوم"}
    
    
        
   
    def handle_register(self, message: Dict[str, Any], client_socket: socket.socket) -> Dict[str, Any]:
        """مدیریت ثبت‌نام بازیکن"""
        username = message.get("username", "").strip()
        if not username:
            return {"success": False, "error": "نام کاربری نمی‌تواند خالی باشد"}
        
        player_id = self.register_player(username, client_socket)
        
        return {
            "success": True,
            "player_id": player_id,
            "username": username,
            "message": "ثبت‌نام با موفقیت انجام شد"
        }
    
    def handle_find_player(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """مدیریت جستجوی بازیکن"""
        search_id = message.get("player_id", "").strip()
        
        player = self.find_player_by_id(search_id)
        if player:
            return {
                "success": True,
                "player": {
                    "id": player["id"],
                    "username": player["username"],
                    "status": player["status"]
                }
            }
        else:
            return {"success": False, "error": "بازیکن با این ID یافت نشد"}
    def handle_respond_game_request(self, message, client):
        
        players=[]
        
        from_player_id = message["to_player"]["id"]
        
        to_player_id = client
        print(f"❌")
    
        players.append(from_player_id)
        players.append(to_player_id)

        self.create_matched_game(players,"1v1")
    '''def handle_respond_game_request(self, message: Dict[str, Any], client_socket: socket.socket) -> Dict[str, Any]:
        accepted = message.get("accepted", False)
        responder_id = message.get("from_player_id")
        requester_id = message.get("to_player_id")

    # Basic validation
        if not responder_id or not requester_id:
             return {"success": False, "error": "اطلاعات بازیکن‌ها ناقص است"}

        if responder_id not in self.connected_players or requester_id not in self.connected_players:
            return {"success": False, "error": "بازیکن‌ها در سرور یافت نشدند"}

    # Notify requester about the decision (optional but nice)
        if requester_id in self.clients:
                try:
                  self.send_message(self.clients[requester_id], {
                     "type": "game_request_response",
                      "from_player_id": responder_id,
                      "accepted": accepted
                   })
                except:
                  pass

        if not accepted:
             print(f"🚫 درخواست بازی از {requester_id} به {responder_id} رد شد")
             return {"success": True, "message": "درخواست رد شد"}

    # Start a 1v1 game with the two players (pass IDs, not dicts or sockets)
        print(f"✅ درخواست بازی پذیرفته شد: {requester_id} در مقابل {responder_id}")
        self.create_matched_game([requester_id, responder_id], "1v1")
        return {"success": True, "message": "بازی ایجاد شد"}'''

    def handle_send_game_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """مدیریت ارسال درخواست بازی"""
        from_player_id = message.get("from_player_id")
        to_player_id = message.get("to_player_id")
        
        if self.send_game_request_to_player(from_player_id, to_player_id):
            return {"success": True, "message": "درخواست ارسال شد"}
        else:
            return {"success": False, "error": "خطا در ارسال درخواست"}
    
    def handle_join_waiting_room(self, message: Dict[str, Any]) -> Dict[str, Any]:
        player_id = message.get("player_id")
        mode = message.get("mode")  
        
        if self.add_to_waiting_room(player_id, mode):
            return {"success": True, "message": f"Added to the Waiting Room {mode}"}
        else:
            return {"success": False, "error": "Error Entering Waiting Room"}
    

    def handle_player_input(self, message: Dict[str, Any]):
        player_id = message.get("player_id")
        input_data = message.get("input_data", {})
        
        if player_id not in self.player_to_game:
            return {"success": False, "error": "Player is Not in Any Game"}
        
        game_id = self.player_to_game[player_id]
        game = self.games.get(game_id)
        
        if not game or game["status"] != "playing":
            return {"success": False, "error": "Game is Not Playing"}
        
        for player in game["players"]:
            if player["id"] == player_id:
                if "position" in input_data:
                    player["position"] = input_data["position"]
                if "health" in input_data:
                    player["health"] = input_data["health"]
                    if player["health"] <= 0:
                        player["alive"] = False
                break
        return {"success": True}
    
    
    def handle_player_action(self, message: Dict[str, Any]):
        player_id = message.get("player_id")
        action = message.get("action")
        action_data = message.get("action_data", {})
        
        if player_id not in self.player_to_game:
            return {"success": False, "error": "Player is Not in Any Game"}
        
        game_id = self.player_to_game[player_id]
        game = self.games.get(game_id)
        
        if not game or game["status"] != "playing":
            return {"success": False, "error": "Game is Not Playing"}
        
        if action == "shoot":
            bullet = {
                "id": str(uuid.uuid4()),
                "owner_id": player_id,
                "position": action_data.get("position", [0, 0]).copy(),
                "velocity": action_data.get("velocity", [5, 0]),\
                "damage": action_data.get("damage", 25)
            }
            game["bullets"].append(bullet)
        return {"success": True}
    
    
    def handle_player_disconnect(self, player_id: str):
        with self.lock:
            if player_id in self.connected_players:
                del self.connected_players[player_id]
            
            if player_id in self.clients:
                del self.clients[player_id]
            
            for mode in self.waiting_rooms:
                if player_id in self.waiting_rooms[mode]:
                    self.waiting_rooms[mode].remove(player_id)
            
            if player_id in self.player_to_game:
                game_id = self.player_to_game[player_id]
                game = self.games.get(game_id)
                
                if game:
                    for player in game["players"]:
                        if player["id"] == player_id:
                            player["alive"] = False
                            player["health"] = 0
                            break
                del self.player_to_game[player_id]
        
        print(f"Player {player_id} Disconnected")
    
    def send_message(self, client_socket: socket.socket, message: Dict[str, Any]):
        try:
            data = json.dumps(message).encode('utf-8')
            length = len(data)
            client_socket.send(length.to_bytes(4, byteorder='big'))
            client_socket.send(data)
        except Exception as e:
            raise e
        
    
    def receive_message(self, client_socket: socket.socket) -> Dict[str, Any]:
        try:
            length_data = client_socket.recv(4)
            if not length_data:
                return None
            
            length = int.from_bytes(length_data, byteorder='big')
            
            data = b''
            while len(data) < length:
                chunk = client_socket.recv(length - len(data))
                if not chunk:
                    return None
                data += chunk
            
            return json.loads(data.decode('utf-8'))
        except:
            return None
        
    
    def game_loop(self):
        while True:
            try:
                for game_id in list(self.games.keys()):
                    self.handle_game(game_id)
                
                finished_games = [
                    game_id for game_id, game in self.games.items()
                    if game["status"] == "finished" and time.time() - game.get("finished_at", 0) > 10
                ]
                
                for game_id in finished_games:
                    del self.games[game_id]
                    print(f"Game {game_id} Deleted")   
                time.sleep(1/60)  
                
            except Exception as e:
                print(f"Error in Main Game Loop: {e}")

    
    def start(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(10)
            print(f"Server Started with {self.host}:{self.port}")
            
            game_thread = threading.Thread(target=self.game_loop, daemon=True)
            game_thread.start()
            
            while True:
                client_socket, address = self.socket.accept()
                print(f"New Client Connected: {address}")
                
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
        except KeyboardInterrupt:
            print("\nServer Closed")
        except Exception as e:
            print(f"Server Error: {e}")
        finally:
            self.socket.close()

if __name__ == "__main__":
    server = GameServer()
    server.start()