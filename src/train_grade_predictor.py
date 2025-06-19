from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
import joblib
from src.export_training_data import fetch_translation_pairs

# Load data
data = fetch_translation_pairs()
X_text = [f"{eng} [SEP] {user}" for eng, user, _ in data]
y = [score for _, _, score in data]

# Load multilingual model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Encode pairs
X_emb = model.encode(X_text, convert_to_numpy=True, show_progress_bar=True)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_emb, y, test_size=0.2, random_state=42)

# Train a regressor
reg = Ridge()
reg.fit(X_train, y_train)

# Evaluate
score = reg.score(X_test, y_test)
print(f"Test R^2: {score:.3f}")

# Save model
joblib.dump((reg, model), "data/grade_predictor.joblib")
print("Model saved to data/grade_predictor.joblib")