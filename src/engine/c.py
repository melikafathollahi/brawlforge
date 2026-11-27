
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
class GameClient:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        
        self.player_id = None
        self.username = None
        
        self.state = "menu"  
        self.game_id = None
        
        self.this_player = None
        self.other_players = []
        self.game_state = {}
        self.bullets = []

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Multiplayer Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        

        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'green': (0, 255, 0),
            'gray': (128, 128, 128),
            'dark_gray': (64, 64, 64)
        }
        
        self.running = True
        self.countdown_start = None
        self.countdown_duration = 3

        self.map_path="src/assets/map/tileset_4/map4.tmx"
        self.scroll_x= None
        self.scroll_y= None
    

    def connect_to_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
            
            return True
        except Exception as e:
            print(f"Error Connecting server {e}")
            return False
    

    def send_message(self, message: Dict[str, Any]):
        if not self.connected:
            return False
        try:
            data = json.dumps(message).encode('utf-8')
            length = len(data)
            if self.socket:
                self.socket.send(length.to_bytes(4, byteorder='big'))
                self.socket.send(data)
            return True
        except Exception as e:
            print(f" Error Sending Message: {e}")
            return False
    

    def receive_message(self):
        try:
            if self.socket:
                length_data = self.socket.recv(4)
                if not length_data:
                    return None
            
                length = int.from_bytes(length_data, byteorder='big')
            
                data = b''
                while len(data) < length:
                    if self.socket:
                        chunk = self.socket.recv(length - len(data))
                        if not chunk:
                            return None
                        data += chunk
            
                return json.loads(data.decode('utf-8'))
        except:
            return None
    

    def receive_messages(self):
        while self.connected:
            try:
                message = self.receive_message()
                if message:
                    self.handle_server_message(message)
                else:
                    break
            except Exception as e:
                print(f"Error Recieving Message {e}")
                break
        self.connected = False

    
    def handle_server_message(self, message: Dict[str, Any]):
        msg_type = message.get("type")
        
        if msg_type == "game_request":
            self.handle_game_request(message)
        elif msg_type == "game_start":
            self.handle_game_start(message)
        elif msg_type == "game_update":
            self.handle_game_update(message)
        elif msg_type == "game_end":
            self.handle_game_end(message)
        else:
            print(f" Message Recieved: {message}")
    
    
    def handle_game_request(self, message: Dict[str, Any]):
          from_player = message.get("from_player")
          if not from_player:
             print("No Player Information")
             return

          username = from_player.get("username", "Unknown")
          print(f"Request Game From {username} Recieved")
          
          response = input("Do You Accept the Game? (y/n): ").strip()
        
          if response == "y":
                  print(f"Start Game With: {username} !")
                  self.send_message({
                      "type": "respond_game_request",
                      "to_player": from_player,
                      "accepted": True
                  })
          else:
                 print(f"Request Game From {username} Rejected.")
                 self.send_message({
                     "type": "respond_game_request",
                     "to_player": from_player,
                     "accepted": False
                  })
    
    
    def handle_game_start(self, message: Dict[str, Any]):
        self.game_id = message.get("game_id")
        #self.countdown_duration = message.get("countdown_duration", 3)
        #self.countdown_start = time.time()
        self.state = "countdown"
        game_players = message.get("players", [])
        self.setup_game_objects(game_players)
        print(f"Game {self.game_id} Started!")

    
    def handle_game_update(self, message: Dict[str, Any]):
        data = message.get("data", {})
        self.game_state = data

        if "countdown_remaining" in data:
            remaining = data["countdown_remaining"]
            if remaining <= 0 and self.state == "countdown":
              self.state = "in_game"
              print(" Game Started!")
        self.update_game_objects(data)
    

    def handle_game_end(self, message: Dict[str, Any]):
        winner = message.get("winner")
        print(f"Game Ended! The Winner: {winner}")
        self.state = "game_ended"

    
    def setup_game_objects(self, players_data: List[Dict[str, Any]]):
        self.other_players = []

        for player_data in players_data:
            if player_data["id"] == self.player_id:
                print(f" Create this_player: {player_data['username']}")
                self.this_player = Player(
                    player_data["position"][0],
                    player_data["position"][1],
                     character="kitsune"
                )
                
                self.this_player = {
                    "id": player_data["id"],
                    "username": player_data["username"],
                    "team": player_data["team"],
                    "position": player_data["position"],
                    "health": player_data["health"],
                    "alive": player_data["alive"]
                }
            else:
                
                other_player = Player(
                    player_data["position"][0],
                    player_data["position"][1],
                    character="kitsune"
                 )
                
                other_player = {
                    "id": player_data["id"],
                    "username": player_data["username"],
                    "team": player_data["team"],
                    "position": player_data["position"],
                    "health": player_data["health"],
                    "alive": player_data["alive"]
                }
                self.other_players.append(other_player)
    
        print(".............###...............")


    def update_game_objects(self, game_data: Dict[str, Any]):
        players_data = game_data.get("players", [])
        
        for player_data in players_data:
            if player_data["id"] == self.player_id:
                pass
                #if self.this_player:
                    #self.this_player["position"] = player_data["position"]
                    #self.this_player["health"] = player_data["health"]
                    #self.this_player["alive"] = player_data["alive"]
            else:
                for other_player in self.other_players:
                    if other_player["id"] == player_data["id"]:
                        other_player["position"] = player_data["position"]
                        other_player["health"] = player_data["health"]
                        other_player["alive"] = player_data["alive"]
                        break
        
        self.bullets = game_data.get("bullets", [])
    

    def register_player(self):
        print("\n=== Player Register ===")
        username = input(" Enter Your Name: ").strip()
        if not username:
            print("User Name Can't be Empty!")
            return False
         
        message = {
            "type": "register",
            "username": username
        }
        
        if self.send_message(message):
            time.sleep(0.5)
            if self.player_id:
                self.username = username
                print(f"Register Successful! YOur ID: {self.player_id}")
                return True
        
        print("Error Registering")
        return False
    

    def show_main_menu(self):
        """Main Menu"""
        print("\n" + "="*50)
        print(" Main Menu")
        print("="*50)
        print(f" Player: {self.username} (ID: {self.player_id})")
        print("\n1  Searchig Player by ID")
        print("2  Waiting Room (1v1)")
        print("3  Waiting Room(2v2)")
        print("4  Exit")
        print("="*50)
        
        choice = input("Your Choice (1-4): ").strip()
        
        if choice == "1":
            self.search_player()
        elif choice == "2":
            self.join_waiting_room("1v1")
        elif choice == "3":
            self.join_waiting_room("2v2")
        elif choice == "4":
            self.running = False
        else:
            print("Invalid Choice")
    

    def search_player(self):
        print("\n=== Search Player ===")
        search_id = input("Player ID: ").strip().upper()
        
        if not search_id:
            print("ID Can't be Empty!")
            return
        
        message = {
            "type": "find_player",
            "player_id": search_id
        }
        
        self.send_message(message)
        print("Searching ...")
        time.sleep(1) 

    
    def join_waiting_room(self, mode: str):
        print(f"\nJoining Waiting Room {mode}...")
        
        message = {
            "type": "join_waiting_room",
            "player_id": self.player_id,
            "mode": mode
        }
        
        if self.send_message(message):
            self.state = "waiting"
            print("Entered Waiting Room. Keep Waiting...")
            self.waiting_loop()
        else:
            print("Error Entering Waiting Room")
    
    def waiting_loop(self):
        print("Finding Other Players...")
        
        while self.state == "waiting" and self.running and self.connected:
            self.screen.fill(self.colors['dark_gray'])

            waiting_text = self.big_font.render(" Waiting for Other Players ...", True, self.colors['white'])
            text_rect = waiting_text.get_rect(center=(400, 200))
            self.screen.blit(waiting_text, text_rect)
            
            dots = "." * ((int(time.time() * 2) % 4) + 1)
            dots_text = self.font.render(dots, True, self.colors['white'])
            dots_rect = dots_text.get_rect(center=(400, 250))
            self.screen.blit(dots_text, dots_rect)
            
            exit_text = self.font.render("ESC back to the menu", True, self.colors['gray'])
            exit_rect = exit_text.get_rect(center=(400, 500))
            self.screen.blit(exit_text, exit_rect) 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                        return
            
            pygame.display.flip()
            self.clock.tick(60)

    
    def handle_input(self):
        if not self.this_player or self.state != "in_game":
            return
            
        keys = pygame.key.get_pressed()
        
        move_x, move_y = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = 5
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y = -5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y = 5
         
        if move_x != 0 or move_y != 0:
            new_x = self.this_player["position"][0] + move_x
            new_y = self.this_player["position"][1] + move_y
            
            new_x = max(20, min(780, new_x))
            new_y = max(20, min(580, new_y))
            
            self.this_player["position"] = [new_x, new_y]
            
            message = {
                "type": "player_input",
                "player_id": self.player_id,
                "input_data": {
                    "position": [new_x, new_y],
                    "health": self.this_player["health"]
                }
            }
            self.send_message(message)
        
        if keys[pygame.K_SPACE]:
            self.shoot()
    

    def shoot(self):
        if not self.this_player:
            return
            
        direction = [5, 0] if self.this_player["team"] == "red" else [-5, 0]
        
        message = {
            "type": "player_action",
            "player_id": self.player_id,
            "action": "shoot",
            "action_data": {
                "position": self.this_player["position"].copy(),
                "velocity": direction,
                "damage": 25
            }
        }    
        self.send_message(message)
    

    def render_game(self):
        if self.state == "countdown":
            if self.countdown_start:
                elapsed = time.time() - self.countdown_start
                remaining = max(0, self.countdown_duration - elapsed)
                print(f"DEBUG: countdown remaining = {remaining}")

                if remaining > 0:
                    countdown_text = self.big_font.render(str(int(remaining) + 1), True, self.colors['red'])
                    text_rect = countdown_text.get_rect(center=(400, 300))
                    self.screen.blit(countdown_text, text_rect)
                    
                    ready_text = self.font.render("Ready! ", True, self.colors['white'])
                    ready_rect = ready_text.get_rect(center=(400, 200))
                    self.screen.blit(ready_text, ready_rect)
        
        elif self.state == "in_game":
            if self.this_player and self.this_player["alive"]:
                color = self.colors['red'] if self.this_player["team"] == "red" else self.colors['blue']
                pos = self.this_player["position"]
                pygame.draw.circle(self.screen, color, (int(pos[0]), int(pos[1])), 15)
                
                name_text = self.font.render(self.this_player["username"], True, self.colors['white'])
                name_rect = name_text.get_rect(center=(pos[0], pos[1] - 30))
                self.screen.blit(name_text, name_rect)
                
                health_text = self.font.render(f"HP: {self.this_player['health']}", True, self.colors['green'])
                health_rect = health_text.get_rect(center=(pos[0], pos[1] + 30))
                self.screen.blit(health_text, health_rect)
            
            for player in self.other_players:
                if player["alive"]:
                    color = self.colors['red'] if player["team"] == "red" else self.colors['blue']
                    pos = player["position"]
                    pygame.draw.circle(self.screen, color, (int(pos[0]), int(pos[1])), 15)
                    
                    name_text = self.font.render(player["username"], True, self.colors['white'])
                    name_rect = name_text.get_rect(center=(pos[0], pos[1] - 30))
                    self.screen.blit(name_text, name_rect)
            
            for bullet in self.bullets:
                pos = bullet["position"]
                pygame.draw.circle(self.screen, self.colors['white'], (int(pos[0]), int(pos[1])), 3)
            
            controls = [
                "WASD/Arrow Keys: Move",
                "Space: Shoot",
                "ESC: Exit"
            ]
            
            y_offset = 10
            for control in controls:
                text = self.font.render(control, True, self.colors['gray'])
                self.screen.blit(text, (10, y_offset))
                y_offset += 25
        
        elif self.state == "game_ended":
            end_text = self.big_font.render("game Ended!", True, self.colors['white'])
            end_rect = end_text.get_rect(center=(400, 250))
            self.screen.blit(end_text, end_rect)
            
            continue_text = self.font.render("ESC Return Back to Menu", True, self.colors['gray'])
            continue_rect = continue_text.get_rect(center=(400, 350))
            self.screen.blit(continue_text, continue_rect)
        
        pygame.display.flip()
    

    def game_loop(self):
        while self.running and self.connected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state in ["countdown", "in_game", "game_ended"]:
                            self.state = "menu"
                            self.game_id = None
                        elif self.state == "waiting":
                            self.state = "menu"
  
            if self.state == "in_game":
                self.handle_input()
            
            if self.state in ["countdown", "in_game", "game_ended"]:
                self.render_game()
            elif self.state == "waiting":
                pass    
            self.clock.tick(60)
    

    def run(self):
        print(" Start Client")
        if not self.connect_to_server():
            return
        
        print("Connected to the Server")
        if not self.register_player():
            return  
        self.state = "menu"
        
        while self.running and self.connected:
            if self.state == "menu":
                self.show_main_menu()
                time.sleep(0.1)  
            elif self.state == "waiting":
                self.waiting_loop()
            else:
                self.game_loop()
                #break
        pygame.display.flip()
        self.clock.tick(60)

        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        
        pygame.quit()
        print("Bye!")
    
    original_handle_server_message = None
    

    def enhanced_handle_server_message(self, message):
        if message.get("success") is not None:
            if "player_id" in message:
                if message.get("success"):
                    self.player_id = message.get("player_id")
                    self.username = message.get("username")
                else:
                    print(f"{message.get('error')}")
            
            elif message.get("type") == "find_player" or "player" in message:
                if message.get("success"):
                    player = message.get("player", {})
                    print(f" Player Found!:")
                    print(f"   Name: {player.get('username')}")
                    print(f"   ID: {player.get('id')}")
                    print(f"   Status: {player.get('status')}")
                    
                    response = input("\n Do You Want to Request Play a Game? (y/n): ").strip().lower()
                    if response == 'y':
                        request_msg = {
                            "type": "send_game_request",
                            "from_player_id": self.player_id,
                            "to_player_id": player.get('id')
                        }
                        self.send_message(request_msg)
                        print("Request Recieved")
                else:
                    print(f"{message.get('error')}")
            
            else:
                if message.get("success"):
                    print(f" {message.get('message', 'Successful')}")
                else:
                    print(f"{message.get('error', 'Unknown Error')}")
        else:
            if self.original_handle_server_message:
                self.original_handle_server_message(message)
            else:
                msg_type = message.get("type")
                if msg_type == "game_request":
                    self.handle_game_request(message)
                elif msg_type == "game_start":
                    self.handle_game_start(message)
                elif msg_type == "game_update":
                    self.handle_game_update(message)
                elif msg_type == "game_end":
                    self.handle_game_end(message)

if __name__ == "__main__":
    client = GameClient("localhost", 5000)

    client.original_handle_server_message = client.handle_server_message
    client.handle_server_message = client.enhanced_handle_server_message
    
    try:
        client.run()
    except KeyboardInterrupt:
        print("\nclient Closed")