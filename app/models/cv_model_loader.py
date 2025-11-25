import pickle
from app.config import settings

class CVModelLoader:
    def __init__(self):
        with open(settings.CV_MODEL_PATH, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, features: list):
        pred = self.model.predict([features])[0]
        prob = self.model.predict_proba([features])[0][1]
        return pred, prob

cv_model = CVModelLoader()
