"""
Iris Classification Model Training Script

This script trains a baseline Iris flower classification model using scikit-learn.
It creates a preprocessing pipeline and a DummyClassifier, then saves both for API deployment.
"""
import sys
from pathlib import Path
import pickle

from sklearn.compose import ColumnTransformer
from sklearn.datasets import load_iris
from sklearn.dummy import DummyClassifier
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import TEST_SIZE, RANDOM_STATE


def load_data():
    """
    Load the Iris dataset from scikit-learn.
    
    Returns:
        tuple: Features (X) and target (y) as pandas DataFrames
    """
    iris = load_iris(as_frame=True)
    return iris.data, iris.target


def create_preprocessing_pipeline():
    """
    Create preprocessing pipelines for numerical and categorical features.
    
    Returns:
        ColumnTransformer: Fitted preprocessing transformer
    """
    # Numerical pipeline: scaling and variance filtering
    numeric_pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('selector', VarianceThreshold())
    ])
    
    # Categorical pipeline: one-hot encoding
    categorical_pipe = Pipeline([
        ('encoder', OneHotEncoder(drop='first'))
    ])
    
    return numeric_pipe, categorical_pipe


def train_model(X_train, X_test, y_train, y_test):
    """
    Train a baseline classifier with preprocessing pipeline.
    
    Args:
        X_train: Training features
        X_test: Testing features
        y_train: Training labels
        y_test: Testing labels
    
    Returns:
        tuple: Fitted transformer and trained model
    """
    # Identify column types
    numeric_cols = X_train._get_numeric_data().columns.tolist()
    cat_cols = X_train.columns[~X_train.columns.isin(numeric_cols)].tolist()
    
    # Create preprocessing pipelines
    numeric_pipe, categorical_pipe = create_preprocessing_pipeline()
    
    # Create column transformer
    col_transformer = ColumnTransformer([
        ('numeric', numeric_pipe, numeric_cols),
        ('categoric', categorical_pipe, cat_cols)
    ])
    
    # Fit transformer and transform data
    col_transformer_fitted = col_transformer.fit(X_train)
    X_train_transformed = col_transformer_fitted.transform(X_train)
    X_test_transformed = col_transformer_fitted.transform(X_test)
    
    # Train baseline model
    model = DummyClassifier()
    model_fitted = model.fit(X_train_transformed, y_train)
    
    # Calculate accuracy
    train_score = model_fitted.score(X_train_transformed, y_train)
    test_score = model_fitted.score(X_test_transformed, y_test)
    
    print(f"Training accuracy: {train_score:.4f}")
    print(f"Testing accuracy: {test_score:.4f}")
    
    return col_transformer_fitted, model_fitted


def save_artifacts(transformer, model, output_dir='outputs'):
    """
    Save trained transformer and model to disk.
    
    Args:
        transformer: Fitted preprocessing transformer
        model: Trained classification model
        output_dir: Directory to save artifacts (default: 'outputs')
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    transformer_path = output_path / 'transformer.pickle'
    model_path = output_path / 'model.pickle'
    
    with open(transformer_path, 'wb') as f:
        pickle.dump(transformer, f)
    print(f"Transformer saved to: {transformer_path}")
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to: {model_path}")


def main():
    """Main training pipeline execution."""
    print("Starting Iris classification model training...")
    
    # Load data
    X, y = load_data()
    print(f"Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )
    print(f"Data split: {len(X_train)} training samples, {len(X_test)} testing samples")
    
    # Train model
    transformer, model = train_model(X_train, X_test, y_train, y_test)
    
    # Save artifacts
    save_artifacts(transformer, model)
    
    print("Training completed successfully!")


if __name__ == "__main__":
    main()