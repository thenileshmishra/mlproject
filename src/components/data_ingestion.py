import os
import sys
from dataclasses import dataclass
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging   

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self, source_path: str) -> Tuple[str, str]:
        """
        Read source_path into a DataFrame, save raw copy, split into train/test,
        save them and return (train_path, test_path).
        """
        logging.info("Entered the data ingestion method/component")
        try:
            if not os.path.exists(source_path):
                raise FileNotFoundError(f"Source file not found: {source_path}")

            df = pd.read_csv(source_path)
            logging.info(f"Read dataset as DataFrame with shape={df.shape}")

            # ensure artifacts dir exists
            artifact_dir = os.path.dirname(self.ingestion_config.train_data_path)
            os.makedirs(artifact_dir, exist_ok=True)

            # save raw data
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info(f"Saved raw data to {self.ingestion_config.raw_data_path}")

            # split
            logging.info("Train/test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # save splits
            train_set.to_csv(self.ingestion_config.train_data_path, index=False)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info(f"Saved train to {self.ingestion_config.train_data_path} and test to {self.ingestion_config.test_data_path}")

            logging.info("Ingestion of the data is completed")
            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path

        except Exception as e:
            logging.exception("Error in data ingestion")
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion("/Users/nileshmishra/MLOPs/notebook/data/StudentsPerformance.csv")
    print(f"Train data path: {train_data}")
    print(f"Test data path: {test_data}")

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)
