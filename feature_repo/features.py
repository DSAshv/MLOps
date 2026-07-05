"""
Feast Feature Definitions for Iris Dataset
============================================

This file defines:
- ENTITY: iris (identifies individual iris plants)
- DATA SOURCE: CSV file with iris measurements
- FEATURE VIEW: iris_measurements (all features grouped together)
"""

from feast import Entity, FeatureView, FeatureStore
from feast.data_sources import FileSource
from datetime import timedelta


# ============================================
# TASK 2: DEFINE ENTITIES, DATA SOURCES & FEATURE VIEWS
# ============================================

# 1. ENTITY: What uniquely identifies each iris
iris = Entity(
    name="iris",
    description="Individual iris plant identifier",
    join_key="iris_id",  # Column name in your CSV that identifies each plant
)


# 2. DATA SOURCE: Where Feast reads the raw features
iris_source = FileSource(
    path="../iris_data_adapted_for_feast.csv",  # Path to your CSV file
    timestamp_field="event_timestamp",  # Column with measurement timestamps
)


# 3. FEATURE VIEW: Logical grouping of all iris features
iris_measurements = FeatureView(
    name="iris_measurements",
    description="Iris flower measurements and species",
    entities=[iris],
    ttl=timedelta(days=60),  # Keep features for 60 days
    features=[
        ("sepal_length", "float"),
        ("sepal_width", "float"),
        ("petal_length", "float"),
        ("petal_width", "float"),
        ("species", "string"),
    ],
    input=iris_source,
    tags={"team": "mlops", "dataset": "iris"},
)
