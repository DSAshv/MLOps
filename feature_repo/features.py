from datetime import timedelta

from feast import Entity, FeatureView, Field
from feast.types import Float32
from feast.data_source import FileSource

# Entity
iris = Entity(
    name="iris",
    join_keys=["iris_id"],
    description="Individual iris plant",
)

# Data Source
iris_source = FileSource(
    path="../iris_data_adapted_for_feast.csv",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# Feature View
iris_measurements = FeatureView(
    name="iris_measurements",
    entities=[iris],
    ttl=timedelta(days=60),
    schema=[
        Field(name="sepal_length", dtype=Float32),
        Field(name="sepal_width", dtype=Float32),
        Field(name="petal_length", dtype=Float32),
        Field(name="petal_width", dtype=Float32),
    ],
    source=iris_source,
)