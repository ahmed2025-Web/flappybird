import pygame
from .quiz import Quiz
import random


class QuizUI:
    """Interface visuelle pour le quiz - respecte la taille de la fenêtre"""
    
    # Couleurs
    COLOR_BG = (20, 20, 40)
    COLOR_QUESTION = (255, 255, 255)
    COLOR_BUTTON = (100, 150, 255)
    COLOR_BUTTON_HOVER = (150, 200, 255)
    COLOR_BUTTON_CORRECT = (100, 255, 100)
    COLOR_BUTTON_WRONG = (255, 100, 100)
    COLOR_TEXT = (255, 255, 255)
    
    def __init__(self, config):
        self.config = config
        self.question = None
        self.button_rects = []
        self.selected_answer = None
        self.show_result = False
        self.is_correct = False
        self.result_message = None
        self.new_question()
    
    def new_question(self):
        """Charger une nouvelle question"""
        self.question = Quiz.get_random_question()
        self.button_rects = []
        self.selected_answer = None
        self.show_result = False
        self.result_message = None
    
    def draw(self, screen):
        """Dessiner l'écran du quiz"""
        # Fond semi-transparent
        overlay = pygame.Surface((self.config.window.width, self.config.window.height))
        overlay.set_alpha(200)
        overlay.fill(self.COLOR_BG)
        screen.blit(overlay, (0, 0))
        
        # Titre
        font_title = pygame.font.SysFont("Arial", 18, bold=True)
        title = font_title.render("QUIZ - Répondez pour continuer!", True, (100, 255, 100))
        title_rect = title.get_rect(center=(self.config.window.width // 2, 30))
        screen.blit(title, title_rect)
        
        # Question
        font_question = pygame.font.SysFont("Arial", 14, bold=True)
        question_text = font_question.render(self.question.question, True, self.COLOR_QUESTION)
        question_rect = question_text.get_rect(center=(self.config.window.width // 2, 80))
        screen.blit(question_text, question_rect)
        
        # Boutons des réponses
        margin = 20
        button_width = self.config.window.width - (2 * margin)
        button_height = 50
        start_y = 150
        spacing = 70
        
        font_button = pygame.font.SysFont("Arial", 12, bold=True)
        
        self.button_rects = []
        for i, answer in enumerate(self.question.get_answers()):
            button_y = start_y + (i * spacing)
            button_rect = pygame.Rect(margin, button_y, button_width, button_height)
            self.button_rects.append((button_rect, answer))
            
            # Couleur du bouton selon l'état
            if self.show_result:
                if answer == self.question.correct_answer:
                    button_color = self.COLOR_BUTTON_CORRECT
                elif answer == self.selected_answer and not self.is_correct:
                    button_color = self.COLOR_BUTTON_WRONG
                else:
                    button_color = self.COLOR_BUTTON
            else:
                # Hover effect
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    button_color = self.COLOR_BUTTON_HOVER
                else:
                    button_color = self.COLOR_BUTTON
            
            # Dessiner le bouton
            pygame.draw.rect(screen, button_color, button_rect, border_radius=5)
            pygame.draw.rect(screen, self.COLOR_TEXT, button_rect, 2, border_radius=5)
            
            # Texte du bouton
            answer_text = font_button.render(f"{i+1}. {answer}", True, self.COLOR_TEXT)
            answer_rect = answer_text.get_rect(center=button_rect.center)
            screen.blit(answer_text, answer_rect)
        
        # Message résultat
        if self.show_result and self.result_message:
            font_result = pygame.font.SysFont("Arial", 20, bold=True)
            font_message = pygame.font.SysFont("Arial", 15)
            
            if self.is_correct:
               
                result_bg = pygame.Surface((self.config.window.width, 120))
                result_bg.fill((50, 200, 50))
                result_bg.set_alpha(240)
                screen.blit(result_bg, (0, 380))
                
                result_text = font_result.render(" BONNE RÉPONSE!", True, (255, 255, 255))
                result_rect = result_text.get_rect(center=(self.config.window.width // 2, 410))
                screen.blit(result_text, result_rect)
                
                message_text = font_message.render(self.result_message, True, (255, 255, 255))
                message_rect = message_text.get_rect(center=(self.config.window.width // 2, 455))
                screen.blit(message_text, message_rect)
            else:
               
                result_bg = pygame.Surface((self.config.window.width, 120))
                result_bg.fill((200, 50, 50))
                result_bg.set_alpha(240)
                screen.blit(result_bg, (0, 380))
                
                result_text = font_result.render(" DOMMAGE!", True, (255, 255, 255))
                result_rect = result_text.get_rect(center=(self.config.window.width // 2, 410))
                screen.blit(result_text, result_rect)
                
                message_text = font_message.render(self.result_message, True, (255, 255, 255))
                message_rect = message_text.get_rect(center=(self.config.window.width // 2, 455))
                screen.blit(message_text, message_rect)
    
    def handle_click(self, pos):
        """Gérer un clic sur une réponse"""
        if self.show_result:
            return
        
        for button_rect, answer in self.button_rects:
            if button_rect.collidepoint(pos):
                self.selected_answer = answer
                self.is_correct = self.question.is_correct(answer)
                self.show_result = True
                
                # Générer le message une seule fois
                if self.is_correct:
                    self.result_message = "Prêt à continuer? Cliquez..."
                else:
                    messages = [
                        "Pas grave! Continuons!",
                        "On apprend de ses erreurs!",
                        "Bonne chance!",
                        "Vous pouvez mieux faire!"
                    ]
                    self.result_message = random.choice(messages)
                
                return self.is_correct
        
        return None
    
    def is_done(self):
        """Vérifier si le quiz est terminé (réponse sélectionnée)"""
        return self.show_result
