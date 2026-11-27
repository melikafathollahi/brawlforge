
class StateManager:
    def __init__(self, game):
        self.game = game
        self.states = {}
        self.current_state = None
        self.next_state_name = None


    def register_state(self, name, state):
        self.states[name] = state


    def set_state(self, name):
        if name in self.states:
            self.current_state = self.states[name]


    def change_state(self, name):
        self.next_state_name = name


    def update(self):
        if self.next_state_name:
            self.set_state(self.next_state_name)
            self.next_state_name = None


    def run(self, screen, events):
     if self.current_state:
        self.current_state.run(screen, events)
