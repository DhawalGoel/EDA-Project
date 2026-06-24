"""
Data Preprocessing Module
Handles data cleaning, transformation, and feature engineering.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import logging

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Class to handle data cleaning and preprocessing."""
    
    def __init__(self, df):
        """
        Initialize preprocessor with dataframe.
        
        Args:
            df (pd.DataFrame): Input dataframe
        """
        self.df = df.copy()
        self.original_df = df.copy()
        
    def handle_missing_values(self, strategy='drop'):
        """
        Handle missing values.
        
        Args:
            strategy (str): 'drop' or 'mean' or 'median'
            
        Returns:
            pd.DataFrame: Dataset with missing values handled
        """
        missing_count = self.df.isnull().sum().sum()
        
        if missing_count == 0:
            logger.info("No missing values found")
            return self.df
        
        if strategy == 'drop':
            self.df = self.df.dropna()
            logger.info(f"Dropped {missing_count} rows with missing values")
        elif strategy == 'mean':
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
            logger.info("Filled numeric columns with mean")
        elif strategy == 'median':
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
            logger.info("Filled numeric columns with median")
        
        return self.df
    
    def detect_outliers(self, method='iqr', threshold=1.5):
        """
        Detect outliers using IQR method.
        
        Args:
            method (str): 'iqr' or 'zscore'
            threshold (float): IQR multiplier or zscore threshold
            
        Returns:
            dict: Outlier information for each numeric column
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        outliers = {}
        
        if method == 'iqr':
            for col in numeric_cols:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                outlier_mask = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
                outliers[col] = {
                    'count': outlier_mask.sum(),
                    'percentage': (outlier_mask.sum() / len(self.df)) * 100,
                    'bounds': (lower_bound, upper_bound)
                }
        
        elif method == 'zscore':
            from scipy import stats
            for col in numeric_cols:
                z_scores = np.abs(stats.zscore(self.df[col]))
                outlier_mask = z_scores > threshold
                
                outliers[col] = {
                    'count': outlier_mask.sum(),
                    'percentage': (outlier_mask.sum() / len(self.df)) * 100
                }
        
        logger.info(f"Outlier detection completed using {method}")
        return outliers
    
    def remove_outliers(self, method='iqr', threshold=1.5):
        """
        Remove outliers from the dataset.
        
        Args:
            method (str): 'iqr' or 'zscore'
            threshold (float): IQR multiplier or zscore threshold
            
        Returns:
            pd.DataFrame: Dataset without outliers
        """
        initial_rows = len(self.df)
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if method == 'iqr':
            for col in numeric_cols:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
        
        removed_rows = initial_rows - len(self.df)
        logger.info(f"Removed {removed_rows} rows with outliers")
        
        return self.df
    
    def normalize_numeric(self):
        """
        Normalize numeric columns to 0-1 range.
        
        Returns:
            pd.DataFrame: Dataset with normalized columns
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            min_val = self.df[col].min()
            max_val = self.df[col].max()
            
            if max_val != min_val:
                self.df[col] = (self.df[col] - min_val) / (max_val - min_val)
        
        logger.info("Numeric columns normalized")
        return self.df
    
    def standardize_numeric(self):
        """
        Standardize numeric columns (z-score normalization).
        
        Returns:
            pd.DataFrame: Dataset with standardized columns
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        scaler = StandardScaler()
        
        self.df[numeric_cols] = scaler.fit_transform(self.df[numeric_cols])
        
        logger.info("Numeric columns standardized")
        return self.df
    
    def encode_categorical(self, method='label'):
        """
        Encode categorical variables.
        
        Args:
            method (str): 'label' or 'onehot'
            
        Returns:
            pd.DataFrame: Dataset with encoded categorical columns
        """
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        if method == 'label':
            le = LabelEncoder()
            for col in categorical_cols:
                self.df[col] = le.fit_transform(self.df[col].astype(str))
                logger.info(f"Label encoded: {col}")
        
        elif method == 'onehot':
            self.df = pd.get_dummies(self.df, columns=categorical_cols, drop_first=True)
            logger.info(f"One-hot encoded: {list(categorical_cols)}")
        
        return self.df
    
    def create_features(self):
        """
        Create derived features.
        
        Returns:
            pd.DataFrame: Dataset with new features
        """
        # Example: Create customer tenure feature
        if 'Customer_Since' in self.df.columns:
            self.df['Customer_Since'] = pd.to_datetime(self.df['Customer_Since'])
            reference_date = pd.Timestamp('2024-06-01')
            self.df['Tenure_Days'] = (reference_date - self.df['Customer_Since']).dt.days
            self.df['Tenure_Years'] = self.df['Tenure_Days'] / 365.25
            logger.info("Created tenure features")
        
        # Example: Create spending to income ratio
        if 'Monthly_Spending' in self.df.columns and 'Annual_Income' in self.df.columns:
            self.df['Spending_Income_Ratio'] = (
                (self.df['Monthly_Spending'] * 12) / self.df['Annual_Income']
            )
            logger.info("Created spending to income ratio feature")
        
        return self.df
    
    def get_processed_data(self):
        """
        Get the preprocessed dataframe.
        
        Returns:
            pd.DataFrame: Processed dataset
        """
        return self.df
    
    def get_original_data(self):
        """
        Get the original dataframe.
        
        Returns:
            pd.DataFrame: Original dataset
        """
        return self.original_df


def preprocess_pipeline(df, handle_missing=True, remove_outliers_flag=False, 
                       normalize=False, encode_cat=False, engineer_features=True):
    """
    Complete preprocessing pipeline.
    
    Args:
        df (pd.DataFrame): Input dataframe
        handle_missing (bool): Handle missing values
        remove_outliers_flag (bool): Remove outliers
        normalize (bool): Normalize numeric columns
        encode_cat (bool): Encode categorical variables
        engineer_features (bool): Create derived features
        
    Returns:
        pd.DataFrame: Processed dataset
    """
    preprocessor = DataPreprocessor(df)
    
    if handle_missing:
        preprocessor.handle_missing_values(strategy='drop')
    
    if engineer_features:
        preprocessor.create_features()
    
    if remove_outliers_flag:
        preprocessor.remove_outliers(method='iqr')
    
    if normalize:
        preprocessor.normalize_numeric()
    
    if encode_cat:
        preprocessor.encode_categorical(method='label')
    
    return preprocessor.get_processed_data()


if __name__ == "__main__":
    # Example usage
    df = pd.read_csv("data/raw_data.csv")
    processed_df = preprocess_pipeline(df, engineer_features=True)
    print(processed_df.head())
