__author__ = 'justinarmstrong'

import pygame as pg
from .. import constants as c
from ..map_logger import map_logger

class Collider(pg.sprite.Sprite):
    """Invisible sprites placed overtop background parts
    that can be collided with (pipes, steps, ground, etc."""
    def __init__(self, x, y, width, height, name='collider'):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height)).convert()
        
        # Configurar visualização com informações
        self.name = name
        self.collision_count = 0
        
        # Cores diferentes para diferentes tipos de colisores
        color_map = {
            'pipe': c.GREEN,
            'step': c.BLUE,
            'ground': c.BROWN,
            'collider': c.RED
        }
        
        # Usar cor baseada no nome ou vermelho como padrão
        color = color_map.get(name.lower(), c.RED)
        self.image.fill(color)
        
        # Adicionar transparência para melhor visualização
        self.image.set_alpha(128)  # 50% transparente
        
        # Adicionar texto com informações
        font = pg.font.Font(None, 16)
        text_surface = font.render(f"{name}({x},{y})", True, c.WHITE)
        text_rect = text_surface.get_rect()
        
        # Posicionar texto no centro se couber
        if text_rect.width <= width and text_rect.height <= height:
            text_x = (width - text_rect.width) // 2
            text_y = (height - text_rect.height) // 2
            self.image.blit(text_surface, (text_x, text_y))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = None
        
        # Registrar no sistema de logging
        self.obstacle_id = map_logger.register_obstacle(
            obstacle_type='collider',
            x=x, y=y, width=width, height=height,
            name=name
        )
    
    def check_collision(self, mario_rect):
        """Verifica e registra colisão com Mario"""
        if self.rect.colliderect(mario_rect):
            self.collision_count += 1
            map_logger.log_collision(mario_rect, self.obstacle_id, f"{self.name}_collision")
            return True
        return False

