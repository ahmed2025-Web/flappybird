import asyncio
import sys

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from .entities import (
    Background,
    Floor,
    GameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from .utils import GameConfig, Images, Quiz, QuizUI, Sounds, Window


class Flappy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        window = Window(288, 512)
        # Créer écran fullscreen
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # Récupérer les dimensions réelles
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        # Créer une surface pour le jeu (288x512)
        self.game_surface = pygame.Surface((window.width, window.height))
        images = Images()

        self.config = GameConfig(
            screen=self.game_surface,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=images,
            sounds=Sounds(),
        )
        self.display_screen = screen
        # Calculer l'offset du jeu centré
        self.game_x = (self.screen_width - window.width) // 2
        self.game_y = (self.screen_height - window.height) // 2
        
        # Charger l'image de fond et la redimensionner pour le fullscreen
        try:
            self.background_image = pygame.image.load("assets/sprites/image sur algorithme et projets.jpg")
            self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        except:
            self.background_image = None

    def is_click_in_game(self, pos):
        """Vérifie si un clic est dans la zone du jeu"""
        return (self.game_x <= pos[0] < self.game_x + 288 and
                self.game_y <= pos[1] < self.game_y + 512)
    
    def convert_click_coords(self, pos):
        """Convertit les coordonnées du fullscreen au jeu"""
        return (pos[0] - self.game_x, pos[1] - self.game_y)

    async def start(self):
        while True:
            self.background = Background(self.config)
            self.floor = Floor(self.config)
            self.player = Player(self.config)
            self.welcome_message = WelcomeMessage(self.config)
            self.game_over_message = GameOver(self.config)
            self.pipes = Pipes(self.config)
            self.score = Score(self.config)
            await self.splash()
            await self.play()
            await self.game_over()

    async def splash(self):
        """Shows welcome splash screen animation of flappy bird"""

        self.player.set_mode(PlayerMode.SHM)

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    return

            self.background.tick()
            self.floor.tick()
            self.player.tick()
            self.welcome_message.tick()

            self.display_centered_game()
            await asyncio.sleep(0)
            self.config.tick()

    def display_centered_game(self):
        if self.background_image:
            self.display_screen.blit(self.background_image, (0, 0))
        else:
            self.display_screen.fill((255, 255, 255))
        x = (self.screen_width - self.game_surface.get_width()) // 2
        y = (self.screen_height - self.game_surface.get_height()) // 2
        self.display_screen.blit(self.game_surface, (x, y))
        pygame.display.update()

    def check_quit_event(self, event):
        if event.type == QUIT or (
            event.type == KEYDOWN and event.key == K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

    def is_tap_event(self, event):
        m_left, _, _ = pygame.mouse.get_pressed()
        if m_left and pygame.mouse.get_focused():
            if not self.is_click_in_game(pygame.mouse.get_pos()):
                m_left = False
        
        space_or_up = event.type == KEYDOWN and (
            event.key == K_SPACE or event.key == K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_or_up or screen_tap

    async def play(self):
        self.score.reset()
        self.player.set_mode(PlayerMode.NORMAL)

        while True:
            if self.player.collided(self.pipes, self.floor):
                # Récupérer la difficulté de collision et l'obstacle
                difficulty = None
                collided_pipe = None
                for pipe in self.pipes.upper + self.pipes.lower:
                    if self.player.collide(pipe):
                        difficulty = pipe.difficulty
                        collided_pipe = pipe
                        break
                
                quiz_result = await self.quiz(difficulty)
                if not quiz_result:
                    # Mauvaise réponse: quitter play()
                    return
                
                # Bonne réponse: supprimer la PAIRE de pipes (haut + bas au même x)
                if collided_pipe:
                    x = collided_pipe.x
                    eps = 2  # Tolérance pour comparaison float
                    self.pipes.upper = [p for p in self.pipes.upper if abs(p.x - x) > eps]
                    self.pipes.lower = [p for p in self.pipes.lower if abs(p.x - x) > eps]
                
                # Relancer le scrolling
                self.pipes.start()
                self.floor.start()
                continue

            for i, pipe in enumerate(self.pipes.upper):
                if self.player.crossed(pipe):
                    self.score.add()

            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    self.player.flap()

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()

            self.display_centered_game()
            await asyncio.sleep(0)
            self.config.tick()

    async def quiz(self, difficulty: str = None):
        """Affiche une quiz quand le joueur entre en collision"""
        self.pipes.stop()
        self.floor.stop()
        
        # Créer l'interface quiz
        quiz_ui = QuizUI(self.config, difficulty)
        waiting_for_confirmation = False
        
        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_click_in_game(event.pos):
                        game_pos = self.convert_click_coords(event.pos)
                        
                        if not waiting_for_confirmation:
                            quiz_ui.handle_click(game_pos)
                            if quiz_ui.is_done():
                                waiting_for_confirmation = True
                        else:
                            if quiz_ui.is_correct:
                                # Bonne réponse: relancer les mouvements
                                self.pipes.start()
                                self.floor.start()
                                self.player.set_mode(PlayerMode.NORMAL)
                                return True
                            else:
                                # Mauvaise réponse: aller au game over
                                self.player.set_mode(PlayerMode.CRASH)
                                self.config.sounds.hit.play()
                                return False
            
            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()
            # NE PAS afficher game_over_message pendant la quiz
            quiz_ui.draw(self.config.screen)
            
            self.config.tick()
            self.display_centered_game()
            await asyncio.sleep(0)

    async def game_over(self):
        """crashes the player down and shows gameover image"""

        self.player.set_mode(PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    if self.player.y + self.player.h >= self.floor.y - 1:
                        return

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()
            self.game_over_message.tick()

            self.display_centered_game()
            await asyncio.sleep(0)
