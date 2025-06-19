import joblib

def load_grade_predictor(model_path="data/grade_predictor.joblib"):
    reg, model = joblib.load(model_path)
    return reg, model

def predict_grade(english, user_translation, reg, model):
    pair = f"{english} [SEP] {user_translation}"
    emb = model.encode([pair])
    pred = reg.predict(emb)[0]
    return float(pred)