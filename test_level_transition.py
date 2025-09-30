#!/usr/bin/env python3
"""
Script de teste para verificar a transição do Level 1 para Level 2
"""

import pygame as pg
import sys
import os

# Adicionar o diretório data ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data'))

from data import constants as c
from data.states import level1, level2
from data import setup

def test_level_transition():
    """Testa a transição do Level 1 para Level 2"""
    print("=== TESTE DE TRANSIÇÃO LEVEL 1 -> LEVEL 2 ===")
    
    try:
        # Inicializar pygame
        pg.init()
        pg.display.set_mode((800, 600))
        
        # Criar instância do Level 1
        level = level1.Level1()
        print("✅ Level1 criado com sucesso")
        
        # Simular dados de persistência iniciais
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
        
        # Inicializar o Level 1
        current_time = pg.time.get_ticks()
        level.startup(current_time, persist)
        print("✅ Level1.startup() executado com sucesso")
        
        # Simular Mario chegando ao castelo (checkpoint '12' na posição x=8775)
        print("\n=== SIMULANDO MARIO CHEGANDO AO CASTELO ===")
        
        # Posicionar Mario próximo ao castelo
        level.mario.rect.x = 8770  # Próximo ao checkpoint '12'
        level.mario.rect.y = 400   # No chão
        level.mario.dead = False
        level.mario.in_castle = False
        
        print(f"Mario posicionado em: x={level.mario.rect.x}, y={level.mario.rect.y}")
        
        # Simular movimento para o checkpoint '12'
        level.mario.rect.x = 8776  # Passar pelo checkpoint '12'
        
        # Verificar se há checkpoint na posição
        for checkpoint in level.check_point_group:
            if checkpoint.name == '12':
                print(f"✅ Checkpoint '12' encontrado na posição: x={checkpoint.rect.x}")
                
                # Simular colisão com checkpoint '12'
                if level.mario.rect.colliderect(checkpoint.rect):
                    print("✅ Mario colidiu com checkpoint '12'")
                    
                    # Simular o que acontece no check_points_check()
                    level.state = c.IN_CASTLE
                    level.mario.kill()
                    level.mario.state = c.STAND
                    level.mario.in_castle = True
                    level.overhead_info_display.state = c.FAST_COUNT_DOWN
                    
                    print("✅ Mario entrou no castelo!")
                    print(f"   Estado do level: {level.state}")
                    print(f"   Mario no castelo: {level.mario.in_castle}")
                    
                    # Simular fim do level
                    level.mario.dead = False
                    level.set_game_info_values()
                    
                    print(f"✅ Próximo estado definido: {level.next}")
                    
                    if level.next == c.LEVEL2:
                        print("🎉 TRANSIÇÃO PARA LEVEL 2 CONFIGURADA COM SUCESSO!")
                        
                        # Testar se Level 2 pode ser carregado com os dados atuais
                        print("\n=== TESTANDO CARREGAMENTO DO LEVEL 2 ===")
                        level2_instance = level2.Level2()
                        level2_instance.startup(current_time, level.persist)
                        print("✅ Level 2 carregado com sucesso!")
                        
                        return True
                    else:
                        print(f"❌ Próximo estado incorreto: {level.next} (esperado: {c.LEVEL2})")
                        return False
                else:
                    print("❌ Mario não colidiu com checkpoint '12'")
                    return False
        
        print("❌ Checkpoint '12' não encontrado")
        return False
        
    except Exception as e:
        print(f"❌ ERRO durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pg.quit()

if __name__ == "__main__":
    success = test_level_transition()
    if success:
        print("\n🎉 TESTE DE TRANSIÇÃO CONCLUÍDO COM SUCESSO!")
        print("O Level 1 está configurado corretamente para transitar para o Level 2.")
    else:
        print("\n❌ TESTE DE TRANSIÇÃO FALHOU!")
        print("Há problemas na configuração da transição Level 1 -> Level 2.")
    
    sys.exit(0 if success else 1)