"""
TASK 6 (OPTIONAL): GCP BigQuery Backend Configuration
======================================================

This file shows how to configure Feast to use Google Cloud Platform
for production-grade feature storage.

When to use: When you need team-accessible, scalable feature stores
"""

# ============================================
# BEFORE YOU START
# ============================================

# 1. Set up GCP authentication
# Option A (recommended):
#   gcloud auth application-default login
#
# Option B: Set environment variable
#   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"

# 2. Create BigQuery dataset
#   bq mk --dataset --description "Iris Feature Store" iris_features

# 3. Install GCP dependencies
#   pip install google-cloud-bigquery google-cloud-storage


# ============================================
# CONFIGURATION FOR BIGQUERY
# ============================================

# Update your feature_store.yaml with this configuration:

"""
project: iris_feature_store
registry: gs://YOUR_BUCKET_NAME/registry.db
provider: gcp

offline_store:
  type: bigquery
  project: YOUR_GCP_PROJECT_ID      # e.g., "ml-ops-12345"
  dataset: iris_features             # BigQuery dataset name

online_store:
  type: bigquery
  project: YOUR_GCP_PROJECT_ID
  dataset: iris_online_features      # Can be same or different dataset
  # OR use Bigtable for lower latency:
  # type: bigtable
  # project: YOUR_GCP_PROJECT_ID
  # instance: iris-feature-store
"""


# ============================================
# REQUIRED CHANGES TO features.py
# ============================================

# Replace FileSource with BigQuerySource:

"""
from feast.data_sources import BigQuerySource

iris_source = BigQuerySource(
    table="your-gcp-project.iris_features.iris_raw_data",
    timestamp_field="event_timestamp",
)
"""

# Feast will automatically create the BigQuery table when you apply features


# ============================================
# STEP-BY-STEP SETUP FOR GCP
# ============================================

STEPS = """
1. Install GCP tools:
   pip install google-cloud-bigquery google-cloud-storage

2. Authenticate with GCP:
   gcloud auth application-default login
   (This will open a browser for authentication)

3. Set your GCP project:
   export GOOGLE_CLOUD_PROJECT=YOUR_GCP_PROJECT_ID

4. Create BigQuery dataset:
   bq mk --dataset iris_features

5. Upload iris data to BigQuery:
   bq load \\
     iris_features.iris_raw_data \\
     iris_data_adapted_for_feast.csv \\
     --autodetect

6. Create Cloud Storage bucket for registry:
   gsutil mb gs://YOUR_UNIQUE_BUCKET_NAME

7. Update feature_store.yaml:
   - Set registry to: gs://YOUR_UNIQUE_BUCKET_NAME/registry.db
   - Set project to YOUR_GCP_PROJECT_ID
   - Set offline_store dataset to iris_features

8. Update features.py:
   - Change FileSource to BigQuerySource
   - Point to: your-gcp-project.iris_features.iris_raw_data

9. Apply and materialize:
   cd feature_repo
   feast apply
   feast materialize
"""


# ============================================
# TRADE-OFFS: LOCAL vs GCP BigQuery
# ============================================

COMPARISON = """
╔════════════════════╦═══════════════╦═════════════════╗
║ Aspect             ║ SQLite (Local) ║ BigQuery (GCP)  ║
╠════════════════════╬═══════════════╬═════════════════╣
║ Setup Complexity   ║ ✓ Instant     ║ Requires GCP    ║
║ Latency            ║ ~1ms          ║ ~100ms          ║
║ Scalability        ║ Limited       ║ ✓ Unlimited     ║
║ Cost               ║ Free          ║ Pay per query   ║
║ Team Access        ║ Local only    ║ ✓ Team-ready    ║
║ Real-time Updates  ║ Basic         ║ ✓ Excellent     ║
║ Production Ready   ║ No            ║ ✓ Yes           ║
╚════════════════════╩═══════════════╩═════════════════╝

USE LOCAL: Development, testing, learning
USE GCP: Production ML pipelines, team collaboration
"""


# ============================================
# GCP PROJECT SETUP
# ============================================

GCP_SETUP = """
Prerequisites:
- Google Cloud account with billing enabled
- gcloud CLI installed (brew install google-cloud-sdk on macOS)

Quick Start:

1. Create a GCP project:
   gcloud projects create iris-feature-store --name="Iris Feature Store"

2. Set as active project:
   gcloud config set project iris-feature-store

3. Enable required APIs:
   gcloud services enable bigquery.googleapis.com
   gcloud services enable storage.googleapis.com

4. Create service account (for CI/CD):
   gcloud iam service-accounts create feast-user \\
     --display-name="Feast Feature Store User"

5. Grant permissions:
   gcloud projects add-iam-policy-binding iris-feature-store \\
     --member=serviceAccount:feast-user@iris-feature-store.iam.gserviceaccount.com \\
     --role=roles/bigquery.admin
"""


# ============================================
# EXAMPLE: Running in GCP Vertex AI Notebook
# ============================================

VERTEX_AI_SETUP = """
1. Create a Vertex AI Notebook instance:
   - Go to Vertex AI > Workbench > User-managed notebooks
   - Create new notebook with Python 3.10

2. In the notebook terminal:
   pip install -r requirements.txt

3. Upload your iris_data_adapted_for_feast.csv to:
   /home/jupyter/

4. Run the scripts:
   !python scripts/01_materialize_features.py
   !python scripts/02_train_with_feast.py
   !python scripts/03_infer_with_feast.py

5. Authenticate BigQuery:
   from google.colab import auth
   auth.authenticate_user()
"""


# ============================================
# DEBUGGING GCP CONNECTION
# ============================================

DEBUGGING = """
If you get authentication errors:

1. Check authentication:
   gcloud auth list

2. Set default credentials:
   gcloud auth application-default login

3. Verify BigQuery access:
   bq ls

4. Check dataset exists:
   bq ls iris_features

5. Check firewall/permissions in Cloud Console:
   - Go to IAM & Admin > IAM
   - Ensure your user/service account has:
     * BigQuery Admin
     * Storage Admin (for registry bucket)

If data doesn't load to BigQuery:

1. Verify data format:
   - CSV encoding (UTF-8)
   - No special characters in column names
   - Date formats recognized by BigQuery

2. Check table schema:
   bq show --schema iris_features.iris_raw_data

3. Manual upload if needed:
   bq load iris_features.iris_raw_data \\
     iris_data_adapted_for_feast.csv \\
     --autodetect --skip_leading_rows=1
"""


if __name__ == "__main__":
    print(STEPS)
    print("\n" + "="*70 + "\n")
    print(COMPARISON)
    print("\n" + "="*70 + "\n")
    print(GCP_SETUP)
    print("\n" + "="*70 + "\n")
    print(VERTEX_AI_SETUP)
    print("\n" + "="*70 + "\n")
    print(DEBUGGING)
