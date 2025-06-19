from src.db import Database

class AdaptiveController:
    def __init__(self, db_file="data/french_tutor.db"):
        self.db = Database(db_file)
        self.levels = ["beginner", "intermediate", "advanced"]

    def suggest_next_difficulty(self, n=5):
        """Suggest next difficulty based on recent scores at the current level."""
        # Find the most recent difficulty attempted
        last_ex = self.db.get_last_n_exercises(1)
        # last_ex[0][-1] is now the difficulty string
        if last_ex and last_ex[0][-1] in self.levels:
            current_level = last_ex[0][-1]
        else:
            current_level = "beginner"

        idx = self.levels.index(current_level)
        recent = self.db.get_last_n_exercises_by_difficulty(n, current_level)
        if not recent or len(recent) < n:
            return current_level  # Not enough data, stay

        avg_score = sum([row[3] for row in recent]) / len(recent)

        # Move up if doing well, down if struggling, else stay
        if avg_score >= 0.85 and idx < len(self.levels) - 1:
            return self.levels[idx + 1]  # Move up one level
        elif avg_score < 0.65 and idx > 0:
            return self.levels[idx - 1]  # Move down one level
        else:
            return current_level  # Stay

    def close(self):
        self.db.close()