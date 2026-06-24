"""
Visualization Module
Creates plots and visualizations for exploratory data analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class Visualizer:
    """Class to create visualizations for EDA."""
    
    def __init__(self, df, output_dir='reports/figures'):
        """
        Initialize Visualizer.
        
        Args:
            df (pd.DataFrame): Input dataframe
            output_dir (str): Directory to save figures
        """
        self.df = df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def distribution_plot(self, col, figsize=(10, 5), save=True):
        """
        Create distribution plot for a numeric column.
        
        Args:
            col (str): Column name
            figsize (tuple): Figure size
            save (bool): Save figure to file
        """
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Histogram
        axes[0].hist(self.df[col], bins=30, edgecolor='black', alpha=0.7, color='skyblue')
        axes[0].set_title(f'Distribution of {col}', fontsize=14, fontweight='bold')
        axes[0].set_xlabel(col)
        axes[0].set_ylabel('Frequency')
        axes[0].grid(alpha=0.3)
        
        # KDE plot
        self.df[col].plot(kind='density', ax=axes[1], color='red', linewidth=2)
        axes[1].set_title(f'KDE Plot of {col}', fontsize=14, fontweight='bold')
        axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            filename = f"{col}_distribution.png"
            plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
            logger.info(f"Saved: {filename}")
        
        return fig, axes
    
    def boxplot(self, col, figsize=(10, 5), save=True):
        """
        Create boxplot for a numeric column.
        
        Args:
            col (str): Column name
            figsize (tuple): Figure size
            save (bool): Save figure to file
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        box = ax.boxplot(self.df[col].dropna(), patch_artist=True)
        box['boxes'][0].set_facecolor('lightblue')
        
        ax.set_title(f'Boxplot of {col}', fontsize=14, fontweight='bold')
        ax.set_ylabel(col)
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            filename = f"{col}_boxplot.png"
            plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
            logger.info(f"Saved: {filename}")
        
        return fig, ax
    
    def correlation_heatmap(self, figsize=(12, 10), save=True):
        """
        Create correlation heatmap.
        
        Args:
            figsize (tuple): Figure size
            save (bool): Save figure to file
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        corr_matrix = self.df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, square=True, ax=ax, cbar_kws={'label': 'Correlation'})
        
        ax.set_title('Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if save:
            filename = "correlation_heatmap.png"
            plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
            logger.info(f"Saved: {filename}")
        
        return fig, ax
    
    def scatter_plot(self, col1, col2, figsize=(10, 6), save=True):
        """
        Create scatter plot between two variables.
        
        Args:
            col1 (str): First column
            col2 (str): Second column
            figsize (tuple): Figure size
            save (bool): Save figure to file
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.scatter(self.df[col1], self.df[col2], alpha=0.6, s=50, color='steelblue')
        ax.set_xlabel(col1, fontsize=12)
        ax.set_ylabel(col2, fontsize=12)
        ax.set_title(f'{col1} vs {col2}', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        
        # Add correlation coefficient
        corr = self.df[[col1, col2]].corr().iloc[0, 1]
        ax.text(0.05, 0.95, f'Correlation: {corr:.3f}', 
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        if save:
            filename = f"{col1}_vs_{col2}_scatter.png"
            plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
            logger.info(f"Saved: {filename}")
        
        return fig, ax
    
    def categorical_bar_plot(self, col, figsize=(10, 6), save=True):
        """
        Create bar plot for categorical variable.
        
        Args:
            col (str): Column name
            figsize (tuple): Figure size
            save (bool): Save figure to file
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        value_counts = self.df[col].value_counts()
        value_counts.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
        
        ax.set_title(f'Distribution of {col}', fontsize=14, fontweight='bold')
        ax.set_xlabel(col)
        ax.set_ylabel('Count')
        ax.grid(alpha=0.3, axis='y')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        
        if save:
            filename = f"{col}_barplot.png"
            plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
            logger.info(f"Saved: {filename}")
        
        return fig, ax
    
    def pie_chart(self, col, figsize=(8, 8), save=True):
        """
        Create pie chart for categorical variable.
        
        Args:
            col (str): Column name
            figsize (tuple): Figure size
            save (bool): Save figure to file
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        value_counts = self.df[col].value_counts()
        colors = plt.cm.Set3(np.linspace(0, 1, len(value_counts)))
        
        ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%',
               colors=colors, startangle=90)
        ax.set_title(f'Distribution of {col}', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            filename = f"{col}_pie.png"
            plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
            logger.info(f"Saved: {filename}")
        
        return fig, ax
    
    def pair_plot(self, columns=None, figsize=(15, 15), save=True):
        """
        Create pair plot for numeric columns.
        
        Args:
            columns (list): Columns to include
            figsize (tuple): Figure size
            save (bool): Save figure to file
        """
        if columns is None:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            columns = numeric_cols[:5]  # Limit to first 5 for clarity
        
        fig = sns.pairplot(self.df[columns], diag_kind='hist', plot_kws={'alpha': 0.6})
        fig.fig.suptitle('Pair Plot', fontsize=16, fontweight='bold', y=0.995)
        
        if save:
            filename = "pairplot.png"
            fig.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
            logger.info(f"Saved: {filename}")
        
        return fig
    
    def grouped_boxplot(self, group_col, value_col, figsize=(12, 6), save=True):
        """
        Create boxplot grouped by categorical variable.
        
        Args:
            group_col (str): Column to group by
            value_col (str): Value column
            figsize (tuple): Figure size
            save (bool): Save figure to file
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.boxplot(data=self.df, x=group_col, y=value_col, ax=ax, palette='Set2')
        
        ax.set_title(f'{value_col} by {group_col}', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save:
            filename = f"{value_col}_by_{group_col}_boxplot.png"
            plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
            logger.info(f"Saved: {filename}")
        
        return fig, ax
    
    def violin_plot(self, col, figsize=(10, 6), save=True):
        """
        Create violin plot for numeric distribution.
        
        Args:
            col (str): Column name
            figsize (tuple): Figure size
            save (bool): Save figure to file
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        parts = ax.violinplot(self.df[col].dropna(), positions=[0], showmeans=True)
        
        ax.set_title(f'Violin Plot of {col}', fontsize=14, fontweight='bold')
        ax.set_ylabel(col)
        ax.set_xticks([])
        ax.grid(alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save:
            filename = f"{col}_violin.png"
            plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
            logger.info(f"Saved: {filename}")
        
        return fig, ax
    
    def close_all(self):
        """Close all matplotlib figures."""
        plt.close('all')


def create_all_visualizations(df, output_dir='reports/figures'):
    """
    Create a comprehensive set of visualizations.
    
    Args:
        df (pd.DataFrame): Input dataframe
        output_dir (str): Directory to save figures
    """
    viz = Visualizer(df, output_dir)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # Distribution plots for numeric columns
    for col in numeric_cols[:6]:  # Limit to first 6
        viz.distribution_plot(col)
        viz.boxplot(col)
    
    # Correlation heatmap
    viz.correlation_heatmap()
    
    # Categorical plots
    for col in categorical_cols[:4]:  # Limit to first 4
        viz.categorical_bar_plot(col)
        viz.pie_chart(col)
    
    # Scatter plots for top correlations
    if len(numeric_cols) >= 2:
        viz.scatter_plot(numeric_cols[0], numeric_cols[1])
    
    viz.close_all()
    logger.info("All visualizations created successfully")


if __name__ == "__main__":
    # Example usage
    df = pd.read_csv("data/raw_data.csv")
    create_all_visualizations(df)
