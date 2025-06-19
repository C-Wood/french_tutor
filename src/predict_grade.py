import joblib

def predict_grade(english, user_translation):
    reg, model = joblib.load("data/grade_predictor.joblib")
    pair = f"{english} [SEP] {user_translation}"
    emb = model.encode([pair])
    pred = reg.predict(emb)[0]
    return float(pred)

if __name__ == "__main__":
    english = "The cat is on the table."
    user_translation = "Le chat est sur la table."
    pred = predict_grade(english, user_translation)
    print(f"Predicted grade: {pred:.2f}")