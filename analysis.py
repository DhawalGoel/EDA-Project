"""
Statistical Analysis Module
Performs statistical tests and correlation analysis.
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import skew, kurtosis, shapiro, mannwhitneyu, spearmanr
import logging

logger = logging.getLogger(__name__)


class StatisticalAnalysis:
    """Class to perform statistical analysis on data."""
    
    def __init__(self, df):
        """
        Initialize analyzer with dataframe.
        
        Args:
            df (pd.DataFrame): Input dataframe
        """
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns
        self.categorical_cols = df.select_dtypes(include=['object']).columns
        
    def summary_statistics(self):
        """
        Calculate comprehensive summary statistics.
        
        Returns:
            pd.DataFrame: Summary statistics
        """
        summary = pd.DataFrame({
            'Count': self.df[self.numeric_cols].count(),
            'Mean': self.df[self.numeric_cols].mean(),
            'Std Dev': self.df[self.numeric_cols].std(),
            'Min': self.df[self.numeric_cols].min(),
            '25%': self.df[self.numeric_cols].quantile(0.25),
            'Median': self.df[self.numeric_cols].median(),
            '75%': self.df[self.numeric_cols].quantile(0.75),
            'Max': self.df[self.numeric_cols].max(),
            'Skewness': self.df[self.numeric_cols].apply(skew),
            'Kurtosis': self.df[self.numeric_cols].apply(kurtosis)
        })
        
        logger.info("Summary statistics calculated")
        return summary
    
    def correlation_analysis(self, method='pearson'):
        """
        Calculate correlation matrix.
        
        Args:
            method (str): 'pearson', 'spearman', or 'kendall'
            
        Returns:
            pd.DataFrame: Correlation matrix
        """
        corr_matrix = self.df[self.numeric_cols].corr(method=method)
        
        logger.info(f"Correlation analysis completed using {method} method")
        return corr_matrix
    
    def get_top_correlations(self, target_col=None, top_n=10):
        """
        Get top correlations for a specific column or overall.
        
        Args:
            target_col (str): Column to find correlations for
            top_n (int): Number of top correlations to return
            
        Returns:
            pd.Series: Top correlations
        """
        corr_matrix = self.correlation_analysis()
        
        if target_col:
            if target_col not in corr_matrix.columns:
                raise ValueError(f"Column {target_col} not found")
            
            correlations = corr_matrix[target_col].drop(target_col).sort_values(ascending=False)
        else:
            # Get top correlations across entire matrix
            corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_pairs.append({
                        'Variable 1': corr_matrix.columns[i],
                        'Variable 2': corr_matrix.columns[j],
                        'Correlation': corr_matrix.iloc[i, j]
                    })
            
            correlations = pd.DataFrame(corr_pairs).sort_values('Correlation', ascending=False)
        
        return correlations.head(top_n)
    
    def normality_test(self, alpha=0.05):
        """
        Perform Shapiro-Wilk normality test.
        
        Args:
            alpha (float): Significance level
            
        Returns:
            pd.DataFrame: Test results
        """
        results = []
        
        for col in self.numeric_cols:
            stat, p_value = shapiro(self.df[col])
            is_normal = "Yes" if p_value > alpha else "No"
            
            results.append({
                'Variable': col,
                'Statistic': stat,
                'P-Value': p_value,
                'Normal (α=0.05)': is_normal
            })
        
        logger.info("Normality tests completed")
        return pd.DataFrame(results)
    
    def distribution_analysis(self, col):
        """
        Analyze distribution of a single variable.
        
        Args:
            col (str): Column name
            
        Returns:
            dict: Distribution metrics
        """
        if col not in self.df.columns:
            raise ValueError(f"Column {col} not found")
        
        data = self.df[col].dropna()
        
        analysis = {
            'Variable': col,
            'Count': len(data),
            'Mean': data.mean(),
            'Median': data.median(),
            'Mode': data.mode()[0] if len(data.mode()) > 0 else np.nan,
            'Std Dev': data.std(),
            'Variance': data.var(),
            'Skewness': skew(data),
            'Kurtosis': kurtosis(data),
            'Min': data.min(),
            'Max': data.max(),
            'Range': data.max() - data.min(),
            'IQR': data.quantile(0.75) - data.quantile(0.25)
        }
        
        return analysis
    
    def categorical_analysis(self):
        """
        Analyze categorical variables.
        
        Returns:
            dict: Categorical analysis for each column
        """
        analysis = {}
        
        for col in self.categorical_cols:
            value_counts = self.df[col].value_counts()
            analysis[col] = {
                'Unique Values': self.df[col].nunique(),
                'Value Counts': value_counts.to_dict(),
                'Mode': value_counts.index[0],
                'Mode Frequency': value_counts.values[0],
                'Mode Percentage': (value_counts.values[0] / len(self.df)) * 100
            }
        
        logger.info("Categorical analysis completed")
        return analysis
    
    def missing_data_analysis(self):
        """
        Analyze missing data patterns.
        
        Returns:
            pd.DataFrame: Missing data report
        """
        missing_report = pd.DataFrame({
            'Column': self.df.columns,
            'Missing Count': self.df.isnull().sum().values,
            'Missing %': (self.df.isnull().sum().values / len(self.df)) * 100
        })
        
        missing_report = missing_report[missing_report['Missing Count'] > 0]
        
        logger.info("Missing data analysis completed")
        return missing_report
    
    def outlier_analysis(self, method='iqr', columns=None):
        """
        Identify and analyze outliers.
        
        Args:
            method (str): 'iqr' or 'zscore'
            columns (list): Columns to analyze (default: all numeric)
            
        Returns:
            dict: Outlier analysis results
        """
        if columns is None:
            columns = self.numeric_cols
        
        outlier_info = {}
        
        if method == 'iqr':
            for col in columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                
                outlier_mask = (self.df[col] < lower) | (self.df[col] > upper)
                
                outlier_info[col] = {
                    'Outlier Count': outlier_mask.sum(),
                    'Outlier %': (outlier_mask.sum() / len(self.df)) * 100,
                    'Lower Bound': lower,
                    'Upper Bound': upper,
                    'Outlier Values': self.df[outlier_mask][col].values.tolist()
                }
        
        elif method == 'zscore':
            from scipy.stats import zscore
            
            for col in columns:
                z_scores = np.abs(zscore(self.df[col].dropna()))
                threshold = 3
                
                outlier_mask = z_scores > threshold
                
                outlier_info[col] = {
                    'Outlier Count': outlier_mask.sum(),
                    'Outlier %': (outlier_mask.sum() / len(self.df)) * 100
                }
        
        logger.info(f"Outlier analysis completed using {method} method")
        return outlier_info
    
    def group_comparison(self, group_col, target_col):
        """
        Compare target variable across groups.
        
        Args:
            group_col (str): Column to group by
            target_col (str): Column to compare
            
        Returns:
            pd.DataFrame: Group statistics
        """
        return self.df.groupby(group_col)[target_col].describe()
    
    def variance_analysis(self):
        """
        Calculate variance for all numeric columns.
        
        Returns:
            pd.Series: Variance for each numeric column
        """
        return self.df[self.numeric_cols].var()


def analyze_dataset(df):
    """
    Perform complete statistical analysis on dataset.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        dict: Complete analysis results
    """
    analyzer = StatisticalAnalysis(df)
    
    results = {
        'summary_statistics': analyzer.summary_statistics(),
        'correlation_matrix': analyzer.correlation_analysis(),
        'top_correlations': analyzer.get_top_correlations(top_n=15),
        'normality_tests': analyzer.normality_test(),
        'missing_data': analyzer.missing_data_analysis(),
        'outliers': analyzer.outlier_analysis(method='iqr'),
        'categorical': analyzer.categorical_analysis()
    }
    
    return results


if __name__ == "__main__":
    # Example usage
    df = pd.read_csv("data/raw_data.csv")
    analysis = analyze_dataset(df)
    
    print("\n=== Summary Statistics ===")
    print(analysis['summary_statistics'])
    
    print("\n=== Correlation Matrix ===")
    print(analysis['correlation_matrix'])
    
    print("\n=== Top Correlations ===")
    print(analysis['top_correlations'])
