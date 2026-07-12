import joblib
from config import *
import pandas as pd

MODEL_PATH = "models/model.joblib"

def load_model():
    return joblib.load(MODEL_PATH)

def predict(features):
    model = load_model()
    return model.predict(features)


if __name__ == "__main__":
    sample = pd.DataFrame([{
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }])

    prediction = predict(sample)

    print("Prediction:", prediction)