import pygame

from ..utils import GameConfig
from ..utils.best_score import BestScoreManager
from .entity import Entity


class Score(Entity):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        self.y = self.config.window.height * 0.1
        self.score = 0
        self.just_broke_record = False
        self._record_display_counter = 0
        self._record_was_broken_this_run = False

    def reset(self) -> None:
        self.score = 0
        self.just_broke_record = False
        self._record_display_counter = 0
        self._record_was_broken_this_run = False

    def add(self) -> None:
        best = BestScoreManager.get_best_score()
        self.score += 1
        self.config.sounds.point.play()
        
        if (
            self.score > best
            and not self.just_broke_record
            and not self._record_was_broken_this_run
        ):
            self.just_broke_record = True
            self._record_display_counter = 90  # ~3 secondes à 30 FPS
            self._record_was_broken_this_run = True

    @property
    def rect(self) -> pygame.Rect:
        score_digits = [int(x) for x in list(str(self.score))]
        images = [self.config.images.numbers[digit] for digit in score_digits]
        w = sum(image.get_width() for image in images)
        x = (self.config.window.width - w) / 2
        h = max(image.get_height() for image in images)
        return pygame.Rect(x, self.y, w, h)

    def draw(self) -> None:
        # N'affiche rien si on est dans un quiz (on laisse le quiz gérer l'affichage)
        if hasattr(self.config, 'in_quiz') and self.config.in_quiz:
            return
        # Score courant (au centre)
        score_digits = [int(x) for x in list(str(self.score))]
        images = [self.config.images.numbers[digit] for digit in score_digits]
        digits_width = sum(image.get_width() for image in images)
        x_offset = (self.config.window.width - digits_width) / 2
        for image in images:
            self.config.screen.blit(image, (x_offset, self.y))
            x_offset += image.get_width()

        # Best score (toujours visible, discret en haut à gauche)
        best = BestScoreManager.get_best_score()
        font_best = pygame.font.SysFont("Arial", 14, bold=True)
        best_text = font_best.render(f"Best: {best}", True, (255, 215, 0))
        self.config.screen.blit(best_text, (8, 8))

        # Message record battu temporaire
        if self.just_broke_record and self._record_display_counter > 0:
            font = pygame.font.SysFont("Arial", 18, bold=True)
            text = font.render("NOUVEAU RECORD !", True, (255, 215, 0))
            rect = text.get_rect(center=(self.config.window.width // 2, self.y + 40))
            self.config.screen.blit(text, rect)
            self._record_display_counter -= 1
        if self._record_display_counter == 0:
            self.just_broke_record = False

    def update_best_score(self):
        return BestScoreManager.update_best_score(self.score)
