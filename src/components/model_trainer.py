import os 
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models, load_yaml


@dataclass
class ModelTrainerConfig:
    train_model_file_path = os.path.join("artifacts", "model.pkl")
    model_params_file_path = os.path.join("config", "model_params.yaml")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            # Define models
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbour Regressor": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor()
            }

            # Load hyperparameters from YAML file
            logging.info(f"Loading model parameters from {self.model_trainer_config.model_params_file_path}")
            config = load_yaml(self.model_trainer_config.model_params_file_path)
            params = config.get('model_parameters', {})
            logging.info(f"Loaded parameters for {len(params)} models")

            # Evaluate models with hyperparameter tuning
            logging.info("Starting model evaluation with hyperparameter tuning...")
            model_report: dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                params=params
            )

            logging.info(f"Model evaluation completed. Report: {model_report}")

            # Get best model
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found with R2 score >= 0.6")

            logging.info(f"Best model found: {best_model_name} with R2 score: {best_model_score:.4f}")

            # Save the best model
            save_object(
                file_path=self.model_trainer_config.train_model_file_path,
                obj=best_model
            )
            logging.info(f"Best model saved to {self.model_trainer_config.train_model_file_path}")

            # Calculate final R2 score
            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)

            return r2_square

        except Exception as e:
            logging.error("Error in model trainer", exc_info=True)
            raise CustomException(e, sys)

