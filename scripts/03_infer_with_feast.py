"""
TASK 5: Fetch Features from Online Store & Perform Inference
===========================================================

This script:
1. Loads the trained model
2. Fetches features from Feast ONLINE STORE (real-time, low-latency)
3. Makes predictions for specific iris plants
4. Demonstrates consistency with training

Key Point: Online store = fast lookups for single entities
This is how inference works in production!
"""

import sys
import pandas as pd
from pathlib import Path
import joblib

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from feast import FeatureStore


def infer_with_feast():
    """Perform inference using features from Feast online store"""
    
    print("=" * 70)
    print("TASK 5: INFERENCE WITH FEAST ONLINE STORE")
    print("=" * 70)
    
    try:
        # 1. LOAD FEATURE STORE AND MODEL
        fs = FeatureStore(repo_path="feature_repo")
        print("✓ Feast Feature Store loaded")
        
        model_path = Path("models") / "iris_model_feast.joblib"
        if not model_path.exists():
            print(f"✗ Model not found at {model_path}")
            print("  Please run 02_train_with_feast.py first")
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        model = joblib.load(str(model_path))
        print(f"✓ Model loaded from {model_path}")
        
        # 2. SELECT IRIS PLANTS FOR INFERENCE
        iris_ids_to_predict = [1001, 1002, 1003]
        print(f"\n▶ Predicting for iris IDs: {iris_ids_to_predict}")
        
        # 3. CREATE ENTITY DATAFRAME FOR ONLINE STORE LOOKUP
        entity_df = pd.DataFrame({
            "iris_id": iris_ids_to_predict,
        })
        print(f"✓ Created entity DataFrame for online lookup")
        
        # 4. FETCH FEATURES FROM ONLINE STORE (REAL-TIME)
        print(f"\n▶ Fetching features from Feast ONLINE STORE...")
        print(f"  (This is fast, low-latency lookup for production)")
        
        online_features = fs.get_online_features(
            entity_rows=entity_df.to_dict(orient="records"),
            features=[
                "iris_measurements:sepal_length",
                "iris_measurements:sepal_width",
                "iris_measurements:petal_length",
                "iris_measurements:petal_width",
            ],
        ).to_df()
        
        print(f"✓ Features fetched from online store!")
        print(f"\n  Features:\n{online_features}")
        
        # 5. PREPARE DATA FOR INFERENCE
        feature_columns = [
            "sepal_length", "sepal_width", "petal_length", "petal_width"
        ]
        X_inference = online_features[feature_columns].values
        
        # 6. MAKE PREDICTIONS
        print(f"\n▶ Making predictions...")
        predictions = model.predict(X_inference)
        probabilities = model.predict_proba(X_inference)
        
        # 7. DISPLAY RESULTS
        species_names = {0: "setosa", 1: "versicolor", 2: "virginica"}
        
        print("\n" + "=" * 70)
        print("INFERENCE RESULTS")
        print("=" * 70)
        
        for i, iris_id in enumerate(iris_ids_to_predict):
            pred = predictions[i]
            probs = probabilities[i]
            species = species_names[pred]
            confidence = probs[pred]
            
            print(f"\n🌸 Iris ID: {iris_id}")
            print(f"   Predicted Species: {species}")
            print(f"   Confidence: {confidence:.2%}")
            print(f"   All probabilities:")
            for class_id, prob in enumerate(probs):
                print(f"     - {species_names[class_id]}: {prob:.2%}")
        
        # 8. VERIFY CONSISTENCY
        print("\n" + "=" * 70)
        print("✓ INFERENCE COMPLETE!")
        print("=" * 70)
        print("\nKey Achievement:")
        print("  Your inference used the SAME features as training,")
        print("  fetched from the ONLINE store for real-time serving.")
        print("  This eliminates training-serving skew!")
        
    except Exception as e:
        print(f"\n✗ ERROR during inference: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Did you run 02_train_with_feast.py first?")
        print("2. Did you run 01_materialize_features.py first?")
        print("3. Check that models/iris_model_feast.joblib exists")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    infer_with_feast()
