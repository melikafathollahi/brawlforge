from src import config
from openai import OpenAI
import threading

class TauntGenerator:
    def __init__(self, on_taunt_callback):
        self.on_taunt_callback = on_taunt_callback
        self.taunt_active = False
        self.lock = threading.Lock()

    def generate_taunt(self, reason):
        """Generate a contextual taunt using OpenAI API"""
        def taunt_thread():
            with self.lock:
                if self.taunt_active:
                   return  
            self.taunt_active = True
            
            client = OpenAI(
                api_key=config.OPENAI_API_KEY,
                base_url=config.OPENAI_BASE_URL
            )
            
            context_map = {
                "player_took_damage": "Generate a taunt when the player gets hit",
                "boss_took_damage": "Generate a defiant response when the boss takes damage",
                "enemy_defeated": "Generate a taunt when minions are defeated",
                "phase_transition": "Generate an intimidating phase transition announcement",
                "intro": "Generate a dramatic boss battle introduction",
                "death": "Generate the boss's final words",
                "attack_1": "Generate a basic attack taunt",
                "attack_2": "Generate a stronger attack taunt",
                "attack_3": "Generate an advanced attack taunt",
                "attack_4": "Generate an ultimate attack taunt",
                "special_attack": "Generate a special move announcement",
                "phase_2": "Generate phase 2 transition dialogue",
                "phase_3": "Generate phase 3 transition dialogue",
                "final_phase": "Generate final phase transition dialogue",
                "boss_low_health": "Generate desperate low health dialogue"
            }
            
            prompt = f"You are a powerful boss in a video game. {context_map.get(reason, 'Generate a taunt')}. Keep it in one sentence, dramatic and fitting for a boss battle."
            
            response = client.chat.completions.create(
                model = config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a sarcastic and dramatic video game boss."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.9
            )
            
            if response.choices and response.choices[0].message:
                taunt_text = response.choices[0].message.content.strip()
                print(f"Generated taunt for {reason}: {taunt_text}")
                self.on_taunt_callback(taunt_text)
            else:
                print("No valid taunt text generated")

        threading.Thread(target=taunt_thread, daemon=True).start()
