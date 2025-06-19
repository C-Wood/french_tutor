import sqlite3
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
import joblib

def fetch_translation_pairs(db_path="data/french_tutor.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT english_sentence, user_translation, score
        FROM translation_exercises
        WHERE english_sentence IS NOT NULL AND user_translation IS NOT NULL AND score IS NOT NULL
    """)
    data = cur.fetchall()
    conn.close()
    return data

def main():
    # 1. Load data
    data = fetch_translation_pairs()
    print(f"Loaded {len(data)} translation pairs.")
    if not data:
        print("No data found. Please add some translation exercises to your database.")
        return

    X_text = [f"{eng} [SEP] {user}" for eng, user, _ in data]
    y = [score for _, _, score in data]

    # 2. Load multilingual model
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    # 3. Encode pairs
    print("Encoding sentence pairs...")
    X_emb = model.encode(X_text, convert_to_numpy=True, show_progress_bar=True)

    # 4. Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X_emb, y, test_size=0.2, random_state=42)

    # 5. Train a regressor
    reg = Ridge()
    reg.fit(X_train, y_train)

    # 6. Evaluate
    score = reg.score(X_test, y_test)
    print(f"Test R^2: {score:.3f}")

    # 7. Save model
    joblib.dump((reg, model), "data/grade_predictor.joblib")
    print("Model saved to data/grade_predictor.joblib")

    # 8. Predict a grade for a sample translation
    english = "The cat is on the table."
    user_translation = "Le chat est sur la table."
    pair = f"{english} [SEP] {user_translation}"
    emb = model.encode([pair])
    pred = reg.predict(emb)[0]
    print(f"Predicted grade for sample: {pred:.2f}")

if __name__ == "__main__":
    main()