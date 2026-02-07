"""
Data Storage Module
Handles database operations and data persistence
"""

import sqlite3
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime


class DataStorage:
    """Manages data storage in SQLite database"""
    
    def __init__(self, config):
        self.config = config
        self.db_path = Path(config['database_path'])
        self.logger = logging.getLogger(__name__)
        
        # Ensure database directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._initialize_database()
    
    def _initialize_database(self):
        """Create database and tables if they don't exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create market_data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS market_data (
                    id TEXT,
                    symbol TEXT,
                    name TEXT,
                    current_price REAL,
                    market_cap REAL,
                    total_volume REAL,
                    price_change_24h REAL,
                    price_change_percentage_24h REAL,
                    high_24h REAL,
                    low_24h REAL,
                    fetch_timestamp TEXT,
                    data_source TEXT,
                    PRIMARY KEY (id, fetch_timestamp)
                )
            ''')
            
            # Create news_data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS news_data (
                    title TEXT,
                    description TEXT,
                    author TEXT,
                    content TEXT,
                    source_id TEXT,
                    source_name TEXT,
                    publishedat TEXT,
                    fetch_timestamp TEXT,
                    data_source TEXT,
                    PRIMARY KEY (title, fetch_timestamp)
                )
            ''')
            
            # Create pipeline_metadata table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pipeline_metadata (
                    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_timestamp TEXT,
                    status TEXT,
                    market_records INTEGER,
                    news_records INTEGER,
                    error_message TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Database initialized at: {self.db_path}")
            
        except sqlite3.Error as e:
            self.logger.error(f"Database initialization error: {str(e)}")
            raise
    
    def store_market_data(self, df, if_exists='append'):
        """
        Store market data in database
        
        Args:
            df (pd.DataFrame): Cleaned market data
            if_exists (str): How to behave if table exists ('append', 'replace', 'fail')
        """
        try:
            self.logger.info(f"Storing {len(df)} market records to database...")
            
            conn = sqlite3.connect(self.db_path)
            df.to_sql('market_data', conn, if_exists=if_exists, index=False)
            conn.close()
            
            self.logger.info("Market data stored successfully")
            
        except sqlite3.Error as e:
            self.logger.error(f"Error storing market data: {str(e)}")
            raise
    
    def store_news_data(self, df, if_exists='append'):
        """
        Store news data in database
        
        Args:
            df (pd.DataFrame): Cleaned news data
            if_exists (str): How to behave if table exists ('append', 'replace', 'fail')
        """
        try:
            self.logger.info(f"Storing {len(df)} news records to database...")
            
            conn = sqlite3.connect(self.db_path)
            df.to_sql('news_data', conn, if_exists=if_exists, index=False)
            conn.close()
            
            self.logger.info("News data stored successfully")
            
        except sqlite3.Error as e:
            self.logger.error(f"Error storing news data: {str(e)}")
            raise
    
    def log_pipeline_run(self, status, market_records=0, news_records=0, error_message=None):
        """
        Log pipeline execution metadata
        
        Args:
            status (str): Pipeline run status
            market_records (int): Number of market records processed
            news_records (int): Number of news records processed
            error_message (str): Error message if failed
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO pipeline_metadata 
                (run_timestamp, status, market_records, news_records, error_message)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().strftime(self.config['date_format']),
                status,
                market_records,
                news_records,
                error_message
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Pipeline run logged with status: {status}")
            
        except sqlite3.Error as e:
            self.logger.error(f"Error logging pipeline run: {str(e)}")
    
    def query_latest_market_data(self, limit=10):
        """
        Query latest market data from database
        
        Args:
            limit (int): Number of records to retrieve
            
        Returns:
            pd.DataFrame: Query results
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = f'''
                SELECT * FROM market_data 
                ORDER BY fetch_timestamp DESC 
                LIMIT {limit}
            '''
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            return df
            
        except sqlite3.Error as e:
            self.logger.error(f"Error querying market data: {str(e)}")
            return pd.DataFrame()
    
    def query_latest_news(self, limit=10):
        """
        Query latest news from database
        
        Args:
            limit (int): Number of records to retrieve
            
        Returns:
            pd.DataFrame: Query results
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = f'''
                SELECT * FROM news_data 
                ORDER BY fetch_timestamp DESC 
                LIMIT {limit}
            '''
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            return df
            
        except sqlite3.Error as e:
            self.logger.error(f"Error querying news data: {str(e)}")
            return pd.DataFrame()
    
    def get_pipeline_history(self, limit=10):
        """
        Get pipeline execution history
        
        Args:
            limit (int): Number of runs to retrieve
            
        Returns:
            pd.DataFrame: Pipeline run history
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = f'''
                SELECT * FROM pipeline_metadata 
                ORDER BY run_timestamp DESC 
                LIMIT {limit}
            '''
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            return df
            
        except sqlite3.Error as e:
            self.logger.error(f"Error querying pipeline history: {str(e)}")
            return pd.DataFrame()
    
    def get_database_stats(self):
        """
        Get database statistics
        
        Returns:
            dict: Database statistics
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Count records in each table
            cursor.execute('SELECT COUNT(*) FROM market_data')
            market_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM news_data')
            news_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM pipeline_metadata')
            pipeline_runs = cursor.fetchone()[0]
            
            conn.close()
            
            stats = {
                'total_market_records': market_count,
                'total_news_records': news_count,
                'total_pipeline_runs': pipeline_runs,
                'database_path': str(self.db_path)
            }
            
            return stats
            
        except sqlite3.Error as e:
            self.logger.error(f"Error getting database stats: {str(e)}")
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
    
    storage = DataStorage(config)
    
    # Test with sample data
    sample_df = pd.DataFrame([
        {'id': 'test', 'symbol': 'TST', 'name': 'Test Coin',
         'current_price': 100, 'market_cap': 1000000,
         'fetch_timestamp': datetime.now().strftime(config['date_format']),
         'data_source': 'test'}
    ])
    
    storage.store_market_data(sample_df)
    
    stats = storage.get_database_stats()
    print(f"Database stats: {stats}")
