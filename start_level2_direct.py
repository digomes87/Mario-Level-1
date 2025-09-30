#!/usr/bin/env python3
"""
Script para iniciar o jogo diretamente no Level 2
Útil para desenvolvimento e testes sem precisar completar o Level 1
"""

import pygame as pg
import sys
import os

# Adicionar o diretório data ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data'))

from data import constants as c
from data.states import level2
from data import setup, tools

class DirectLevel2Game:
    """Classe para executar o Level 2 diretamente"""
    
    def __init__(self):
        """Inicializa o jogo"""
        pg.init()
        self.screen = pg.display.set_mode(c.SCREEN_SIZE)
        pg.display.set_caption("Mario Level 2 - Teste Direto")
        self.clock = pg.time.Clock()
        self.fps = 60
        
        # Os recursos são carregados automaticamente ao importar setup
        
        # Criar estado do Level 2
        self.level2 = level2.Level2()
        
        # Dados de persistência simulando chegada do Level 1
        self.persist = {
            c.COIN_TOTAL: 5,        # Algumas moedas coletadas
            c.SCORE: 2500,          # Pontuação do Level 1
            c.TOP_SCORE: 10000,     # Melhor pontuação
            c.LIVES: 3,             # Vidas restantes
            c.CURRENT_TIME: 0.0,    # Tempo atual
            c.LEVEL_STATE: c.NOT_FROZEN,
            c.CAMERA_START_X: 0,
            c.MARIO_DEAD: False
        }
        
        # Inicializar Level 2
        current_time = pg.time.get_ticks()
        self.level2.startup(current_time, self.persist)
        
        print("🎮 MARIO LEVEL 2 - TESTE DIRETO")
        print("=" * 40)
        print("Controles:")
        print("  ← → : Mover Mario")
        print("  ↑   : Pular")
        print("  Z   : Correr/Atirar fireball")
        print("  ESC : Sair")
        print("=" * 40)
        print("Level 2 carregado com sucesso!")
        print("Divirta-se testando! 🍄")
    
    def handle_events(self):
        """Gerencia eventos do jogo"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False
        return True
    
    def run(self):
        """Loop principal do jogo"""
        running = True
        
        while running:
            # Gerenciar eventos
            running = self.handle_events()
            
            # Obter teclas pressionadas
            keys = pg.key.get_pressed()
            
            # Atualizar Level 2
            current_time = pg.time.get_ticks()
            self.level2.update(self.screen, keys, current_time)
            
            # Verificar se o level terminou
            if self.level2.done:
                print(f"\n🎉 Level 2 concluído!")
                print(f"Próximo estado: {self.level2.next}")
                print(f"Pontuação final: {self.level2.game_info[c.SCORE]}")
                running = False
            
            # Atualizar display
            pg.display.flip()
            self.clock.tick(self.fps)
        
        # Cleanup
        pg.quit()
        print("\nObrigado por testar o Level 2! 👋")

def main():
    """Função principal"""
    try:
        game = DirectLevel2Game()
        game.run()
    except KeyboardInterrupt:
        print("\n\nJogo interrompido pelo usuário.")
        pg.quit()
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
        pg.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()