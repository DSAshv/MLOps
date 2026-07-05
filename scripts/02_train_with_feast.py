"""
TASK 4: Fetch Features from Offline Store & Train Model
========================================================

This script:
1. Loads iris data to get entity keys (iris_id) and timestamps
2. Fetches historical features from Feast OFFLINE STORE
3. Trains a RandomForest classifier using Feast features
4. Saves the trained model

Key Point: We read from Feast, not directly from CSV!
This ensures training consistency.
"""

import sys
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from feast import FeatureStore


def train_with_feast():
    """Train model using features fetched from Feast"""
    
    print("=" * 70)
    print("TASK 4: TRAINING WITH FEAST OFFLINE STORE")
    print("=" * 70)
    
    try:
        # 1. LOAD THE FEATURE STORE
        fs = FeatureStore(repo_path="feature_repo")
        print("✓ Feast Feature Store loaded")
        
        # 2. LOAD IRIS DATA TO GET ENTITY KEYS
        iris_data = pd.read_csv("iris_data_adapted_for_feast.csv")
        print(f"✓ Loaded iris data: {iris_data.shape[0]} rows, {iris_data.shape[1]} columns")
        
        # 3. CREATE ENTITY DATAFRAME
        # Feast needs iris_id and event_timestamp to fetch the right features
        entity_df = iris_data[["iris_id", "event_timestamp"]].copy()
        print(f"✓ Created entity DataFrame for feature lookup")
        print(f"\n  Sample entities (first 5):\n{entity_df.head()}")
        
        # 4. FETCH HISTORICAL FEATURES FROM OFFLINE STORE
        print("\n▶ Fetching historical features from Feast offline store...")
        print("  (This reads from your CSV file)")
        
        training_features = fs.get_historical_features(
            entity_df=entity_df,
            features=[
                "iris_measurements:sepal_length",
                "iris_measurements:sepal_width",
                "iris_measurements:petal_length",
                "iris_measurements:petal_width",
                "iris_measurements:species",
            ],
        ).to_df()
        
        print(f"✓ Features fetched successfully!")
        print(f"  Shape: {training_features.shape}")
        print(f"\n  Sample features (first 5):\n{training_features.head()}")
        
        # 5. PREPARE DATA FOR TRAINING
        feature_columns = [
            "sepal_length", "sepal_width", "petal_length", "petal_width"
        ]
        X = training_features[feature_columns].values
        
        # Convert species string to numeric
        species_map = {"setosa": 0, "versicolor": 1, "virginica": 2}
        y = training_features["species"].map(species_map).values
        
        print(f"\n▶ Preparing training data:")
        print(f"  X shape: {X.shape}")
        print(f"  y shape: {y.shape}")
        print(f"  Classes: {species_map}")
        
        # 6. TRAIN THE MODEL
        print(f"\n▶ Training RandomForest classifier...")
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        # Evaluate
        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)
        print(f"✓ Model trained!")
        print(f"  Training accuracy: {accuracy:.2%}")
        
        print(f"\n  Classification Report:\n")
        print(classification_report(y, y_pred, target_names=["setosa", "versicolor", "virginica"]))
        
        # 7. SAVE THE MODEL
        model_path = Path("models") / "iris_model_feast.joblib"
        model_path.parent.mkdir(exist_ok=True)
        joblib.dump(model, str(model_path))
        
        print("=" * 70)
        print(f"✓ MODEL TRAINING COMPLETE!")
        print("=" * 70)
        print(f"Model saved to: {model_path}")
        print(f"\nKey Achievement:")
        print("  Your model was trained using features from Feast,")
        print("  not directly from the CSV. This ensures consistency")
        print("  with how inference will retrieve features!")
        
    except Exception as e:
        print(f"\n✗ ERROR during training: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Did you run 02_materialize_features.py first?")
        print("2. Check that iris_data_adapted_for_feast.csv exists")
        print("3. Verify features.py is correctly defined")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    train_with_feast()
