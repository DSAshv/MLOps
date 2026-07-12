import pandas as pd
from predict import predict
from config import *

def test_prediction():

    sample = pd.DataFrame([{
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }])

    result = predict(sample)

    assert len(result) == 1

    assert result[0] in [
        "setosa",
        "versicolor",
        "virginica"
    ]