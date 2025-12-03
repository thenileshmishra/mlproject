import os
import sys
import numpy as np
import pandas as pd
import dill
import yaml

from src.exception import CustomException

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e, sys)


def load_yaml(file_path):
    """Load YAML configuration file"""
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, params=None):
    """
    Evaluate multiple models with optional hyperparameter tuning.

    Args:
        X_train: Training features
        y_train: Training target
        X_test: Test features
        y_test: Test target
        models: Dictionary of model names and model objects
        params: Dictionary of model names and their hyperparameters for GridSearchCV

    Returns:
        report: Dictionary with model names as keys and test R2 scores as values
    """
    try:
        report = {}

        for i in range(len(list(models))):
            model_name = list(models.keys())[i]
            model = list(models.values())[i]

            # Get hyperparameters for the current model if available
            param_grid = params.get(model_name, {}) if params else {}

            if param_grid:
                # Perform GridSearchCV if parameters are provided
                gs = GridSearchCV(model, param_grid, cv=3, n_jobs=-1, verbose=1, scoring='r2')
                gs.fit(X_train, y_train)
                model = gs.best_estimator_
            else:
                # Train model without hyperparameter tuning
                model.fit(X_train, y_train)

            # Make predictions
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            # Calculate scores
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

        return report
    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)