#!/usr/bin/env python3
"""
Script de teste para verificar se o Level 2 pode ser carregado sem erros
"""

import pygame as pg
import sys
import os

# Adicionar o diretório data ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data'))

from data import constants as c
from data.states import level2
from data import setup

def test_level2_startup():
    """Testa se o Level 2 pode ser inicializado sem erros"""
    print("=== TESTE DE INICIALIZAÇÃO DO LEVEL 2 ===")
    
    try:
        # Inicializar pygame
        pg.init()
        pg.display.set_mode((800, 600))
        
        # Criar instância do Level 2
        level = level2.Level2()
        print("✅ Level2 criado com sucesso")
        
        # Simular dados de persistência (como se viesse do Level 1)
        persist = {
            c.COIN_TOTAL: 0,
            c.SCORE: 1000,
            c.TOP_SCORE: 5000,
            c.LIVES: 3,
            c.CURRENT_TIME: 0.0,
            c.LEVEL_STATE: c.NOT_FROZEN,
            c.CAMERA_START_X: 0,
            c.MARIO_DEAD: False
        }
        
        # Tentar inicializar o Level 2
        current_time = pg.time.get_ticks()
        level.startup(current_time, persist)
        print("✅ Level2.startup() executado com sucesso")
        
        # Verificar se os grupos de sprites foram criados
        required_groups = [
            'ground_group', 'pipe_group', 'step_group', 
            'brick_group', 'coin_box_group', 'enemy_group'
        ]
        
        for group_name in required_groups:
            if hasattr(level, group_name):
                group = getattr(level, group_name)
                print(f"✅ {group_name}: {len(group)} sprites")
            else:
                print(f"❌ {group_name}: não encontrado")
        
        print("\n=== TESTE CONCLUÍDO COM SUCESSO ===")
        return True
        
    except Exception as e:
        print(f"❌ ERRO durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pg.quit()

if __name__ == "__main__":
    success = test_level2_startup()
    sys.exit(0 if success else 1)