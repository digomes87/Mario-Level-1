"""Sistema de logging para mapear obstáculos e movimentos do Mario
"""

import logging
import os
from datetime import datetime
import pygame as pg
from .logging_config import setup_game_logging, get_map_logger, get_collision_logger

# Configurar logging se ainda não foi configurado
if not logging.getLogger().handlers:
    setup_game_logging()

logger = get_map_logger()
collision_logger = get_collision_logger()

class MapLogger:
    def __init__(self):
        self.logger = logger
        self.collision_logger = collision_logger
        self.obstacles = {}  # Dicionário para armazenar obstáculos registrados
        self.obstacle_registry = {}  # Registry de obstáculos
        self.mario_positions = []  # Lista de posições do Mario
        self.collisions = []  # Lista de colisões registradas
    
    def register_obstacle(self, obstacle_type, x, y, width, height, name="unknown"):
        """Registra um obstáculo no sistema"""
        obstacle_id = f"{obstacle_type}_{x}_{y}"
        obstacle_info = {
            'type': obstacle_type,
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'name': name,
            'rect': pg.Rect(x, y, width, height)
        }
        
        self.obstacle_registry[obstacle_id] = obstacle_info
        self.logger.info(f"OBSTÁCULO REGISTRADO: {obstacle_type} em ({x}, {y}) - Tamanho: {width}x{height} - Nome: {name}")
        
        return obstacle_id
    
    def log_mario_position(self, x, y, state="unknown"):
        """Registra posição atual do Mario"""
        position_info = {
            'x': x,
            'y': y,
            'state': state,
            'timestamp': datetime.now()
        }
        
        self.mario_positions.append(position_info)
        
        # Manter apenas as últimas 100 posições para não sobrecarregar
        if len(self.mario_positions) > 100:
            self.mario_positions.pop(0)
        
        self.logger.debug(f"MARIO POSIÇÃO: ({x:.1f}, {y:.1f}) - Estado: {state}")
    
    def log_collision(self, mario_name, obstacle_type, mario_rect, obstacle_rect, collision_type="unknown"):
        """Registra evento de colisão"""
        self.collision_count += 1
        
        self.logger.warning(
            f"COLISÃO #{self.collision_count}: {mario_name}({mario_rect.x}, {mario_rect.y}) "
            f"com {obstacle_type} em ({obstacle_rect.x}, {obstacle_rect.y}) - "
            f"Tipo: {collision_type}"
        )
    
    def log_level_setup(self, level_name):
        """Registra início de setup de um nível"""
        self.logger.info(f"=== SETUP DO NÍVEL: {level_name} ===")
        self.obstacle_registry.clear()  # Limpar obstáculos do nível anterior
        self.collision_count = 0
    
    def log_sprite_group(self, group_name, sprite_group):
        """Registra todos os sprites de um grupo"""
        count = len(sprite_group)
        self.logger.info(f"GRUPO {group_name}: {count} sprites")
        
        for i, sprite in enumerate(sprite_group):
            if hasattr(sprite, 'rect'):
                self.logger.debug(
                    f"  {group_name}[{i}]: ({sprite.rect.x}, {sprite.rect.y}) "
                    f"- Tamanho: {sprite.rect.width}x{sprite.rect.height}"
                )
    
    def generate_map_summary(self):
        """Gera resumo do mapeamento atual"""
        self.logger.info("=== RESUMO DO MAPEAMENTO ===")
        self.logger.info(f"Total de obstáculos registrados: {len(self.obstacle_registry)}")
        self.logger.info(f"Total de colisões detectadas: {self.collision_count}")
        self.logger.info(f"Posições do Mario registradas: {len(self.mario_positions)}")
        
        # Listar todos os obstáculos
        for obstacle_id, obstacle in self.obstacle_registry.items():
            self.logger.info(
                f"  {obstacle['type']}: ({obstacle['x']}, {obstacle['y']}) "
                f"- {obstacle['width']}x{obstacle['height']} - {obstacle['name']}"
            )
        
        # Última posição do Mario
        if self.mario_positions:
            last_pos = self.mario_positions[-1]
            self.logger.info(
                f"Última posição do Mario: ({last_pos['x']:.1f}, {last_pos['y']:.1f}) "
                f"- Estado: {last_pos['state']}"
            )
    
    def check_mario_near_obstacles(self, mario_rect, distance=50):
        """Verifica obstáculos próximos ao Mario"""
        near_obstacles = []
        
        for obstacle_id, obstacle in self.obstacle_registry.items():
            obstacle_rect = obstacle['rect']
            
            # Calcular distância aproximada
            dx = abs(mario_rect.centerx - obstacle_rect.centerx)
            dy = abs(mario_rect.centery - obstacle_rect.centery)
            
            if dx <= distance and dy <= distance:
                near_obstacles.append(obstacle)
        
        if near_obstacles:
            self.logger.debug(f"Mario próximo a {len(near_obstacles)} obstáculos:")
            for obstacle in near_obstacles:
                self.logger.debug(
                    f"  - {obstacle['type']} em ({obstacle['x']}, {obstacle['y']})"
                )
        
        return near_obstacles

# Instância global do logger
map_logger = MapLogger()