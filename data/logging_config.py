"""
Configuração do sistema de logging para o jogo Mario
"""

import logging
import os
from datetime import datetime

def setup_game_logging():
    """Configura o sistema de logging para o jogo"""
    
    # Criar diretório de logs se não existir
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Nome do arquivo de log com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f'mario_game_{timestamp}.log')
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # Para ver logs no console também
        ]
    )
    
    # Logger específico para o mapeamento
    map_logger = logging.getLogger('mario_map')
    map_logger.setLevel(logging.INFO)
    
    # Logger específico para colisões
    collision_logger = logging.getLogger('mario_collisions')
    collision_logger.setLevel(logging.INFO)
    
    print(f"Sistema de logging configurado. Logs salvos em: {log_file}")
    
    return log_file

def get_map_logger():
    """Retorna o logger específico para mapeamento"""
    return logging.getLogger('mario_map')

def get_collision_logger():
    """Retorna o logger específico para colisões"""
    return logging.getLogger('mario_collisions')