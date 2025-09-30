from __future__ import division

import logging
import pygame as pg

from .. import constants as c
from .. import game_sound, setup, tools
from ..components import (bricks, castle_flag, checkpoint, coin_box, collider,
                          enemies, flagpole, info, mario, score)
from ..map_logger import map_logger
from ..logging_config import setup_game_logging


class Level2(tools._State):
    """
    Level 2 - Underground Theme
    Uma fase subterrânea mais desafiadora com múltiplas plataformas,
    mais inimigos Koopa e layout vertical mais complexo.
    """

    def __init__(self):
        tools._State.__init__(self)

    def startup(self, current_time, persist):
        """Called when the State object is created"""
        # Configurar sistema de logging
        setup_game_logging()
        
        logger = logging.getLogger(__name__)
        logger.info("=== LEVEL 2 STARTUP INICIADO ===")
        
        # Inicializar sistema de mapeamento
        map_logger.log_level_setup("LEVEL2")
        
        try:
            logger.debug("Inicializando variáveis básicas do Level2")
            self.game_info = persist
            self.persist = self.game_info
            self.game_info[c.CURRENT_TIME] = current_time
            self.game_info[c.LEVEL_STATE] = c.NOT_FROZEN
            self.game_info[c.MARIO_DEAD] = False

            self.state = c.NOT_FROZEN
            self.death_timer = 0
            self.flag_timer = 0
            self.flag_score = None
            self.flag_score_total = 0

            self.moving_score_list = []
            
            logger.debug("Criando OverheadInfo display")
            self.overhead_info_display = info.OverheadInfo(self.game_info, c.LEVEL)
            
            logger.debug("Criando Sound manager")
            self.sound_manager = game_sound.Sound(self.overhead_info_display)

            logger.debug("Configurando background")
            self.setup_background()
            
            logger.debug("Configurando ground (chão)")
            self.setup_ground()
            map_logger.log_sprite_group("GROUND_GROUP", self.ground_group)
            
            logger.debug("Configurando pipes (canos)")
            self.setup_pipes()
            map_logger.log_sprite_group("PIPE_GROUP", self.pipe_group)
            
            logger.debug("Configurando steps (escadas)")
            self.setup_steps()
            map_logger.log_sprite_group("STEP_GROUP", self.step_group)
            
            logger.debug("Configurando bricks (tijolos)")
            self.setup_bricks()
            map_logger.log_sprite_group("BRICK_GROUP", self.brick_group)
            
            logger.debug("Configurando coin boxes (caixas de moedas)")
            self.setup_coin_boxes()
            map_logger.log_sprite_group("COIN_BOX_GROUP", self.coin_box_group)
            
            logger.debug("Configurando flag pole (mastro da bandeira)")
            self.setup_flag_pole()
            
            logger.debug("Configurando enemies (inimigos)")
            self.setup_enemies()
            
            logger.debug("Configurando mario")
            self.setup_mario()
            
            logger.debug("Configurando checkpoints")
            self.setup_checkpoints()
            
            logger.debug("Configurando sprite groups")
            self.setup_spritegroups()
            map_logger.log_sprite_group("ENEMY_GROUP", self.enemy_group)
            
            # Gerar resumo do mapeamento
            map_logger.generate_map_summary()
            
            logger.info("=== LEVEL 2 STARTUP CONCLUÍDO COM SUCESSO ===")
            
        except Exception as e:
            logger.error("=== ERRO CRÍTICO NO LEVEL 2 STARTUP ===")
            logger.error(f"Tipo do erro: {type(e).__name__}")
            logger.error(f"Mensagem do erro: {str(e)}")
            logger.error("Traceback completo:")
            import traceback
            logger.error(traceback.format_exc())
            
            # Print para console também
            print(f"\n{'='*50}")
            print("ERRO CRÍTICO NO LEVEL 2 STARTUP!")
            print(f"{'='*50}")
            print(f"Erro: {type(e).__name__}: {str(e)}")
            print("\nTraceback:")
            traceback.print_exc()
            print(f"{'='*50}\n")
            
            raise

    def setup_background(self):
        """Sets the background image, rect and scales it to the correct proportions"""
        # Reutiliza o mesmo background do level1 para manter consistência visual
        self.background = setup.GFX["level_1"]
        self.back_rect = self.background.get_rect()
        self.background = pg.transform.scale(
            self.background,
            (
                int(self.back_rect.width * c.BACKGROUND_MULTIPLER),
                int(self.back_rect.height * c.BACKGROUND_MULTIPLER),
            ),
        )
        self.back_rect = self.background.get_rect()
        width = self.back_rect.width
        height = self.back_rect.height

        self.level = pg.Surface((width, height)).convert()
        self.level_rect = self.level.get_rect()
        self.viewport = setup.SCREEN.get_rect(bottom=self.level_rect.bottom)
        self.viewport.x = self.game_info[c.CAMERA_START_X]

    def setup_ground(self):
        """Creates collideable, invisible rectangles over top of the ground for sprites to walk on"""
        # Layout de chão contínuo sem gaps para evitar que Mario caia
        ground_rect1 = collider.Collider(0, c.GROUND_HEIGHT, 1800, 60, 'ground_section_1')
        ground_rect2 = collider.Collider(1800, c.GROUND_HEIGHT, 1400, 60, 'ground_section_2')  # Conecta com section_1
        ground_rect3 = collider.Collider(3200, c.GROUND_HEIGHT, 1700, 60, 'ground_section_3')  # Conecta com section_2
        ground_rect4 = collider.Collider(4900, c.GROUND_HEIGHT, 2000, 60, 'ground_section_4')  # Conecta com section_3
        ground_rect5 = collider.Collider(6900, c.GROUND_HEIGHT, 2300, 60, 'ground_section_5')  # Conecta com section_4

        self.ground_group = pg.sprite.Group(
            ground_rect1, ground_rect2, ground_rect3, ground_rect4, ground_rect5
        )

    def setup_pipes(self):
        """Create collideable rects for all the pipes - Aligned with Level 1 background"""
        # Ajustando posições para corresponder ao background do Level 1
        pipe1 = collider.Collider(1202, 452, 83, 82, 'pipe_1')  # Pipe pequeno
        pipe2 = collider.Collider(1631, 409, 83, 140, 'pipe_2')  # Pipe médio
        pipe3 = collider.Collider(1973, 366, 83, 170, 'pipe_3')  # Pipe alto
        pipe4 = collider.Collider(2445, 366, 83, 170, 'pipe_4')  # Pipe alto
        pipe5 = collider.Collider(6989, 452, 83, 82, 'pipe_5')  # Pipe pequeno
        pipe6 = collider.Collider(7675, 452, 83, 82, 'pipe_6')  # Pipe pequeno

        self.pipe_group = pg.sprite.Group(
            pipe1, pipe2, pipe3, pipe4, pipe5, pipe6
        )

    def setup_steps(self):
        """Create collideable rects for all the steps - More complex platform layout"""
        # Plataformas em múltiplos níveis para maior complexidade
        # Plataformas baixas
        step1 = collider.Collider(1000, 495, 40, 40)
        step2 = collider.Collider(1040, 495, 40, 40)
        step3 = collider.Collider(1080, 495, 40, 40)

        # Plataformas médias
        step4 = collider.Collider(1400, 400, 40, 40)
        step5 = collider.Collider(1440, 400, 40, 40)
        step6 = collider.Collider(1480, 360, 40, 40)
        step7 = collider.Collider(1520, 320, 40, 40)

        # Plataformas altas
        step8 = collider.Collider(2400, 320, 40, 40)
        step9 = collider.Collider(2440, 280, 40, 40)
        step10 = collider.Collider(2480, 240, 40, 40)
        step11 = collider.Collider(2520, 200, 40, 40)

        # Mais plataformas espalhadas
        step12 = collider.Collider(3200, 400, 40, 40)
        step13 = collider.Collider(3240, 360, 40, 40)
        step14 = collider.Collider(3280, 320, 40, 40)

        step15 = collider.Collider(4600, 450, 40, 40)
        step16 = collider.Collider(4640, 410, 40, 40)
        step17 = collider.Collider(4680, 370, 40, 40)
        step18 = collider.Collider(4720, 330, 40, 40)

        # Plataformas finais
        step19 = collider.Collider(6400, 400, 40, 40)
        step20 = collider.Collider(6440, 360, 40, 40)
        step21 = collider.Collider(6480, 320, 40, 40)
        step22 = collider.Collider(6520, 280, 40, 40)

        self.step_group = pg.sprite.Group(
            step1,
            step2,
            step3,
            step4,
            step5,
            step6,
            step7,
            step8,
            step9,
            step10,
            step11,
            step12,
            step13,
            step14,
            step15,
            step16,
            step17,
            step18,
            step19,
            step20,
            step21,
            step22,
        )

    def setup_bricks(self):
        """Creates all the breakable bricks for the level - Strategic placement"""
        self.coin_group = pg.sprite.Group()
        self.powerup_group = pg.sprite.Group()
        self.brick_pieces_group = pg.sprite.Group()

        # Grupos de tijolos estrategicamente posicionados
        # Início da fase
        brick1 = bricks.Brick(600, 365)
        brick2 = bricks.Brick(643, 365)
        brick3 = bricks.Brick(686, 365, c.COIN, self.coin_group)
        brick4 = bricks.Brick(729, 365)

        # Área das plataformas médias
        brick5 = bricks.Brick(1300, 280, c.MUSHROOM, self.powerup_group)
        brick6 = bricks.Brick(1343, 280)
        brick7 = bricks.Brick(1386, 280, c.COIN, self.coin_group)

        # Seção elevada
        brick8 = bricks.Brick(2300, 200)
        brick9 = bricks.Brick(2343, 200, c.SIXCOINS, self.coin_group)
        brick10 = bricks.Brick(2386, 200)
        brick11 = bricks.Brick(2429, 200, c.STAR, self.powerup_group)
        brick12 = bricks.Brick(2472, 200)

        # Área intermediária
        brick13 = bricks.Brick(3500, 365)
        brick14 = bricks.Brick(3543, 365, c.COIN, self.coin_group)
        brick15 = bricks.Brick(3586, 365)
        brick16 = bricks.Brick(3629, 365, c.FIREFLOWER, self.powerup_group)

        # Seção de pipes altos
        brick17 = bricks.Brick(4100, 200)
        brick18 = bricks.Brick(4143, 200, c.COIN, self.coin_group)
        brick19 = bricks.Brick(4186, 200)
        brick20 = bricks.Brick(4229, 200, c.COIN, self.coin_group)
        brick21 = bricks.Brick(4272, 200)

        # Área final
        brick22 = bricks.Brick(6800, 365)
        brick23 = bricks.Brick(6843, 365, c.COIN, self.coin_group)
        brick24 = bricks.Brick(6886, 365)
        brick25 = bricks.Brick(6929, 365, c.LIFE_MUSHROOM, self.powerup_group)

        self.brick_group = pg.sprite.Group(
            brick1,
            brick2,
            brick3,
            brick4,
            brick5,
            brick6,
            brick7,
            brick8,
            brick9,
            brick10,
            brick11,
            brick12,
            brick13,
            brick14,
            brick15,
            brick16,
            brick17,
            brick18,
            brick19,
            brick20,
            brick21,
            brick22,
            brick23,
            brick24,
            brick25,
        )

    def setup_coin_boxes(self):
        """Creates all the coin boxes and puts them in a sprite group"""
        # Distribuição estratégica de coin boxes
        coin_box1 = coin_box.Coin_box(500, 365, c.COIN, self.coin_group)
        coin_box2 = coin_box.Coin_box(900, 365, c.MUSHROOM, self.powerup_group)
        coin_box3 = coin_box.Coin_box(1100, 365, c.COIN, self.coin_group)
        coin_box4 = coin_box.Coin_box(1350, 200, c.COIN, self.coin_group)
        coin_box5 = coin_box.Coin_box(2100, 365, c.FIREFLOWER, self.powerup_group)
        coin_box6 = coin_box.Coin_box(2600, 200, c.COIN, self.coin_group)
        coin_box7 = coin_box.Coin_box(3000, 365, c.COIN, self.coin_group)
        coin_box8 = coin_box.Coin_box(3800, 365, c.COIN, self.coin_group)
        coin_box9 = coin_box.Coin_box(4000, 200, c.STAR, self.powerup_group)
        coin_box10 = coin_box.Coin_box(4800, 365, c.COIN, self.coin_group)
        coin_box11 = coin_box.Coin_box(5600, 365, c.MUSHROOM, self.powerup_group)
        coin_box12 = coin_box.Coin_box(6200, 365, c.COIN, self.coin_group)
        coin_box13 = coin_box.Coin_box(6600, 280, c.COIN, self.coin_group)
        coin_box14 = coin_box.Coin_box(7000, 365, c.COIN, self.coin_group)

        self.coin_box_group = pg.sprite.Group(
            coin_box1,
            coin_box2,
            coin_box3,
            coin_box4,
            coin_box5,
            coin_box6,
            coin_box7,
            coin_box8,
            coin_box9,
            coin_box10,
            coin_box11,
            coin_box12,
            coin_box13,
            coin_box14,
        )

    def setup_flag_pole(self):
        """Creates the flag pole at the end of the level"""
        # Posiciona a bandeira no final da fase
        self.flag = flagpole.Flag(8200, 100)

        pole0 = flagpole.Pole(8200, 97)
        pole1 = flagpole.Pole(8200, 137)
        pole2 = flagpole.Pole(8200, 177)
        pole3 = flagpole.Pole(8200, 217)
        pole4 = flagpole.Pole(8200, 257)
        pole5 = flagpole.Pole(8200, 297)
        pole6 = flagpole.Pole(8200, 337)
        pole7 = flagpole.Pole(8200, 377)
        pole8 = flagpole.Pole(8200, 417)
        pole9 = flagpole.Pole(8200, 450)

        finial = flagpole.Finial(8202, 97)

        self.flag_pole_group = pg.sprite.Group(
            self.flag,
            finial,
            pole0,
            pole1,
            pole2,
            pole3,
            pole4,
            pole5,
            pole6,
            pole7,
            pole8,
            pole9,
        )

    def setup_enemies(self):
        """Creates all the enemies - More Koopas for increased difficulty"""
        # Mais inimigos com foco em Koopas para maior dificuldade
        goomba0 = enemies.Goomba()
        goomba1 = enemies.Goomba()
        goomba2 = enemies.Goomba()
        goomba3 = enemies.Goomba()
        goomba4 = enemies.Goomba(193)
        goomba5 = enemies.Goomba(193)
        goomba6 = enemies.Goomba()
        goomba7 = enemies.Goomba()

        # Mais Koopas para aumentar a dificuldade
        koopa0 = enemies.Koopa()
        koopa1 = enemies.Koopa()
        koopa2 = enemies.Koopa()
        koopa3 = enemies.Koopa()
        koopa4 = enemies.Koopa()
        koopa5 = enemies.Koopa()

        # Grupos de inimigos distribuídos pela fase
        enemy_group1 = pg.sprite.Group(goomba0, goomba1)
        enemy_group2 = pg.sprite.Group(koopa0)
        enemy_group3 = pg.sprite.Group(goomba2, koopa1)
        enemy_group4 = pg.sprite.Group(goomba3, goomba4)
        enemy_group5 = pg.sprite.Group(koopa2, koopa3)
        enemy_group6 = pg.sprite.Group(goomba5)
        enemy_group7 = pg.sprite.Group(koopa4)
        enemy_group8 = pg.sprite.Group(goomba6, goomba7)
        enemy_group9 = pg.sprite.Group(koopa5)
        enemy_group10 = pg.sprite.Group(goomba0, koopa0)  # Grupo final misto

        self.enemy_group_list = [
            enemy_group1,
            enemy_group2,
            enemy_group3,
            enemy_group4,
            enemy_group5,
            enemy_group6,
            enemy_group7,
            enemy_group8,
            enemy_group9,
            enemy_group10,
        ]

    def setup_mario(self):
        """Places Mario at the beginning of the level"""
        self.mario = mario.Mario()
        self.mario.rect.x = self.viewport.x + 110
        self.mario.rect.bottom = c.GROUND_HEIGHT

    def setup_checkpoints(self):
        """Creates invisible checkpoints that activate enemies and events"""
        # Checkpoints estratégicos para ativar inimigos
        check1 = checkpoint.Checkpoint(510, "checkpoint1")
        check2 = checkpoint.Checkpoint(1100, "checkpoint2")
        check3 = checkpoint.Checkpoint(1800, "checkpoint3")
        check4 = checkpoint.Checkpoint(2500, "checkpoint4")
        check5 = checkpoint.Checkpoint(3200, "checkpoint5")
        check6 = checkpoint.Checkpoint(4000, "checkpoint6")
        check7 = checkpoint.Checkpoint(4800, "checkpoint7")
        check8 = checkpoint.Checkpoint(5600, "checkpoint8")
        check9 = checkpoint.Checkpoint(6400, "checkpoint9")
        check10 = checkpoint.Checkpoint(7200, "checkpoint10")
        check11 = checkpoint.Checkpoint(8150, "flag_pole")

        self.check_point_group = pg.sprite.Group(
            check1,
            check2,
            check3,
            check4,
            check5,
            check6,
            check7,
            check8,
            check9,
            check10,
            check11,
        )

    def setup_spritegroups(self):
        """Creates the sprite groups and adds them to a list"""
        self.sprites_about_to_die_group = pg.sprite.Group()
        self.shell_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()

        self.ground_step_pipe_group = pg.sprite.Group(
            self.ground_group, self.pipe_group, self.step_group
        )
        self.mario_and_enemy_group = pg.sprite.Group(self.mario, self.enemy_group)

    # Métodos de update e lógica do jogo (reutilizam a mesma lógica do Level1)
    def update(self, surface, keys, current_time):
        """Updates the state every refresh"""
        try:
            self.game_info[c.CURRENT_TIME] = self.current_time = current_time
            self.handle_states(keys)
            self.check_if_time_out()
            self.blit_everything(surface)
            self.sound_manager.update(self.game_info, self.mario)
        except Exception as e:
            print(f"ERRO no Level2.update(): {e}")
            import traceback
            traceback.print_exc()
            raise

    def handle_states(self, keys):
        """Determines the behavior of objects based on game state"""
        try:
            if self.state == c.FROZEN:
                self.update_during_transition_state(keys)
            elif self.state == c.NOT_FROZEN:
                self.update_all_sprites(keys)
            elif self.state == c.IN_CASTLE:
                self.update_while_in_castle()
            elif self.state == c.FLAG_AND_FIREWORKS:
                self.update_flag_and_fireworks()
        except Exception as e:
            print(f"ERRO no Level2.handle_states() - Estado atual: {self.state}: {e}")
            import traceback
            traceback.print_exc()
            raise

    def update_during_transition_state(self, keys):
        """Updates mario in a transition state (like becoming big, small, etc.)"""
        self.mario.update(keys, self.game_info, self.powerup_group)
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.game_info)
        if (
            self.mario.state != c.SMALL_TO_BIG
            and self.mario.state != c.BIG_TO_FIRE
            and self.mario.state != c.BIG_TO_SMALL
        ):
            self.state = c.NOT_FROZEN
            self.mario.state = c.WALK

    def check_if_mario_in_transition_state(self):
        """Checks if mario is in a transition state (becoming big, small, etc.)"""
        if self.mario.state == c.SMALL_TO_BIG:
            self.state = c.FROZEN
        elif self.mario.state == c.BIG_TO_FIRE:
            self.state = c.FROZEN
        elif self.mario.state == c.BIG_TO_SMALL:
            self.state = c.FROZEN

    def update_all_sprites(self, keys):
        """Updates all sprites on the screen"""
        logger = logging.getLogger(__name__)
        
        try:
            logger.debug("Atualizando Mario...")
            self.mario.update(keys, self.game_info, self.powerup_group)
            
            logger.debug("Atualizando moving scores...")
            for score in self.moving_score_list:
                score.update(self.moving_score_list, self.game_info)
            
            logger.debug("Atualizando flag pole group...")
            self.flag_pole_group.update()
            
            logger.debug("Verificando checkpoints...")
            self.check_points_check()
            
            logger.debug("Atualizando enemy group...")
            self.enemy_group.update(self.game_info)
            
            logger.debug("Atualizando sprites about to die group...")
            self.sprites_about_to_die_group.update(self.game_info, self.viewport)
            
            logger.debug("Atualizando shell group...")
            self.shell_group.update(self.game_info)
            
            logger.debug("Atualizando brick group...")
            self.brick_group.update()
            
            logger.debug("Atualizando coin box group...")
            self.coin_box_group.update(self.game_info)
            
            logger.debug("Atualizando powerup group...")
            self.powerup_group.update(self.game_info, self.viewport)
            
            logger.debug("Atualizando coin group...")
            self.coin_group.update(self.game_info, self.viewport)
            
            logger.debug("Atualizando brick pieces group...")
            self.brick_pieces_group.update()
            
            logger.debug("Ajustando posições dos sprites...")
            self.adjust_sprite_positions()
            
            logger.debug("Verificando estado de transição do Mario...")
            self.check_if_mario_in_transition_state()
            
            logger.debug("Verificando morte do Mario...")
            self.check_for_mario_death()
            
            logger.debug("Atualizando viewport...")
            self.update_viewport()
            
            logger.debug("Atualizando overhead info display...")
            self.overhead_info_display.update(self.game_info, self.mario)
            
        except Exception as e:
            logger.error("=== ERRO NO UPDATE_ALL_SPRITES ===")
            logger.error(f"Erro: {type(e).__name__}: {str(e)}")
            logger.error("Traceback:")
            import traceback
            logger.error(traceback.format_exc())
            
            print(f"\n{'='*50}")
            print("ERRO NO UPDATE_ALL_SPRITES!")
            print(f"{'='*50}")
            print(f"Erro: {type(e).__name__}: {str(e)}")
            print("\nTraceback:")
            traceback.print_exc()
            print(f"{'='*50}\n")
            
            raise



    def check_points_check(self):
        """Checks if Mario hits a checkpoint to activate enemies"""
        checkpoint = pg.sprite.spritecollideany(self.mario, self.check_point_group)

        if checkpoint:
            if checkpoint.name == "checkpoint1":
                self.enemy_group.add(self.enemy_group_list[0])
            elif checkpoint.name == "checkpoint2":
                self.enemy_group.add(self.enemy_group_list[1])
            elif checkpoint.name == "checkpoint3":
                self.enemy_group.add(self.enemy_group_list[2])
            elif checkpoint.name == "checkpoint4":
                self.enemy_group.add(self.enemy_group_list[3])
            elif checkpoint.name == "checkpoint5":
                self.enemy_group.add(self.enemy_group_list[4])
            elif checkpoint.name == "checkpoint6":
                self.enemy_group.add(self.enemy_group_list[5])
            elif checkpoint.name == "checkpoint7":
                self.enemy_group.add(self.enemy_group_list[6])
            elif checkpoint.name == "checkpoint8":
                self.enemy_group.add(self.enemy_group_list[7])
            elif checkpoint.name == "checkpoint9":
                self.enemy_group.add(self.enemy_group_list[8])
            elif checkpoint.name == "checkpoint10":
                self.enemy_group.add(self.enemy_group_list[9])
            elif checkpoint.name == "flag_pole":
                self.mario.state = c.FLAGPOLE
                if self.mario.rect.bottom < 485:
                    self.mario.rect.bottom = 485

            checkpoint.kill()

    def adjust_sprite_positions(self):
        """Adjusts sprites for collisions and other purposes"""
        self.adjust_mario_position()
        self.adjust_enemy_position()
        self.adjust_shell_position()
        self.adjust_powerup_position()

    def adjust_mario_position(self):
        """Adjusts Mario's position based on his x, y velocities and
        potential collisions"""
        self.last_x_position = self.mario.rect.right
        self.mario.rect.x += round(self.mario.x_vel)
        self.check_mario_x_collisions()

        if self.mario.in_transition_state == False:
            self.mario.rect.y += round(self.mario.y_vel)
            self.check_mario_y_collisions()

        if self.mario.rect.x < (self.viewport.x + 5):
            self.mario.rect.x = (self.viewport.x + 5)
        
        # Log da posição do Mario e verificação de obstáculos próximos
        map_logger.log_mario_position(self.mario.rect.x, self.mario.rect.y, self.mario.state)
        map_logger.check_mario_near_obstacles(self.mario.rect)

    def check_mario_x_collisions(self):
        """Checks for Mario's horizontal collisions"""
        collider = pg.sprite.spritecollideany(self.mario, self.ground_step_pipe_group)
        coin_box = pg.sprite.spritecollideany(self.mario, self.coin_box_group)
        brick = pg.sprite.spritecollideany(self.mario, self.brick_group)
        enemy = pg.sprite.spritecollideany(self.mario, self.enemy_group)
        shell = pg.sprite.spritecollideany(self.mario, self.shell_group)
        powerup = pg.sprite.spritecollideany(self.mario, self.powerup_group)
        coin = pg.sprite.spritecollideany(self.mario, self.coin_group)

        if coin_box:
            map_logger.log_collision("Mario", "coin_box", self.mario.rect, coin_box.rect, "horizontal")
            self.adjust_mario_for_x_collisions(coin_box)

        elif brick:
            map_logger.log_collision("Mario", "brick", self.mario.rect, brick.rect, "horizontal")
            self.adjust_mario_for_x_collisions(brick)

        elif collider:
            collider_name = getattr(collider, 'name', 'unknown_collider')
            map_logger.log_collision("Mario", collider_name, self.mario.rect, collider.rect, "horizontal")
            self.adjust_mario_for_x_collisions(collider)

        elif enemy:
            if self.mario.invincible or self.mario.test_invincible:
                setup.SFX["kick"].play()
                self.game_info[c.SCORE] += 100
                self.moving_score_list.append(
                    score.Score(enemy.rect.centerx - self.viewport.x, enemy.rect.y, 100)
                )
                enemy.start_death_jump(self.mario.facing)
                self.sprites_about_to_die_group.add(enemy)
                enemy.kill()
            elif self.mario.hurt_invincible:
                pass
            elif self.mario.big:
                setup.SFX["pipe"].play()
                self.mario.fire = False
                self.mario.y_vel = -1
                self.mario.state = c.BIG_TO_SMALL
                self.convert_fireflowers_to_mushrooms()
            elif self.mario.fire:
                setup.SFX["pipe"].play()
                self.mario.fire = False
                self.mario.y_vel = -1
                self.mario.state = c.BIG_TO_SMALL
                self.convert_fireflowers_to_mushrooms()
            else:
                self.mario.start_death_jump(self.game_info)
                self.state = c.FROZEN

        elif shell:
            self.adjust_mario_for_x_shell_collisions(shell)

        elif powerup:
            if powerup.name == c.MUSHROOM:
                setup.SFX["powerup"].play()
                self.game_info[c.SCORE] += 1000
                self.moving_score_list.append(
                    score.Score(
                        powerup.rect.centerx - self.viewport.x, powerup.rect.y, 1000
                    )
                )
                if self.mario.big and self.mario.fire:
                    self.game_info[c.SCORE] += 1000
                    self.moving_score_list.append(
                        score.Score(
                            powerup.rect.centerx - self.viewport.x, powerup.rect.y, 1000
                        )
                    )
                elif self.mario.big:
                    self.mario.fire = True
                    self.mario.state = c.BIG_TO_FIRE
                    self.convert_mushrooms_to_fireflowers()
                else:
                    self.mario.state = c.SMALL_TO_BIG
                powerup.kill()

            elif powerup.name == c.FIREFLOWER:
                setup.SFX["powerup"].play()
                self.game_info[c.SCORE] += 1000
                self.moving_score_list.append(
                    score.Score(
                        powerup.rect.centerx - self.viewport.x, powerup.rect.y, 1000
                    )
                )
                if self.mario.big and self.mario.fire:
                    self.game_info[c.SCORE] += 1000
                    self.moving_score_list.append(
                        score.Score(
                            powerup.rect.centerx - self.viewport.x, powerup.rect.y, 1000
                        )
                    )
                elif self.mario.big:
                    self.mario.fire = True
                    self.mario.state = c.BIG_TO_FIRE
                else:
                    self.mario.state = c.SMALL_TO_BIG
                powerup.kill()

            elif powerup.name == c.STAR:
                setup.SFX["powerup"].play()
                self.game_info[c.SCORE] += 1000
                self.moving_score_list.append(
                    score.Score(
                        powerup.rect.centerx - self.viewport.x, powerup.rect.y, 1000
                    )
                )
                self.mario.invincible = True
                powerup.kill()

            elif powerup.name == c.LIFE_MUSHROOM:
                setup.SFX["one_up"].play()
                self.game_info[c.LIVES] += 1
                self.moving_score_list.append(
                    score.Score(
                        powerup.rect.centerx - self.viewport.x, powerup.rect.y, c.ONEUP
                    )
                )
                powerup.kill()

        elif coin:
            setup.SFX["coin"].play()
            self.game_info[c.SCORE] += 200
            self.game_info[c.COIN_TOTAL] += 1
            self.moving_score_list.append(
                score.Score(coin.rect.centerx - self.viewport.x, coin.rect.y, 200)
            )
            coin.kill()

    def convert_mushrooms_to_fireflowers(self):
        """Converts mushroom powerups to fireflower powerups"""
        for brick in self.brick_group:
            if brick.contents == c.MUSHROOM:
                brick.contents = c.FIREFLOWER
        for coin_box in self.coin_box_group:
            if coin_box.contents == c.MUSHROOM:
                coin_box.contents = c.FIREFLOWER

    def convert_fireflowers_to_mushrooms(self):
        """Converts fireflower powerups to mushroom powerups"""
        for brick in self.brick_group:
            if brick.contents == c.FIREFLOWER:
                brick.contents = c.MUSHROOM
        for coin_box in self.coin_box_group:
            if coin_box.contents == c.FIREFLOWER:
                coin_box.contents = c.MUSHROOM

    def adjust_mario_for_x_collisions(self, collider):
        """Adjusts Mario's position for horizontal collisions"""
        if self.mario.rect.x < collider.rect.x:
            self.mario.rect.right = collider.rect.left
        else:
            self.mario.rect.left = collider.rect.right

        self.mario.x_vel = 0

    def adjust_mario_for_x_shell_collisions(self, shell):
        """Adjusts Mario's position for shell collisions"""
        if shell.state == c.SHELL_SLIDE:
            if self.mario.invincible:
                setup.SFX["kick"].play()
                self.game_info[c.SCORE] += 400
                self.moving_score_list.append(
                    score.Score(shell.rect.centerx - self.viewport.x, shell.rect.y, 400)
                )
                shell.start_death_jump()
                self.sprites_about_to_die_group.add(shell)
                shell.kill()
            elif self.mario.hurt_invincible:
                pass
            elif self.mario.big:
                setup.SFX["pipe"].play()
                self.mario.y_vel = -1
                self.mario.state = c.BIG_TO_SMALL
                self.mario.fire = False
                self.convert_fireflowers_to_mushrooms()
            elif self.mario.fire:
                setup.SFX["pipe"].play()
                self.mario.y_vel = -1
                self.mario.state = c.BIG_TO_SMALL
                self.mario.fire = False
                self.convert_fireflowers_to_mushrooms()
            else:
                self.mario.start_death_jump(self.game_info)
                self.state = c.FROZEN
        else:
            if self.mario.rect.x < shell.rect.x:
                self.mario.rect.right = shell.rect.left
                shell.direction = c.RIGHT
                shell.x_vel = 10
            else:
                self.mario.rect.left = shell.rect.right
                shell.direction = c.LEFT
                shell.x_vel = -10

            shell.rect.x += shell.x_vel
            shell.state = c.SHELL_SLIDE
            setup.SFX["kick"].play()

    def check_mario_y_collisions(self):
        """Checks for Mario's vertical collisions"""
        ground_step_or_pipe = pg.sprite.spritecollideany(
            self.mario, self.ground_step_pipe_group
        )
        enemy = pg.sprite.spritecollideany(self.mario, self.enemy_group)
        shell = pg.sprite.spritecollideany(self.mario, self.shell_group)

        # Check for coin box collision
        coin_box = pg.sprite.spritecollideany(self.mario, self.coin_box_group)
        if coin_box:
            map_logger.log_collision("Mario", "coin_box", self.mario.rect, coin_box.rect, "vertical")
            self.adjust_mario_for_y_coin_box_collisions(coin_box)

        # Check for brick collision
        brick = pg.sprite.spritecollideany(self.mario, self.brick_group)
        if brick:
            map_logger.log_collision("Mario", "brick", self.mario.rect, brick.rect, "vertical")
            self.adjust_mario_for_y_brick_collisions(brick)

        # Check for ground, step, or pipe collision
        if ground_step_or_pipe:
            collider_name = getattr(ground_step_or_pipe, 'name', 'unknown_ground_step_pipe')
            map_logger.log_collision("Mario", collider_name, self.mario.rect, ground_step_or_pipe.rect, "vertical")
            self.adjust_mario_for_y_ground_pipe_collisions(ground_step_or_pipe)

        # Check for enemy collision
        if enemy:
            if self.mario.y_vel > 0:
                self.adjust_mario_for_y_enemy_collisions(enemy)

        # Check for shell collision
        if shell:
            if self.mario.y_vel > 0:
                self.adjust_mario_for_y_shell_collisions(shell)

        self.test_if_mario_is_falling()

    def prevent_collision_conflict(self, obstacle1, obstacle2):
        """Prevents collision conflicts between obstacles"""
        if obstacle1.rect.centerx > obstacle2.rect.centerx:
            obstacle1.rect.left = obstacle2.rect.right
            obstacle1.x_vel = 2
            obstacle1.direction = c.RIGHT
        else:
            obstacle1.rect.right = obstacle2.rect.left
            obstacle1.x_vel = -2
            obstacle1.direction = c.LEFT

    def adjust_mario_for_y_coin_box_collisions(self, coin_box):
        """Adjusts Mario for coin box collisions"""
        if self.mario.rect.y > coin_box.rect.y:
            if coin_box.state != c.OPENED:
                if coin_box.contents == c.COIN:
                    setup.SFX["coin"].play()
                    self.game_info[c.SCORE] += 200
                    coin_box.start_bump(self.moving_score_list)
                else:
                    setup.SFX["powerup_appears"].play()
                    coin_box.start_bump(self.moving_score_list)

                self.game_info[c.COIN_TOTAL] += 1
                self.moving_score_list.append(
                    score.Score(
                        coin_box.rect.centerx - self.viewport.x, coin_box.rect.y, 200
                    )
                )

            self.mario.y_vel = 7
            self.mario.rect.y = coin_box.rect.bottom
            self.mario.state = c.FALL
        else:
            self.mario.y_vel = 0
            self.mario.rect.bottom = coin_box.rect.top
            self.mario.state = c.WALK

    def adjust_mario_for_y_brick_collisions(self, brick):
        """Adjusts Mario for brick collisions"""
        if self.mario.rect.y > brick.rect.y:
            if brick.state == c.RESTING:
                if self.mario.big:
                    setup.SFX["brick_smash"].play()
                    self.check_if_enemy_on_brick(brick)
                    brick.kill()
                    self.game_info[c.SCORE] += 50
                    self.moving_score_list.append(
                        score.Score(
                            brick.rect.centerx - self.viewport.x, brick.rect.y, 50
                        )
                    )
                else:
                    setup.SFX["bump"].play()
                    if brick.contents:
                        if brick.contents == c.COIN:
                            setup.SFX["coin"].play()
                            self.game_info[c.SCORE] += 200
                            brick.start_bump(self.moving_score_list)
                        elif brick.contents == c.SIXCOINS:
                            setup.SFX["coin"].play()
                            brick.start_bump(self.moving_score_list)
                        else:
                            brick.start_bump(self.moving_score_list)
                    else:
                        brick.start_bump(self.moving_score_list)

            self.mario.y_vel = 7
            self.mario.rect.y = brick.rect.bottom
            self.mario.state = c.FALL

        else:
            self.mario.y_vel = 0
            self.mario.rect.bottom = brick.rect.top
            self.mario.state = c.WALK

    def check_if_enemy_on_brick(self, brick):
        """Checks if enemy is on brick when Mario breaks it"""
        brick.rect.y -= 5

        enemy = pg.sprite.spritecollideany(brick, self.enemy_group)

        if enemy:
            setup.SFX["kick"].play()
            self.game_info[c.SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.centerx - self.viewport.x, enemy.rect.y, 100)
            )
            enemy.start_death_jump(c.RIGHT)
            self.sprites_about_to_die_group.add(enemy)
            enemy.kill()

        brick.rect.y += 5

    def adjust_mario_for_y_ground_pipe_collisions(self, collider):
        """Adjusts Mario for ground and pipe collisions"""
        if collider.rect.bottom > self.mario.rect.bottom:
            self.mario.y_vel = 0
            self.mario.rect.bottom = collider.rect.top
            if self.mario.state == c.END_OF_LEVEL_FALL:
                self.mario.state = c.WALKING_TO_CASTLE
            else:
                self.mario.state = c.WALK
        elif collider.rect.top < self.mario.rect.top:
            self.mario.y_vel = 7
            self.mario.rect.top = collider.rect.bottom
            self.mario.state = c.FALL

    def test_if_mario_is_falling(self):
        """Tests if Mario is falling"""
        self.mario.rect.y += 1

        test_collide_group = pg.sprite.Group(
            self.ground_step_pipe_group, self.coin_box_group, self.brick_group
        )

        if pg.sprite.spritecollideany(self.mario, test_collide_group) is None:
            if self.mario.state != c.JUMP:
                self.mario.state = c.FALL

        self.mario.rect.y -= 1

    def adjust_mario_for_y_enemy_collisions(self, enemy):
        """Adjusts Mario for enemy collisions when falling"""
        if enemy.name == c.GOOMBA:
            setup.SFX["stomp"].play()
            self.game_info[c.SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.centerx - self.viewport.x, enemy.rect.y, 100)
            )
            enemy.state = c.JUMPED_ON
            enemy.kill()

        elif enemy.name == c.KOOPA:
            setup.SFX["stomp"].play()
            self.game_info[c.SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.centerx - self.viewport.x, enemy.rect.y, 100)
            )
            enemy.state = c.JUMPED_ON
            enemy.kill()
            shell = enemy.get_shell()
            self.shell_group.add(shell)

        self.mario.rect.bottom = enemy.rect.top
        self.mario.state = c.FALL
        self.mario.y_vel = -7

    def adjust_mario_for_y_shell_collisions(self, shell):
        """Adjusts Mario for shell collisions when falling"""
        if shell.state == c.SHELL_SLIDE:
            setup.SFX["stomp"].play()
            self.game_info[c.SCORE] += 400
            self.moving_score_list.append(
                score.Score(shell.rect.centerx - self.viewport.x, shell.rect.y, 400)
            )
            shell.state = c.RESTING
            shell.x_vel = 0
            self.mario.rect.bottom = shell.rect.top
            self.mario.state = c.FALL
            self.mario.y_vel = -7

    def adjust_enemy_position(self):
        """Adjusts enemy positions"""
        for enemy in self.enemy_group:
            self.check_enemy_x_collisions(enemy)
            self.check_enemy_y_collisions(enemy)
            self.delete_if_off_screen(enemy)

    def check_enemy_x_collisions(self, enemy):
        """Checks enemy horizontal collisions"""
        collider = pg.sprite.spritecollideany(enemy, self.ground_step_pipe_group)
        brick = pg.sprite.spritecollideany(enemy, self.brick_group)
        coin_box = pg.sprite.spritecollideany(enemy, self.coin_box_group)
        enemy2 = pg.sprite.spritecollideany(enemy, self.enemy_group)
        shell = pg.sprite.spritecollideany(enemy, self.shell_group)

        if collider:
            if enemy.direction == c.RIGHT:
                enemy.rect.right = collider.rect.left
                enemy.direction = c.LEFT
                enemy.x_vel = -2
            elif enemy.direction == c.LEFT:
                enemy.rect.left = collider.rect.right
                enemy.direction = c.RIGHT
                enemy.x_vel = 2

        elif brick:
            if enemy.direction == c.RIGHT:
                enemy.rect.right = brick.rect.left
                enemy.direction = c.LEFT
                enemy.x_vel = -2
            elif enemy.direction == c.LEFT:
                enemy.rect.left = brick.rect.right
                enemy.direction = c.RIGHT
                enemy.x_vel = 2

        elif coin_box:
            if enemy.direction == c.RIGHT:
                enemy.rect.right = coin_box.rect.left
                enemy.direction = c.LEFT
                enemy.x_vel = -2
            elif enemy.direction == c.LEFT:
                enemy.rect.left = coin_box.rect.right
                enemy.direction = c.RIGHT
                enemy.x_vel = 2

        elif enemy2:
            if enemy.direction == c.RIGHT:
                enemy.rect.right = enemy2.rect.left
                enemy.direction = c.LEFT
                enemy.x_vel = -2
            elif enemy.direction == c.LEFT:
                enemy.rect.left = enemy2.rect.right
                enemy.direction = c.RIGHT
                enemy.x_vel = 2

        elif shell:
            if shell.state == c.SHELL_SLIDE:
                setup.SFX["kick"].play()
                self.game_info[c.SCORE] += 400
                self.moving_score_list.append(
                    score.Score(enemy.rect.centerx - self.viewport.x, enemy.rect.y, 400)
                )
                enemy.start_death_jump(shell.direction)
                self.sprites_about_to_die_group.add(enemy)
                enemy.kill()
            else:
                if enemy.direction == c.RIGHT:
                    shell.x_vel = 10
                    shell.direction = c.RIGHT
                elif enemy.direction == c.LEFT:
                    shell.x_vel = -10
                    shell.direction = c.LEFT

                shell.state = c.SHELL_SLIDE
                enemy.start_death_jump(shell.direction)
                self.sprites_about_to_die_group.add(enemy)
                enemy.kill()

    def check_enemy_y_collisions(self, enemy):
        """Checks enemy vertical collisions"""
        collider = pg.sprite.spritecollideany(enemy, self.ground_step_pipe_group)
        brick = pg.sprite.spritecollideany(enemy, self.brick_group)
        coin_box = pg.sprite.spritecollideany(enemy, self.coin_box_group)

        # Check if falling off platform
        if collider:
            if enemy.rect.bottom > collider.rect.bottom:
                enemy.y_vel = 0
                enemy.rect.bottom = collider.rect.top
                enemy.state = c.WALK
            elif enemy.rect.top < collider.rect.top:
                enemy.y_vel = 7
                enemy.rect.top = collider.rect.bottom
                enemy.state = c.FALL

        elif brick:
            if enemy.rect.bottom > brick.rect.bottom:
                enemy.y_vel = 0
                enemy.rect.bottom = brick.rect.top
                enemy.state = c.WALK
            elif enemy.rect.top < brick.rect.top:
                enemy.y_vel = 7
                enemy.rect.top = brick.rect.bottom
                enemy.state = c.FALL

        elif coin_box:
            if enemy.rect.bottom > coin_box.rect.bottom:
                enemy.y_vel = 0
                enemy.rect.bottom = coin_box.rect.top
                enemy.state = c.WALK
            elif enemy.rect.top < coin_box.rect.top:
                enemy.y_vel = 7
                enemy.rect.top = coin_box.rect.bottom
                enemy.state = c.FALL

        else:
            if not self.check_if_falling(enemy, self.ground_step_pipe_group):
                enemy.state = c.FALL

    def adjust_shell_position(self):
        """Adjusts shell positions"""
        for shell in self.shell_group:
            self.check_shell_x_collisions(shell)
            self.check_shell_y_collisions(shell)

    def check_shell_x_collisions(self, shell):
        """Checks shell horizontal collisions"""
        collider = pg.sprite.spritecollideany(shell, self.ground_step_pipe_group)
        brick = pg.sprite.spritecollideany(shell, self.brick_group)
        coin_box = pg.sprite.spritecollideany(shell, self.coin_box_group)
        enemy = pg.sprite.spritecollideany(shell, self.enemy_group)

        if collider:
            setup.SFX["bump"].play()
            if shell.direction == c.RIGHT:
                shell.direction = c.LEFT
                shell.rect.right = collider.rect.left
                shell.x_vel = -10
            elif shell.direction == c.LEFT:
                shell.direction = c.RIGHT
                shell.rect.left = collider.rect.right
                shell.x_vel = 10

        elif brick:
            setup.SFX["bump"].play()
            if shell.direction == c.RIGHT:
                shell.direction = c.LEFT
                shell.rect.right = brick.rect.left
                shell.x_vel = -10
            elif shell.direction == c.LEFT:
                shell.direction = c.RIGHT
                shell.rect.left = brick.rect.right
                shell.x_vel = 10

        elif coin_box:
            setup.SFX["bump"].play()
            if shell.direction == c.RIGHT:
                shell.direction = c.LEFT
                shell.rect.right = coin_box.rect.left
                shell.x_vel = -10
            elif shell.direction == c.LEFT:
                shell.direction = c.RIGHT
                shell.rect.left = coin_box.rect.right
                shell.x_vel = 10

        elif enemy:
            setup.SFX["kick"].play()
            self.game_info[c.SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.centerx - self.viewport.x, enemy.rect.y, 100)
            )
            enemy.start_death_jump(shell.direction)
            self.sprites_about_to_die_group.add(enemy)
            enemy.kill()

    def check_shell_y_collisions(self, shell):
        """Checks shell vertical collisions"""
        collider = pg.sprite.spritecollideany(shell, self.ground_step_pipe_group)
        if collider:
            shell.y_vel = 0
            shell.rect.bottom = collider.rect.top

    def adjust_powerup_position(self):
        """Moves mushrooms, stars and fireballs along the x, y axes"""
        for powerup in self.powerup_group:
            if powerup.name == c.MUSHROOM:
                self.adjust_mushroom_position(powerup)
            elif powerup.name == c.STAR:
                self.adjust_star_position(powerup)
            elif powerup.name == c.FIREBALL:
                self.adjust_fireball_position(powerup)
            elif powerup.name == '1up_mushroom':
                self.adjust_mushroom_position(powerup)

    def adjust_mushroom_position(self, mushroom):
        """Adjusts mushroom position"""
        if mushroom.state != c.REVEAL:
            self.check_mushroom_x_collisions(mushroom)
            self.check_mushroom_y_collisions(mushroom)

    def check_mushroom_x_collisions(self, mushroom):
        """Checks mushroom horizontal collisions"""
        collider = pg.sprite.spritecollideany(mushroom, self.ground_step_pipe_group)
        if collider:
            self.adjust_mushroom_for_collision_x(mushroom, collider)

        brick = pg.sprite.spritecollideany(mushroom, self.brick_group)
        if brick:
            self.adjust_mushroom_for_collision_x(mushroom, brick)

        coin_box = pg.sprite.spritecollideany(mushroom, self.coin_box_group)
        if coin_box:
            self.adjust_mushroom_for_collision_x(mushroom, coin_box)

    def check_mushroom_y_collisions(self, mushroom):
        """Checks mushroom vertical collisions"""
        collider = pg.sprite.spritecollideany(mushroom, self.ground_step_pipe_group)
        if collider:
            self.adjust_mushroom_for_collision_y(mushroom, collider)

        brick = pg.sprite.spritecollideany(mushroom, self.brick_group)
        if brick:
            self.adjust_mushroom_for_collision_y(mushroom, brick)

        coin_box = pg.sprite.spritecollideany(mushroom, self.coin_box_group)
        if coin_box:
            self.adjust_mushroom_for_collision_y(mushroom, coin_box)

        if not self.check_if_falling(mushroom, self.ground_step_pipe_group):
            mushroom.state = c.FALL

    def adjust_mushroom_for_collision_x(self, item, collider):
        """Adjusts mushroom for horizontal collision"""
        if item.rect.x < collider.rect.x:
            item.rect.right = collider.rect.left
            item.direction = c.LEFT
        else:
            item.rect.left = collider.rect.right
            item.direction = c.RIGHT

    def adjust_mushroom_for_collision_y(self, item, collider):
        """Adjusts mushroom for vertical collision"""
        item.rect.bottom = collider.rect.top
        item.state = c.SLIDE
        item.y_vel = 0

    def adjust_star_position(self, star):
        """Adjusts star position"""
        if star.state != c.REVEAL:
            self.check_star_y_collisions(star)

    def check_star_y_collisions(self, star):
        """Checks star vertical collisions"""
        collider = pg.sprite.spritecollideany(star, self.ground_step_pipe_group)
        if collider:
            self.adjust_star_for_collision_y(star, collider)

        brick = pg.sprite.spritecollideany(star, self.brick_group)
        if brick:
            self.adjust_star_for_collision_y(star, brick)

        coin_box = pg.sprite.spritecollideany(star, self.coin_box_group)
        if coin_box:
            self.adjust_star_for_collision_y(star, coin_box)

        if not self.check_if_falling(star, self.ground_step_pipe_group):
            star.state = c.FALL

    def adjust_star_for_collision_y(self, star, collider):
        """Adjusts star for vertical collision"""
        star.rect.bottom = collider.rect.top
        star.state = c.BOUNCE
        star.y_vel = star.y_accel

    def adjust_fireball_position(self, fireball):
        """Adjusts fireball position"""
        for fireball in self.mario.fireballs:
            self.check_fireball_x_collisions(fireball)
            self.check_fireball_y_collisions(fireball)

    def bounce_fireball(self, fireball):
        """Bounces fireball off ground"""
        fireball.y_vel = -8
        fireball.state = c.BOUNCING

    def check_fireball_x_collisions(self, fireball):
        """Checks fireball horizontal collisions"""
        collider = pg.sprite.spritecollideany(fireball, self.ground_step_pipe_group)
        if collider:
            fireball.kill()

        brick = pg.sprite.spritecollideany(fireball, self.brick_group)
        if brick:
            fireball.kill()

        coin_box = pg.sprite.spritecollideany(fireball, self.coin_box_group)
        if coin_box:
            fireball.kill()

        enemy = pg.sprite.spritecollideany(fireball, self.enemy_group)
        if enemy:
            self.fireball_kill(fireball, enemy)

        shell = pg.sprite.spritecollideany(fireball, self.shell_group)
        if shell:
            fireball.kill()

    def check_fireball_y_collisions(self, fireball):
        """Checks fireball vertical collisions"""
        collider = pg.sprite.spritecollideany(fireball, self.ground_step_pipe_group)
        if collider:
            if fireball.state == c.FLYING:
                self.bounce_fireball(fireball)
            elif fireball.state == c.BOUNCING:
                fireball.kill()

        brick = pg.sprite.spritecollideany(fireball, self.brick_group)
        if brick:
            if fireball.state == c.FLYING:
                self.bounce_fireball(fireball)
            elif fireball.state == c.BOUNCING:
                fireball.kill()

        coin_box = pg.sprite.spritecollideany(fireball, self.coin_box_group)
        if coin_box:
            if fireball.state == c.FLYING:
                self.bounce_fireball(fireball)
            elif fireball.state == c.BOUNCING:
                fireball.kill()

    def fireball_kill(self, fireball, enemy):
        """Kills enemy with fireball"""
        setup.SFX["kick"].play()
        self.game_info[c.SCORE] += 100
        self.moving_score_list.append(
            score.Score(enemy.rect.centerx - self.viewport.x, enemy.rect.y, 100)
        )
        enemy.start_death_jump(fireball.facing)
        self.sprites_about_to_die_group.add(enemy)
        enemy.kill()
        fireball.kill()

    def check_if_falling(self, sprite, sprite_group):
        """Checks if sprite is falling"""
        sprite.rect.y += 5

        if pg.sprite.spritecollideany(sprite, sprite_group):
            sprite.rect.y -= 5
            return True
        else:
            sprite.rect.y -= 5
            return False

    def delete_if_off_screen(self, enemy):
        """Deletes enemy if off screen"""
        if enemy.rect.x < (self.viewport.x - 300):
            enemy.kill()

    def check_flag(self):
        """Checks if Mario hits the flag"""
        if (
            self.mario.rect.centerx >= self.flag.rect.x
            and self.mario.state != c.FLAGPOLE
        ):
            self.mario.state = c.FLAGPOLE

    def check_to_add_flag_score(self):
        """Checks to add flag score"""
        if self.flag_score:
            self.flag_score.update(self.flag_score, self.game_info)
            if self.flag_score.y <= 120:
                self.flag_score.kill()
                self.flag_score = None

    def check_for_mario_death(self):
        """Checks if Mario has died"""
        if self.mario.rect.y > c.SCREEN_HEIGHT:
            self.mario.start_death_jump(self.game_info)
            self.state = c.FROZEN

    def play_death_song(self):
        """Plays death song"""
        if self.death_timer == 0:
            self.death_timer = self.current_time
        elif (self.current_time - self.death_timer) > 3000:
            self.set_game_info_values()
            self.done = True

    def set_game_info_values(self):
        """Sets game info values"""
        if self.mario.dead:
            self.persist[c.LIVES] -= 1

        if self.persist[c.LIVES] == 0:
            self.next_state = c.GAME_OVER
        elif self.mario.dead:
            if self.mario.rect.x > 3670:
                self.next_state = c.LEVEL2  # Volta para o level2 se morrer
            else:
                self.next_state = c.LEVEL2  # Volta para o level2 se morrer
        elif self.mario.in_castle:
            self.next_state = (
                c.MAIN_MENU
            )  # Volta ao menu principal após completar a fase 2

        self.persist[c.MARIO_DEAD] = self.mario.dead

    def check_if_time_out(self):
        """Checks if time runs out"""
        if self.overhead_info_display.time <= 0:
            self.overhead_info_display.time = 0
            self.mario.start_death_jump(self.game_info)
            self.state = c.FROZEN

    def update_viewport(self):
        """Updates viewport position"""
        third = self.viewport.x + self.viewport.width // 3
        mario_center = self.mario.rect.centerx

        if self.mario.x_vel > 0 and mario_center >= third:
            self.viewport.x += self.mario.x_vel
        elif self.mario.x_vel < 0 and self.mario.rect.x < self.viewport.centerx:
            self.viewport.x += self.mario.x_vel

    def update_while_in_castle(self):
        """Updates while Mario is in castle"""
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.game_info)
        self.overhead_info_display.update(self.game_info, self.mario)

        if self.mario.in_castle == False:
            self.state = c.FLAG_AND_FIREWORKS

    def update_flag_and_fireworks(self):
        """Updates during flag and fireworks"""
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.game_info)
        self.overhead_info_display.update(self.game_info, self.mario)
        self.check_to_add_flag_score()

        if self.flag_timer == 0:
            self.flag_timer = self.current_time
        elif (self.current_time - self.flag_timer) > 2000:
            self.set_game_info_values()
            self.done = True

    def blit_everything(self, surface):
        """Blits all sprites to the main surface"""
        self.level.blit(self.background, self.viewport, self.viewport)
        self.powerup_group.draw(self.level)
        self.coin_group.draw(self.level)
        self.brick_group.draw(self.level)
        self.coin_box_group.draw(self.level)
        self.sprites_about_to_die_group.draw(self.level)
        self.shell_group.draw(self.level)
        self.enemy_group.draw(self.level)
        self.mario_and_enemy_group.draw(self.level)
        self.flag_pole_group.draw(self.level)
        self.brick_pieces_group.draw(self.level)

        surface.blit(self.level, (0, 0), self.viewport)
        self.overhead_info_display.draw(surface)

        for score in self.moving_score_list:
            score.draw(surface)
        if self.flag_score:
            self.flag_score.draw(surface)
