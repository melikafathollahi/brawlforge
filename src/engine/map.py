import pygame
import pytmx
from src import config
class TileMap:
      
    def __init__(self,address):
       
        self.tmx_data = pytmx.util_pygame.load_pygame(address) # type: ignore
       
    def draw_map(self, screen, scroll_x, scroll_y):
        for layer in self.tmx_data.visible_layers:
            
             if isinstance(layer, pytmx.TiledTileLayer):
               
                for x, y, image in layer.tiles():  
                    if image: 
                        screen.blit(image, (x * config.TILESIZE - scroll_x, y * config.TILESIZE - scroll_y))
        

    def get_collision_tiles(self):
        tile_rects = []
        collision_layer = self.tmx_data.get_layer_by_name("ground")
        if collision_layer is None:
            return []

        for x, y, tile_surface in collision_layer.tiles():
            if tile_surface:
                tile_rect = pygame.Rect(
                    x * config.TILESIZE,
                    y * config.TILESIZE,
                    config.TILESIZE,
                    config.TILESIZE
                )
                tile_rects.append(tile_rect)

        return tile_rects
        
