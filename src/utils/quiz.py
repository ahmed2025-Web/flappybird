import random


class QuizQuestion:
    def __init__(self, question: str, correct_answer: str, wrong_answer1: str, wrong_answer2: str):
        self.question = question
        self.correct_answer = correct_answer
        self.wrong_answers = [wrong_answer1, wrong_answer2]
        # Mélanger les réponses
        self.all_answers = [correct_answer, wrong_answer1, wrong_answer2]
        random.shuffle(self.all_answers)
    
    def is_correct(self, answer: str) -> bool:
        return answer == self.correct_answer
    
    def get_answers(self):
        """Retourne les 3 réponses mélangées"""
        return self.all_answers


class Quiz:
    """Quiz facile pour journée portes ouvertes"""
    
    QUESTIONS = [
        QuizQuestion(
            "Combien de bits dans un octet?",
            "8 bits",
            "16 bits",
            "4 bits"
        ),
        QuizQuestion(
            "Quel langage utilise les balises < et >?",
            "HTML",
            "Python",
            "Java"
        ),
        QuizQuestion(
            "Qu'est-ce que GitHub?",
            "Un site pour partager du code",
            "Un jeu vidéo",
            "Une marque d'ordinateur"
        ),
        QuizQuestion(
            "Python est un...",
            "Langage de programmation",
            "Un animal venimeux",
            "Un type de café"
        ),
        QuizQuestion(
            "Quelle est la capitale du web?",
            "L'algorithme",
            "Le routeur",
            "La batterie"
        ),
        QuizQuestion(
            "Qu'est-ce qu'un bug en programmation?",
            "Une erreur dans le code",
            "Un virus informatique",
            "Un type de souris"
        ),
        QuizQuestion(
            "Combien de dimensions a un pixel?",
            "2 (largeur x hauteur)",
            "3 (3D)",
            "1 (ligne)"
        ),
        QuizQuestion(
            "Quel langage est utilisé pour les sites web?",
            "JavaScript",
            "Assembly",
            "Rust"
        ),
        QuizQuestion(
            "Qu'est-ce que le Wi-Fi?",
            "Un réseau sans fil",
            "Un type de mur",
            "Une marque de biscuit"
        ),
        QuizQuestion(
            "Combien de bits dans un kilobit?",
            "1000 bits",
            "1024 bits",
            "512 bits"
        ),
    ]
    
    @staticmethod
    def get_random_question() -> QuizQuestion:
        """Retourne une question aléatoire"""
        return random.choice(Quiz.QUESTIONS)
