# data_ingestion.py

import pandas as pd
import os
import sys
from src.exception import CustomException
from src.logger import logging

class DataIngestion:
    def __init__(self):
        pass

    def load_data(self, file_path):
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File '{file_path}' not found.")

            # Load data from file
            data = pd.read_csv(file_path)

            # Optionally, perform any preprocessing steps here

            return data

        except Exception as e:
            logging.error(f"Error occurred during data ingestion: {e}")
            raise CustomException(e, sys)

# Example usage:
if __name__ == "__main__":
    # Initialize DataIngestion object
    data_ingestion = DataIngestion()

    # Specify the file path of the dataset
    file_path = "notebooks/data/train_data (2).json"

    # Load the data
    data = data_ingestion.load_data(file_path)

    # Optionally, you can perform further operations with the loaded data
    print(data.head())
