import random
from typing import List, Tuple, Dict

import pygame

from .constants import BACKGROUNDS, PIPES, PLAYERS


class DifficultyImageGenerator:
    """Génère des images pour chaque difficulté"""
    
    # Couleurs par thème de difficulté
    DIFFICULTY_COLORS = {
        "Projet Piscine": (100, 149, 237),      # Cornflower Blue
        "Projet Web": (255, 140, 0),             # Dark Orange
        "Projet Data": (34, 139, 34),            # Forest Green
        "Algorithmique": (220, 20, 60),          # Crimson
        "Langage C": (0, 0, 139),                # Dark Blue
        "Swift": (255, 69, 0),                   # Red Orange
        "Java": (184, 134, 11),                  # Dark Goldenrod
        "Kotlin": (139, 35, 69),                 # Dark Slate Blue
        "R": (25, 25, 112),                      # Midnight Blue
        "Machine Learning": (255, 20, 147),     # Deep Pink
        "Deep Learning": (138, 43, 226),        # Blue Violet
        "Statistical Learning": (0, 100, 100),  # Dark Cyan
        "Finance": (184, 134, 11),              # Dark Goldenrod
        "Comptabilité": (105, 105, 105),        # Dim Gray
    }
    
    @staticmethod
    def create_difficulty_image(difficulty: str, height: int = 320, width: int = 52) -> pygame.Surface:
        """Crée une image pour une difficulté"""
        # Créer la surface
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Couleur de base
        color = DifficultyImageGenerator.DIFFICULTY_COLORS.get(difficulty, (100, 100, 100))
        
        # Remplir avec dégradé de couleur
        for y in range(height):
            # Créer un dégradé vertical
            factor = y / height
            r = int(color[0] * (0.7 + 0.3 * factor))
            g = int(color[1] * (0.7 + 0.3 * factor))
            b = int(color[2] * (0.7 + 0.3 * factor))
            pygame.draw.line(image, (r, g, b, 255), (0, y), (width, y))
        
        # Ajouter une bordure
        pygame.draw.rect(image, (255, 255, 255, 200), (0, 0, width, height), 3, border_radius=5)
        
        # Ajouter le texte du nom de la difficulté
        font = pygame.font.SysFont("Arial", 10, bold=True)
        # Diviser le texte en deux lignes si trop long
        text_parts = difficulty.split()
        if len(text_parts) > 1:
            text_line1 = " ".join(text_parts[:len(text_parts)//2])
            text_line2 = " ".join(text_parts[len(text_parts)//2:])
        else:
            text_line1 = difficulty
            text_line2 = ""
        
        # Afficher le texte centré
        if text_line2:
            text_surface1 = font.render(text_line1, True, (255, 255, 255))
            text_surface2 = font.render(text_line2, True, (255, 255, 255))
            text_rect1 = text_surface1.get_rect(center=(width // 2, height // 2 - 10))
            text_rect2 = text_surface2.get_rect(center=(width // 2, height // 2 + 10))
            image.blit(text_surface1, text_rect1)
            image.blit(text_surface2, text_rect2)
        else:
            text_surface = font.render(text_line1, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            image.blit(text_surface, text_rect)
        
        return image


class Images:
    numbers: List[pygame.Surface]
    game_over: pygame.Surface
    welcome_message: pygame.Surface
    base: pygame.Surface
    background: pygame.Surface
    player: Tuple[pygame.Surface]
    pipe: Tuple[pygame.Surface]
    difficulty_pipes: Dict[str, Tuple[pygame.Surface, pygame.Surface]]

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
        
        # Initialiser le dictionnaire des tuyaux personnalisés
        self.difficulty_pipes = {}
        self.randomize()

    def randomize(self):
        # Charger le background JPO personnalisé
        try:
            bg = pygame.image.load("assets/sprites/jpo-background.png").convert()
            # Redimensionner pour adapter à la résolution du jeu (288x512)
            self.background = pygame.transform.scale(bg, (288, 512))
        except:
            # Fallback: utiliser un background aléatoire si l'image JPO n'existe pas
            rand_bg = random.randint(0, len(BACKGROUNDS) - 1)
            self.background = pygame.image.load(BACKGROUNDS[rand_bg]).convert()
        
        # select random player sprites
        #rand_player = random.randint(0, len(PLAYERS) - 1)
        rand_player = 3
        # select random pipe sprites
        rand_pipe = random.randint(0, len(PIPES) - 1)
        
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
    
    def get_difficulty_pipe_images(self, difficulty: str) -> Tuple[pygame.Surface, pygame.Surface]:
        """Retourne les images des tuyaux pour une difficulté donnée"""
        if difficulty not in self.difficulty_pipes:
            # Générer les images pour cette difficulté
            upper_image = DifficultyImageGenerator.create_difficulty_image(difficulty, height=320)
            lower_image = DifficultyImageGenerator.create_difficulty_image(difficulty, height=320)
            self.difficulty_pipes[difficulty] = (upper_image, lower_image)
        
        return self.difficulty_pipes[difficulty]
