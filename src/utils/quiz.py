import random


class QuizQuestion:
    def __init__(self, difficulty: str, question: str, correct_answer: str, wrong_answer1: str, wrong_answer2: str):
        self.difficulty = difficulty  # Le nom de la difficulté (Projet Piscine, Web, etc.)
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
    """Quiz pour journée portes ouvertes - Formation DAMS"""
    
    QUESTIONS = [
        QuizQuestion(
            "Projet Piscine",
            "Comment réussir le projet piscine ?",
            "Organisation + commencer tôt",
            "Attendre la dernière semaine",
            "Copier sans comprendre"
        ),
        QuizQuestion(
            "Projet Web",
            "Le plus important pour un projet web ?",
            "Structure + travail en équipe",
            "Le design seulement",
            "Tout faire seul"
        ),
        QuizQuestion(
            "Projet Data",
            "Avant de faire un modèle, il faut :",
            "Comprendre et nettoyer les données",
            "Lancer le code directement",
            "Choisir le modèle le plus complexe"
        ),
        QuizQuestion(
            "Algorithmique",
            "Une bonne solution algorithmique est :",
            "La plus claire et efficace",
            "La plus longue",
            "La plus compliquée"
        ),
        QuizQuestion(
            "Langage C",
            "Le plus grand danger en C ?",
            "La gestion de la mémoire",
            "Les boucles",
            "Les fonctions"
        ),
        QuizQuestion(
            "Swift",
            "Swift est surtout utilisé pour :",
            "Les apps iOS",
            "Le web",
            "Les bases de données"
        ),
        QuizQuestion(
            "Java",
            "L'avantage principal de Java ?",
            "Portable (JVM)",
            "Rapide à écrire",
            "Très simple"
        ),
        QuizQuestion(
            "Kotlin",
            "Kotlin est principalement lié à :",
            "Android",
            "iOS",
            "Web"
        ),
        QuizQuestion(
            "R",
            "R est surtout utilisé pour :",
            "Statistiques et data",
            "Jeux vidéo",
            "Systèmes embarqués"
        ),
        QuizQuestion(
            "Machine Learning",
            "Le machine learning permet :",
            "D'apprendre à partir des données",
            "De coder sans données",
            "De tout prédire parfaitement"
        ),
        QuizQuestion(
            "Deep Learning",
            "Le deep learning est basé sur :",
            "Des réseaux de neurones",
            "Des règles fixes",
            "Des tableaux Excel"
        ),
        QuizQuestion(
            "Statistical Learning",
            "Le statistical learning sert à :",
            "Modéliser et interpréter les données",
            "Décorer des graphiques",
            "Remplacer les maths"
        ),
        QuizQuestion(
            "Finance",
            "En finance, le plus important est :",
            "Analyser le risque",
            "Deviner",
            "Copier les autres"
        ),
        QuizQuestion(
            "Comptabilité",
            "La comptabilité sert à :",
            "Suivre la santé financière",
            "Programmer",
            "Faire du marketing"
        ),
    ]
    
    @staticmethod
    def get_random_question() -> QuizQuestion:
        """Retourne une question aléatoire"""
        return random.choice(Quiz.QUESTIONS)
    
    @staticmethod
    def get_question_by_difficulty(difficulty: str) -> QuizQuestion:
        """Retourne la question correspondant à une difficulté"""
        questions = [q for q in Quiz.QUESTIONS if q.difficulty == difficulty]
        if questions:
            return questions[0]
        return Quiz.get_random_question()
