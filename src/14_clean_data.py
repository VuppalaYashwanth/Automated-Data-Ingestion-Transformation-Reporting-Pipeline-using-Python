"""
Data Cleaning Module
Handles data transformation, cleaning, and standardization
"""

import pandas as pd
import numpy as np
import logging
import json
from datetime import datetime
from pathlib import Path


class DataCleaner:
    """Cleans and transforms raw data into structured format"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def clean_market_data(self, raw_data):
        """
        Clean and transform market data
        
        Args:
            raw_data (list/dict): Raw API response
            
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        try:
            self.logger.info("Starting market data cleaning...")
            
            # Convert to DataFrame
            if isinstance(raw_data, list):
                df = pd.DataFrame(raw_data)
            else:
                df = pd.DataFrame([raw_data])
            
            self.logger.info(f"Initial records: {len(df)}")
            
            # Select relevant columns (adjust based on actual API response)
            columns_to_keep = [
                'id', 'symbol', 'name', 'current_price', 'market_cap',
                'total_volume', 'price_change_24h', 'price_change_percentage_24h',
                'high_24h', 'low_24h'
            ]
            
            # Keep only existing columns
            available_columns = [col for col in columns_to_keep if col in df.columns]
            df = df[available_columns]
            
            # Standardize column names
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            
            # Handle missing values
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            df[numeric_columns] = df[numeric_columns].fillna(0)
            
            # Remove duplicates
            df = df.drop_duplicates()
            
            # Add metadata
            df['fetch_timestamp'] = datetime.now().strftime(self.config['date_format'])
            df['data_source'] = 'market_api'
            
            # Data validation
            df = self._validate_market_data(df)
            
            self.logger.info(f"Cleaned records: {len(df)}")
            self.logger.info(f"Columns: {list(df.columns)}")
            
            # Save processed data
            self._save_processed_data(df, 'market_data_cleaned')
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error cleaning market data: {str(e)}")
            raise
    
    def clean_news_data(self, raw_data):
        """
        Clean and transform news data
        
        Args:
            raw_data (dict): Raw API response
            
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        try:
            self.logger.info("Starting news data cleaning...")
            
            # Extract articles from response
            if isinstance(raw_data, dict) and 'articles' in raw_data:
                articles = raw_data['articles']
            elif isinstance(raw_data, list):
                articles = raw_data
            else:
                articles = [raw_data]
            
            df = pd.DataFrame(articles)
            
            self.logger.info(f"Initial records: {len(df)}")
            
            # Flatten nested 'source' column if exists
            if 'source' in df.columns and isinstance(df['source'].iloc[0], dict):
                df['source_id'] = df['source'].apply(lambda x: x.get('id', '') if isinstance(x, dict) else '')
                df['source_name'] = df['source'].apply(lambda x: x.get('name', '') if isinstance(x, dict) else '')
                df = df.drop('source', axis=1)
            
            # Standardize column names
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            
            # Handle missing values
            text_columns = df.select_dtypes(include=['object']).columns
            df[text_columns] = df[text_columns].fillna('')
            
            # Remove duplicates based on title
            if 'title' in df.columns:
                df = df.drop_duplicates(subset=['title'])
            
            # Add metadata
            df['fetch_timestamp'] = datetime.now().strftime(self.config['date_format'])
            df['data_source'] = 'news_api'
            
            # Clean text fields
            df = self._clean_text_fields(df)
            
            self.logger.info(f"Cleaned records: {len(df)}")
            self.logger.info(f"Columns: {list(df.columns)}")
            
            # Save processed data
            self._save_processed_data(df, 'news_data_cleaned')
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error cleaning news data: {str(e)}")
            raise
    
    def _validate_market_data(self, df):
        """Validate market data quality"""
        # Remove records with invalid prices
        if 'current_price' in df.columns:
            df = df[df['current_price'] > 0]
        
        # Remove records with negative market cap
        if 'market_cap' in df.columns:
            df = df[df['market_cap'] >= 0]
        
        return df
    
    def _clean_text_fields(self, df):
        """Clean text fields in news data"""
        text_columns = ['title', 'description', 'content', 'author']
        
        for col in text_columns:
            if col in df.columns:
                # Remove extra whitespace
                df[col] = df[col].str.strip()
                # Remove newlines
                df[col] = df[col].str.replace('\n', ' ', regex=False)
                # Remove multiple spaces
                df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
        
        return df
    
    def _save_processed_data(self, df, filename):
        """Save processed data to CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        processed_path = Path(self.config['processed_data_path'])
        
        # Ensure directory exists
        processed_path.mkdir(parents=True, exist_ok=True)
        
        output_path = processed_path / f"{filename}_{timestamp}.csv"
        
        df.to_csv(output_path, index=False)
        self.logger.info(f"Processed data saved to: {output_path}")
    
    def merge_datasets(self, market_df, news_df):
        """
        Optional: Create a combined dataset with summary statistics
        
        Args:
            market_df (pd.DataFrame): Cleaned market data
            news_df (pd.DataFrame): Cleaned news data
            
        Returns:
            dict: Combined summary statistics
        """
        try:
            summary = {
                'market_summary': {
                    'total_records': len(market_df),
                    'total_market_cap': float(market_df['market_cap'].sum()) if 'market_cap' in market_df.columns else 0,
                    'avg_price': float(market_df['current_price'].mean()) if 'current_price' in market_df.columns else 0
                },
                'news_summary': {
                    'total_articles': len(news_df),
                    'unique_sources': int(news_df['source_name'].nunique()) if 'source_name' in news_df.columns else 0
                },
                'timestamp': datetime.now().strftime(self.config['date_format'])
            }
            
            self.logger.info("Datasets merged successfully")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error merging datasets: {str(e)}")
            return {}


if __name__ == "__main__":
    # Test module independently
    import json
    
    with open('../config.json', 'r') as f:
        config = json.load(f)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    cleaner = DataCleaner(config)
    
    # Test with sample data
    sample_market = [
        {'id': 'bitcoin', 'symbol': 'btc', 'name': 'Bitcoin', 
         'current_price': 50000, 'market_cap': 1000000000}
    ]
    
    sample_news = {
        'articles': [
            {'title': 'Test Article', 'description': 'Test', 'author': 'Test Author',
             'source': {'id': 'test', 'name': 'Test Source'}}
        ]
    }
    
    market_clean = cleaner.clean_market_data(sample_market)
    news_clean = cleaner.clean_news_data(sample_news)
    
    print(f"Market data shape: {market_clean.shape}")
    print(f"News data shape: {news_clean.shape}")
