import random
from typing import List, Tuple

import pygame

from .constants import BACKGROUNDS, PIPES, PLAYERS


class Images:
    numbers: List[pygame.Surface]
    game_over: pygame.Surface
    welcome_message: pygame.Surface
    base: pygame.Surface
    background: pygame.Surface
    player: Tuple[pygame.Surface]
    pipe: Tuple[pygame.Surface]

    def __init__(self) -> None:
        self.numbers = list(
            (
                pygame.image.load(f"assets/sprites/{num}.png").convert_alpha()
                for num in range(10)
            )
        )

        # game over sprite
        self.game_over = pygame.image.load(
            "assets/sprites/gameover.png"
        ).convert_alpha()
        # welcome_message sprite for welcome screen
        self.welcome_message = pygame.image.load(
            "assets/sprites/message.png"
        ).convert_alpha()
        # base (ground) sprite
        self.base = pygame.image.load("assets/sprites/base.png").convert_alpha()
        self.randomize()

    def randomize(self):
        # select random background sprites
        rand_bg = random.randint(0, len(BACKGROUNDS) - 1)
        # select random player sprites
        #rand_player = random.randint(0, len(PLAYERS) - 1)
        rand_player = 3
        # select random pipe sprites
        rand_pipe = random.randint(0, len(PIPES) - 1)

        self.background = pygame.image.load(BACKGROUNDS[rand_bg]).convert()
        
        # Charger et redimensionner les images du custom bird
        p0 = pygame.image.load(PLAYERS[rand_player][0]).convert_alpha()
        p1 = pygame.image.load(PLAYERS[rand_player][1]).convert_alpha()
        p2 = pygame.image.load(PLAYERS[rand_player][2]).convert_alpha()
        
        # Redimensionner si c'est le custom bird (408x612 -> 100x150 pour voir le "01")
        if p0.get_width() > 100:
            p0 = pygame.transform.scale(p0, (100, 150))
            p1 = pygame.transform.scale(p1, (100, 150))
            p2 = pygame.transform.scale(p2, (100, 150))
        
        self.player = (p0, p1, p2)
        
        self.pipe = (
            pygame.transform.flip(
                pygame.image.load(PIPES[rand_pipe]).convert_alpha(),
                False,
                True,
            ),
            pygame.image.load(PIPES[rand_pipe]).convert_alpha(),
        )
