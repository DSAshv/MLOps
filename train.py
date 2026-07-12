import os
import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from config import *

os.makedirs("models", exist_ok=True)

data = pd.read_csv("data/raw/iris.csv")

X = data[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
y = data["species"]

model = DecisionTreeClassifier(max_depth=3)
model.fit(X, y)

joblib.dump(model, "models/model.joblib")

print("Model saved successfully.")