import os

class BestScoreManager:
    FILE = os.path.expanduser("~/.flappybird_best_score")

    @classmethod
    def get_best_score(cls):
        try:
            with open(cls.FILE, "r") as f:
                return int(f.read().strip())
        except Exception:
            return 0

    @classmethod
    def update_best_score(cls, score):
        best = cls.get_best_score()
        if score > best:
            with open(cls.FILE, "w") as f:
                f.write(str(score))
            return True  # Nouveau record battu
        return False
