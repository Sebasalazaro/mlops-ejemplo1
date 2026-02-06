"""
Iris Classification REST API

FastAPI service that serves predictions from a trained Iris classification model.
Accepts flower measurements and returns predicted species.
"""
import sys
from pathlib import Path
import pickle
from typing import List

from fastapi import FastAPI, HTTPException
import pandas as pd

# Add project root to path for config imports
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import (
    API_HOST, API_PORT, API_DEBUG, API_RELOAD,
    MODEL_PATH, TRANSFORMER_PATH, IRIS_FEATURE_COLUMNS
)


def load_model_artifacts():
    """
    Load the trained model and preprocessing transformer from disk.
    
    Returns:
        tuple: (transformer, model)
    
    Raises:
        FileNotFoundError: If model artifacts are not found
    """
    try:
        with open(TRANSFORMER_PATH, 'rb') as f:
            transformer = pickle.load(f)
        
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        
        print(f"Model loaded from: {MODEL_PATH}")
        print(f"Transformer loaded from: {TRANSFORMER_PATH}")
        
        return transformer, model
    
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Model artifacts not found. Please train the model first using src/train.py"
        ) from e


# Initialize FastAPI app
app = FastAPI(
    title="Iris Classification API",
    description="Machine learning API for predicting Iris flower species",
    version="1.0.0"
)

# Load model artifacts at startup
transformer, model = load_model_artifacts()


@app.get("/")
def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: Welcome message and API status
    """
    return {
        "message": "Iris Classification API",
        "status": "active",
        "version": "1.0.0",
        "endpoints": {
            "/get-iris-type": "Predict iris species from measurements"
        }
    }


@app.get("/get-iris-type")
def predict_iris_type(
    sepal_length: float,
    sepal_width: float,
    petal_length: float,
    petal_width: float
) -> List[int]:
    """
    Predict Iris flower species from petal and sepal measurements.
    
    Args:
        sepal_length: Length of sepal in centimeters
        sepal_width: Width of sepal in centimeters
        petal_length: Length of petal in centimeters
        petal_width: Width of petal in centimeters
    
    Returns:
        List[int]: Predicted class label(s)
    
    Example:
        GET /get-iris-type?sepal_length=5.1&sepal_width=3.5&petal_length=1.4&petal_width=0.2
        Returns: [0] (Setosa)
    """
    try:
        # Validate input ranges
        if any(val < 0 for val in [sepal_length, sepal_width, petal_length, petal_width]):
            raise HTTPException(
                status_code=400,
                detail="All measurements must be positive values"
            )
        
        # Create input dataframe with proper column names
        input_data = pd.DataFrame.from_dict({
            IRIS_FEATURE_COLUMNS[0]: [sepal_length],
            IRIS_FEATURE_COLUMNS[1]: [sepal_width],
            IRIS_FEATURE_COLUMNS[2]: [petal_length],
            IRIS_FEATURE_COLUMNS[3]: [petal_width]
        })
        
        # Transform and predict
        transformed_data = transformer.transform(input_data)
        predictions = model.predict(transformed_data)
        
        return predictions.tolist()
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )


@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Service health status
    """
    return {"status": "healthy", "model_loaded": True}