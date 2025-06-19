import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_file="data/french_tutor.db"):
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to the SQLite database."""
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create necessary tables if they don't exist."""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS practice_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Add difficulty column if it doesn't exist
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS translation_exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            english_sentence TEXT,
            correct_french TEXT,
            user_translation TEXT,
            score FLOAT,
            feedback TEXT,
            difficulty TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES practice_sessions(id)
        )
        ''')

        self.conn.commit()
    
    def start_session(self):
        """Start a new practice session and return its ID."""
        self.cursor.execute("INSERT INTO practice_sessions DEFAULT VALUES")
        self.conn.commit()
        return self.cursor.lastrowid
    
    def save_translation_exercise(self, session_id, english, correct_french, user_translation, score, feedback, difficulty):
        """Save the results of a translation exercise."""
        self.cursor.execute('''
        INSERT INTO translation_exercises 
        (session_id, english_sentence, correct_french, user_translation, score, feedback, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, english, correct_french, user_translation, score, feedback, difficulty))
        self.conn.commit()
    
    
    def get_recent_exercises(self, limit=10):
        """Get the recent translation exercises."""
        self.cursor.execute('''
        SELECT english_sentence, correct_french, user_translation, score, feedback
        FROM translation_exercises
        ORDER BY timestamp DESC
        LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()

    def get_recent_perfect_english(self, limit=10, min_score=1.0):
        """Return a set of English sentences recently answered with a perfect score."""
        self.cursor.execute('''
        SELECT english_sentence FROM translation_exercises
        WHERE score >= ? 
        ORDER BY timestamp DESC
        LIMIT ?
        ''', (min_score, limit))
        return set(row[0] for row in self.cursor.fetchall())
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def get_last_n_exercises(self, n=5):
        """Get the last n translation exercises with their scores and difficulty."""
        self.cursor.execute('''
        SELECT english_sentence, correct_french, user_translation, score, feedback, difficulty
        FROM translation_exercises
        ORDER BY timestamp DESC
        LIMIT ?
        ''', (n,))
        return self.cursor.fetchall()
    
    def get_last_n_exercises_by_difficulty(self, n=5, difficulty="beginner"):
        """Get the last n translation exercises for a given difficulty."""
        self.cursor.execute('''
        SELECT english_sentence, correct_french, user_translation, score, feedback, difficulty
        FROM translation_exercises
        WHERE difficulty = ?
        ORDER BY timestamp DESC
        LIMIT ?
        ''', (difficulty, n))
        return self.cursor.fetchall()