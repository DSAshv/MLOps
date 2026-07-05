#!/usr/bin/env python3
"""
Validation Script: Check if all tasks are ready to run
=====================================================

Run this BEFORE recording your video to ensure everything is working.
"""

import os
import sys
from pathlib import Path

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
CHECK = "✓"
CROSS = "✗"


def print_status(condition, message):
    """Print status with color"""
    if condition:
        print(f"{GREEN}{CHECK}{RESET} {message}")
    else:
        print(f"{RED}{CROSS}{RESET} {message}")


def main():
    print(f"{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}FEAST Assignment Validation Script{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    project_root = Path.cwd()
    all_good = True
    
    # 1. Check project structure
    print(f"{BLUE}1. Checking Project Structure{RESET}")
    print("-" * 70)
    
    required_dirs = {
        "feature_repo": "Feature repository",
        "scripts": "Scripts directory",
        "models": "Models directory (for saving trained model)",
        "notebooks": "Notebooks directory",
    }
    
    for dir_name, description in required_dirs.items():
        dir_path = project_root / dir_name
        exists = dir_path.exists()
        print_status(exists, f"{description}: {dir_name}/")
        all_good = all_good and exists
    
    # 2. Check required files
    print(f"\n{BLUE}2. Checking Required Files{RESET}")
    print("-" * 70)
    
    required_files = {
        "feature_repo/feature_store.yaml": "Feast configuration",
        "feature_repo/features.py": "Feature definitions",
        "scripts/01_materialize_features.py": "Materialize script",
        "scripts/02_train_with_feast.py": "Training script",
        "scripts/03_infer_with_feast.py": "Inference script",
        "requirements.txt": "Python dependencies",
        "README.md": "Project README",
        "QUICK_START_VIDEO_GUIDE.md": "Quick start guide",
        "GCP_BIGQUERY_SETUP.py": "GCP setup guide",
        "notebooks/FEAST_Complete_Guide.ipynb": "Jupyter notebook",
    }
    
    for file_name, description in required_files.items():
        file_path = project_root / file_name
        exists = file_path.exists()
        print_status(exists, f"{description}: {file_name}")
        all_good = all_good and exists
    
    # 3. Check data file
    print(f"\n{BLUE}3. Checking Data File{RESET}")
    print("-" * 70)
    
    data_file = project_root / "iris_data_adapted_for_feast.csv"
    data_exists = data_file.exists()
    print_status(data_exists, f"Iris dataset: iris_data_adapted_for_feast.csv")
    
    if not data_exists:
        print(f"\n{RED}WARNING: Data file not found!{RESET}")
        print(f"Please copy iris_data_adapted_for_feast.csv to: {project_root}")
        all_good = False
    
    # 4. Check Python packages
    print(f"\n{BLUE}4. Checking Python Packages{RESET}")
    print("-" * 70)
    
    required_packages = [
        ("feast", "Feast Feature Store"),
        ("pandas", "Pandas"),
        ("sklearn", "Scikit-learn"),
        ("joblib", "Joblib"),
        ("numpy", "NumPy"),
    ]
    
    for package_name, description in required_packages:
        try:
            __import__(package_name)
            print_status(True, f"{description}: {package_name}")
        except ImportError:
            print_status(False, f"{description}: {package_name}")
            print(f"  Install with: pip install {package_name}")
            all_good = False
    
    # 5. Check Feast installation
    print(f"\n{BLUE}5. Checking Feast Setup{RESET}")
    print("-" * 70)
    
    try:
        from feast import FeatureStore
        print_status(True, "Feast FeatureStore import: Success")
        
        # Try to load feature store
        try:
            fs = FeatureStore(repo_path="feature_repo")
            print_status(True, "Feature store initialization: Success")
        except Exception as e:
            print_status(False, f"Feature store initialization: {str(e)}")
            all_good = False
            
    except ImportError:
        print_status(False, "Feast FeatureStore import: Failed")
        all_good = False
    
    # 6. Summary
    print(f"\n{BLUE}{'='*70}{RESET}")
    if all_good and data_exists:
        print(f"{GREEN}✓ ALL CHECKS PASSED! You're ready to go!{RESET}")
        print(f"\nNext steps:")
        print(f"1. Run: python scripts/01_materialize_features.py  (TASK 3)")
        print(f"2. Run: python scripts/02_train_with_feast.py      (TASK 4)")
        print(f"3. Run: python scripts/03_infer_with_feast.py      (TASK 5)")
        return 0
    else:
        print(f"{RED}✗ Some checks failed. Fix issues above before proceeding.{RESET}")
        if not data_exists:
            print(f"\n{RED}CRITICAL: Data file is missing!{RESET}")
            print(f"Copy iris_data_adapted_for_feast.csv to project root")
        return 1


if __name__ == "__main__":
    sys.exit(main())
