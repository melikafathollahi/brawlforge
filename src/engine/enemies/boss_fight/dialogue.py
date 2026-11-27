import pygame
from src import config
from src import utils
# Add typing sound effect later 
class DialogueBox:
    def __init__(self, pos, text, font_color=(255, 255, 255), font_size=24, typing_speed=50, on_finish_typing = None):
        
        self.img = utils.load_image(config.DIALOGUE_BOX_IMAGE)
            
        self.pos = pos
        self.text = text
        self.font = pygame.font.Font(config.FONT_PATH, font_size)
        self.font_color = font_color

        self.typing_speed = typing_speed  # in milliseconds
        self.last_typing_time = pygame.time.get_ticks()
        self.char_index = 0
        self.typing_done = False

        self.pop_progress = 0.0
        self.pop_duration = 300
        self.pop_start_time = pygame.time.get_ticks()

        self.lines = self.wrap_text(self.text, self.font)

        self.on_finish_typing = on_finish_typing


    def wrap_text(self, text, font, max_words_in_line=6):
        words = text.split(' ')
        lines = []
        while words:
            line_words = words[:max_words_in_line]
            lines.append(' '.join(line_words))
            words = words[max_words_in_line:]
        return lines
    

    def typing_effect(self):
        current_time = pygame.time.get_ticks()
        if not self.typing_done and current_time - self.last_typing_time >= self.typing_speed:
            self.last_typing_time = current_time
            self.char_index += 1
            total_length = sum(len(line) for line in self.lines)
            if self.char_index >= total_length:
                self.typing_done = True
                if self.on_finish_typing:
                    self.on_finish_typing()
                    

    def draw(self, surface):
        box_height = len(self.lines) * self.font.get_linesize() + 20
        box_width = max(self.font.size(line)[0] for line in self.lines) + 20  
        scaled_img_width = int(box_width * (self.pop_progress ** 0.5))
        scaled_img_height = int(box_height * (self.pop_progress ** 0.5))

        self.pop_progress = min(1.0, (pygame.time.get_ticks() - self.pop_start_time) / self.pop_duration)
        if self.pop_progress < 1.0:
            self.img.set_alpha(int(255 * self.pop_progress))
        else:
            self.img.set_alpha(255)

        scaled_img = pygame.transform.smoothscale(self.img, (scaled_img_width, scaled_img_height))
        surface.blit(scaled_img, self.pos)

        if self.pop_progress >= 1.0:
            self.typing_effect()
            chars_remaining = self.char_index
            for i, line in enumerate(self.lines):
                render_length = min(len(line), chars_remaining)
                line_surface = self.font.render(line[:render_length], True, self.font_color)
                surface.blit(line_surface, (self.pos[0] + 10, self.pos[1] + 10 + i * self.font.get_linesize()))
                chars_remaining -= render_length
                if chars_remaining <= 0:
                    break
