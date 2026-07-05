"""
TASK 3: Materialize Features to Online Store
=============================================

This script:
1. Loads the Feast feature store
2. Materializes (copies) features from offline store to online store
3. Makes features available for real-time inference

Run this AFTER defining features in features.py
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from feast import FeatureStore


def materialize_features():
    """Materialize features to online store"""
    
    print("=" * 70)
    print("TASK 3: MATERIALIZING FEATURES TO ONLINE STORE")
    print("=" * 70)
    
    try:
        # Load the feature store
        fs = FeatureStore(repo_path="feature_repo")
        print("✓ Feast Feature Store loaded successfully")
        
        # Materialize features
        # This copies features from the offline store (CSV/BigQuery)
        # into the online store (SQLite/Bigtable) for fast inference
        start_date = datetime.now() - timedelta(days=60)
        end_date = datetime.now()
        
        print(f"\nMaterializing features from {start_date.date()} to {end_date.date()}...")
        fs.materialize(start_date=start_date, end_date=end_date)
        
        print("\n" + "=" * 70)
        print("✓ MATERIALIZATION SUCCESSFUL!")
        print("=" * 70)
        print("\nYour online store is now populated with features for inference.")
        print("You can now use fs.get_online_features() for real-time predictions.")
        
    except Exception as e:
        print(f"\n✗ ERROR during materialization: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Ensure CSV path in features.py is correct")
        print("2. Verify CSV has 'event_timestamp' and 'iris_id' columns")
        print("3. Check that Feast is installed: pip install feast")
        raise


if __name__ == "__main__":
    materialize_features()
