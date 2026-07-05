# Week 3 Assignment: Feast Feature Store for Iris Pipeline

This week’s assignment adds a Feast feature store to the Iris ML pipeline so that training and inference use the same feature definitions.

## What was done

- Set up a Feast feature repository locally.
- Configured Feast to use a local backend with SQLite for online serving.
- Defined the Iris features once in a central place.
- Used the notebook as the main end-to-end workflow for materialization, training, and inference.

## Files and what they are used for

- `tasks.ipynb`
  - Main notebook for the whole assignment.
  - Run it to install dependencies, materialize features, train the model, and run inference.

- `feature_repo/feature_store.yaml`
  - Feast configuration file.
  - Tells Feast to use the local CSV as the offline store and SQLite as the online store.

- `feature_repo/features.py`
  - Defines the feature schema.
  - Contains the entity, data source, and feature view used by Feast.

- `iris_data_adapted_for_feast.csv`
  - Input dataset used by Feast.
  - This is the source data for offline feature retrieval and materialization.

- `GCP_BIGQUERY_SETUP.py`
  - Optional reference file.
  - Shows how the same setup could be adapted for Google BigQuery in the future.

- `.gitignore`
  - Keeps unnecessary generated files out of the repository.
  - Helps avoid committing local runtime artifacts.

## summary

This assignment shows how to make ML training and inference use the same feature store so the pipeline stays consistent and reliable.
