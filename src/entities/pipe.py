import random
from typing import List

from ..utils import GameConfig
from .entity import Entity


class Pipe(Entity):
    def __init__(self, *args, difficulty: str = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.vel_x = -5
        self.difficulty = difficulty  # Nom de la difficulté (Projet Piscine, Web, etc.)

    def draw(self) -> None:
        self.x += self.vel_x
        super().draw()


class Pipes(Entity):
    upper: List[Pipe]
    lower: List[Pipe]
    
    # Les difficultés de la formation DAMS
    DIFFICULTIES = [
        "Projet Piscine",
        "Projet Web",
        "Projet Data",
        "Algorithmique",
        "Langage C",
        "Swift",
        "Java",
        "Kotlin",
        "R",
        "Machine Learning",
        "Deep Learning",
        "Statistical Learning",
        "Finance",
        "Comptabilité",
    ]

    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        self.pipe_gap = 120
        self.top = 0
        self.bottom = self.config.window.viewport_height
        self.upper = []
        self.lower = []
        self.difficulty_index = 0  # Pour cycler à travers les difficultés
        self.spawn_initial_pipes()

    def tick(self) -> None:
        if self.can_spawn_pipes():
            self.spawn_new_pipes()
        self.remove_old_pipes()

        for up_pipe, low_pipe in zip(self.upper, self.lower):
            up_pipe.tick()
            low_pipe.tick()

    def stop(self) -> None:
        for pipe in self.upper + self.lower:
            pipe.vel_x = 0

    def start(self) -> None:
        for pipe in self.upper + self.lower:
            pipe.vel_x = -5

    def can_spawn_pipes(self) -> bool:
        if not self.upper:
            return True
        
        last = self.upper[-1]
        if not last:
            return True

        return self.config.window.width - (last.x + last.w) > last.w * 2.5

    def spawn_new_pipes(self):
        # add new pipe when first pipe is about to touch left of screen
        upper, lower = self.make_random_pipes()
        self.upper.append(upper)
        self.lower.append(lower)

    def remove_old_pipes(self):
        # remove first pipe if its out of the screen
        for pipe in self.upper:
            if pipe.x < -pipe.w:
                self.upper.remove(pipe)

        for pipe in self.lower:
            if pipe.x < -pipe.w:
                self.lower.remove(pipe)

    def spawn_initial_pipes(self):
        upper_1, lower_1 = self.make_random_pipes()
        upper_1.x = self.config.window.width + upper_1.w * 3
        lower_1.x = self.config.window.width + upper_1.w * 3
        self.upper.append(upper_1)
        self.lower.append(lower_1)

        upper_2, lower_2 = self.make_random_pipes()
        upper_2.x = upper_1.x + upper_1.w * 3.5
        lower_2.x = upper_1.x + upper_1.w * 3.5
        self.upper.append(upper_2)
        self.lower.append(lower_2)

    def make_random_pipes(self):
        """returns a randomly generated pipe with a difficulty and custom image"""
        # Choisir une difficulté (cycler à travers ou aléatoire)
        difficulty = self.DIFFICULTIES[self.difficulty_index % len(self.DIFFICULTIES)]
        self.difficulty_index += 1
        
        # Récupérer les images personnalisées pour cette difficulté
        upper_img, lower_img = self.config.images.get_difficulty_pipe_images(difficulty)
        
        # y of gap between upper and lower pipe
        base_y = self.config.window.viewport_height

        gap_y = random.randrange(0, int(base_y * 0.6 - self.pipe_gap))
        gap_y += int(base_y * 0.2)
        pipe_x = self.config.window.width + 10

        upper_pipe = Pipe(
            self.config,
            upper_img,
            pipe_x,
            gap_y - upper_img.get_height(),
            difficulty=difficulty
        )

        lower_pipe = Pipe(
            self.config,
            lower_img,
            pipe_x,
            gap_y + self.pipe_gap,
            difficulty=difficulty
        )

        return upper_pipe, lower_pipe
