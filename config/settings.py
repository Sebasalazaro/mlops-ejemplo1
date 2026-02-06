"""
Configuration settings for the MLOps Iris Classification project.
"""
import os
from pathlib import Path

# Project directories
PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"  # For backwards compatibility

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8080))
API_DEBUG = os.getenv("API_DEBUG", "False").lower() == "true"
API_RELOAD = os.getenv("API_RELOAD", "False").lower() == "true"

# Model paths
MODEL_PATH = os.getenv("MODEL_PATH", str(OUTPUTS_DIR / "model.pickle"))
TRANSFORMER_PATH = os.getenv("TRANSFORMER_PATH", str(OUTPUTS_DIR / "transformer.pickle"))

# Training configuration
TEST_SIZE = float(os.getenv("TEST_SIZE", 0.2))
RANDOM_STATE = int(os.getenv("RANDOM_STATE", 42))

# Feature columns for Iris dataset
IRIS_FEATURE_COLUMNS = [
    'sepal length (cm)',
    'sepal width (cm)',
    'petal length (cm)',
    'petal width (cm)'
]
