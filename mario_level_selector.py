#!/usr/bin/env python3
"""
Mario Level Selector - Escolha qual nível iniciar
Permite iniciar diretamente no Level 1 ou Level 2 para testes e desenvolvimento
"""

import pygame as pg
import sys
import os
import argparse

# Adicionar o diretório data ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data'))

from data import constants as c
from data.states import level1, level2
from data import setup, tools

class MarioLevelSelector:
    """Classe para selecionar e executar níveis específicos"""
    
    def __init__(self, level_number=1, debug_mode=False):
        """
        Inicializa o seletor de níveis
        
        Args:
            level_number (int): Número do nível (1 ou 2)
            debug_mode (bool): Se True, mostra informações de debug
        """
        self.level_number = level_number
        self.debug_mode = debug_mode
        
        # Inicializar pygame
        pg.init()
        self.screen = pg.display.set_mode(c.SCREEN_SIZE)
        pg.display.set_caption(f"Mario Level {level_number} - Seletor Direto")
        self.clock = pg.time.Clock()
        self.fps = 60
        
        # Os recursos são carregados automaticamente ao importar setup
        
        # Criar estado do nível apropriado
        if level_number == 1:
            self.level = level1.Level1()
            self.persist = self._get_level1_persist()
        elif level_number == 2:
            self.level = level2.Level2()
            self.persist = self._get_level2_persist()
        else:
            raise ValueError(f"Nível {level_number} não suportado. Use 1 ou 2.")
        
        # Inicializar nível
        current_time = pg.time.get_ticks()
        self.level.startup(current_time, self.persist)
        
        self._print_welcome_message()
    
    def _get_level1_persist(self):
        """Retorna dados de persistência para Level 1"""
        return {
            c.COIN_TOTAL: 0,
            c.SCORE: 0,
            c.TOP_SCORE: 0,
            c.LIVES: 3,
            c.CURRENT_TIME: 0.0,
            c.LEVEL_STATE: c.NOT_FROZEN,
            c.CAMERA_START_X: 0,
            c.MARIO_DEAD: False
        }
    
    def _get_level2_persist(self):
        """Retorna dados de persistência para Level 2 (simulando chegada do Level 1)"""
        return {
            c.COIN_TOTAL: 8,        # Moedas coletadas no Level 1
            c.SCORE: 3200,          # Pontuação do Level 1
            c.TOP_SCORE: 15000,     # Melhor pontuação
            c.LIVES: 3,             # Vidas restantes
            c.CURRENT_TIME: 0.0,    # Tempo atual
            c.LEVEL_STATE: c.NOT_FROZEN,
            c.CAMERA_START_X: 0,
            c.MARIO_DEAD: False
        }
    
    def _print_welcome_message(self):
        """Imprime mensagem de boas-vindas"""
        print(f"🎮 MARIO LEVEL {self.level_number} - SELETOR DIRETO")
        print("=" * 50)
        print("Controles:")
        print("  ← → : Mover Mario")
        print("  ↑   : Pular")
        print("  Z   : Correr/Atirar fireball")
        print("  ESC : Sair")
        if self.debug_mode:
            print("  D   : Toggle informações de debug")
        print("=" * 50)
        print(f"Level {self.level_number} carregado com sucesso!")
        print(f"Pontuação inicial: {self.persist[c.SCORE]}")
        print(f"Moedas: {self.persist[c.COIN_TOTAL]}")
        print(f"Vidas: {self.persist[c.LIVES]}")
        print("Divirta-se testando! 🍄")
        print()
    
    def handle_events(self):
        """Gerencia eventos do jogo"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False
                elif event.key == pg.K_d and self.debug_mode:
                    self._print_debug_info()
        return True
    
    def _print_debug_info(self):
        """Imprime informações de debug"""
        mario = self.level.mario
        print(f"\n🔍 DEBUG INFO - Level {self.level_number}")
        print(f"Mario Position: ({mario.rect.x}, {mario.rect.y})")
        print(f"Mario State: {mario.state}")
        print(f"Mario Velocity: ({mario.x_vel}, {mario.y_vel})")
        print(f"Level State: {self.level.state}")
        print(f"Score: {self.level.game_info[c.SCORE]}")
        print(f"Coins: {self.level.game_info[c.COIN_TOTAL]}")
        print(f"Lives: {self.level.game_info[c.LIVES]}")
        if hasattr(self.level, 'viewport'):
            print(f"Viewport X: {self.level.viewport.x}")
        print()
    
    def run(self):
        """Loop principal do jogo"""
        running = True
        
        while running:
            # Gerenciar eventos
            running = self.handle_events()
            
            # Obter teclas pressionadas
            keys = pg.key.get_pressed()
            
            # Atualizar nível
            current_time = pg.time.get_ticks()
            self.level.update(self.screen, keys, current_time)
            
            # Verificar se o level terminou
            if self.level.done:
                print(f"\n🎉 Level {self.level_number} concluído!")
                print(f"Próximo estado: {self.level.next}")
                print(f"Pontuação final: {self.level.game_info[c.SCORE]}")
                print(f"Moedas coletadas: {self.level.game_info[c.COIN_TOTAL]}")
                
                if self.level_number == 1 and self.level.next == c.LEVEL2:
                    print("\n🚀 Transição para Level 2 detectada!")
                    print("Para testar Level 2, execute: python mario_level_selector.py --level 2")
                
                running = False
            
            # Atualizar display
            pg.display.flip()
            self.clock.tick(self.fps)
        
        # Cleanup
        pg.quit()
        print(f"\nObrigado por testar o Level {self.level_number}! 👋")

def main():
    """Função principal com argumentos de linha de comando"""
    parser = argparse.ArgumentParser(description="Mario Level Selector - Escolha qual nível iniciar")
    parser.add_argument("--level", "-l", type=int, choices=[1, 2], default=1,
                       help="Número do nível para iniciar (1 ou 2)")
    parser.add_argument("--debug", "-d", action="store_true",
                       help="Ativar modo debug (pressione D durante o jogo)")
    
    args = parser.parse_args()
    
    try:
        game = MarioLevelSelector(args.level, args.debug)
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