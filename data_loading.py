"""
Data Loading Module
Handles loading, validation, and initial exploration of the dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataLoader:
    """Class to handle data loading and initial validation."""
    
    def __init__(self, data_path):
        """
        Initialize DataLoader with path to data file.
        
        Args:
            data_path (str): Path to the CSV file
        """
        self.data_path = Path(data_path)
        self.df = None
        
    def load_data(self):
        """
        Load CSV file into pandas DataFrame.
        
        Returns:
            pd.DataFrame: Loaded dataset
        """
        try:
            logger.info(f"Loading data from {self.data_path}")
            self.df = pd.read_csv(self.data_path)
            logger.info(f"Data loaded successfully: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            return self.df
        except FileNotFoundError:
            logger.error(f"File not found: {self.data_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def validate_data(self):
        """
        Perform basic data validation.
        
        Returns:
            dict: Validation results
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        validation_results = {
            'shape': self.df.shape,
            'missing_values': self.df.isnull().sum().to_dict(),
            'duplicates': self.df.duplicated().sum(),
            'dtypes': self.df.dtypes.to_dict(),
            'memory_usage': self.df.memory_usage(deep=True).sum() / 1024**2  # in MB
        }
        
        logger.info("Data validation completed")
        logger.info(f"Missing values: {validation_results['missing_values']}")
        logger.info(f"Duplicate rows: {validation_results['duplicates']}")
        logger.info(f"Memory usage: {validation_results['memory_usage']:.2f} MB")
        
        return validation_results
    
    def get_summary(self):
        """
        Get summary statistics of the dataset.
        
        Returns:
            pd.DataFrame: Summary statistics
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        return self.df.describe()
    
    def get_info(self):
        """
        Display detailed information about the dataset.
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        return self.df.info()
    
    def get_dataframe(self):
        """
        Get the loaded dataframe.
        
        Returns:
            pd.DataFrame: The loaded dataset
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        return self.df


def load_and_validate(data_path):
    """
    Convenience function to load and validate data.
    
    Args:
        data_path (str): Path to CSV file
        
    Returns:
        pd.DataFrame: Validated dataset
    """
    loader = DataLoader(data_path)
    df = loader.load_data()
    validation = loader.validate_data()
    
    print("\n=== Dataset Overview ===")
    print(f"Shape: {validation['shape']}")
    print(f"\nData Types:\n{pd.Series(validation['dtypes'])}")
    print(f"\nMissing Values:\n{pd.Series(validation['missing_values'])}")
    print(f"Duplicate Rows: {validation['duplicates']}")
    print(f"Memory Usage: {validation['memory_usage']:.2f} MB")
    
    return df


if __name__ == "__main__":
    # Example usage
    DATA_PATH = "data/raw_data.csv"
    df = load_and_validate(DATA_PATH)
    print("\n=== Summary Statistics ===")
    print(df.describe())
