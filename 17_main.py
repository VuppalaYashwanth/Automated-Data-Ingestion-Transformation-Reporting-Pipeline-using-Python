"""
Main Pipeline Orchestrator
Coordinates the entire data pipeline execution
"""

import logging
import json
import sys
from pathlib import Path
from datetime import datetime

# Import pipeline modules
from fetch_data import DataFetcher
from clean_data import DataCleaner
from store_data import DataStorage
from generate_report import ReportGenerator


class DataPipeline:
    """Main pipeline orchestrator for data ingestion, cleaning, and reporting"""
    
    def __init__(self, config_path='../config.json'):
        """
        Initialize pipeline with configuration
        
        Args:
            config_path (str): Path to configuration file
        """
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Setup logging
        self._setup_logging()
        
        # Initialize pipeline components
        self.fetcher = DataFetcher(self.config)
        self.cleaner = DataCleaner(self.config)
        self.storage = DataStorage(self.config)
        self.reporter = ReportGenerator(self.config)
        
        self.logger.info("=" * 80)
        self.logger.info("DATA PIPELINE INITIALIZED")
        self.logger.info("=" * 80)
    
    def _setup_logging(self):
        """Configure logging for the pipeline"""
        log_path = Path(self.config['log_path'])
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Configure root logger
        logging.basicConfig(
            level=logging.INFO,
            handlers=[file_handler, console_handler]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Logging initialized. Log file: {log_path}")
    
    def run(self, fetch_news=True, api_key=None):
        """
        Execute the complete data pipeline
        
        Args:
            fetch_news (bool): Whether to fetch news data
            api_key (str): API key for news service (optional)
            
        Returns:
            dict: Pipeline execution summary
        """
        start_time = datetime.now()
        self.logger.info("\n" + "=" * 80)
        self.logger.info(f"PIPELINE EXECUTION STARTED: {start_time.strftime(self.config['date_format'])}")
        self.logger.info("=" * 80 + "\n")
        
        market_records = 0
        news_records = 0
        status = "FAILED"
        error_message = None
        
        try:
            # Step 1: Fetch Data
            self.logger.info("STEP 1: Fetching data from APIs...")
            self.logger.info("-" * 80)
            
            market_data = self.fetcher.fetch_market_data()
            if market_data is None:
                raise Exception("Failed to fetch market data")
            
            news_data = None
            if fetch_news:
                news_data = self.fetcher.fetch_news_data(api_key)
                if news_data is None:
                    self.logger.warning("Failed to fetch news data, continuing with market data only")
            
            self.logger.info("✓ Data fetch completed\n")
            
            # Step 2: Clean Data
            self.logger.info("STEP 2: Cleaning and transforming data...")
            self.logger.info("-" * 80)
            
            market_df = self.cleaner.clean_market_data(market_data)
            market_records = len(market_df)
            
            news_df = None
            if news_data:
                news_df = self.cleaner.clean_news_data(news_data)
                news_records = len(news_df)
            
            self.logger.info("✓ Data cleaning completed\n")
            
            # Step 3: Store Data
            self.logger.info("STEP 3: Storing data to database...")
            self.logger.info("-" * 80)
            
            self.storage.store_market_data(market_df)
            
            if news_df is not None:
                self.storage.store_news_data(news_df)
            
            self.logger.info("✓ Data storage completed\n")
            
            # Step 4: Generate Reports
            self.logger.info("STEP 4: Generating reports and summaries...")
            self.logger.info("-" * 80)
            
            market_summary = self.reporter.generate_market_summary(market_df)
            news_summary = self.reporter.generate_news_summary(news_df) if news_df is not None else {}
            
            # Create daily report
            report_path = self.reporter.create_daily_report(
                market_df, 
                news_df if news_df is not None else pd.DataFrame(),
                market_summary,
                news_summary
            )
            
            # Export to CSV
            csv_files = self.reporter.export_to_csv(
                market_df,
                news_df if news_df is not None else pd.DataFrame()
            )
            
            self.logger.info("✓ Report generation completed\n")
            
            # Pipeline completed successfully
            status = "SUCCESS"
            
            # Get database statistics
            db_stats = self.storage.get_database_stats()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Create execution summary
            summary = {
                'status': status,
                'start_time': start_time.strftime(self.config['date_format']),
                'end_time': end_time.strftime(self.config['date_format']),
                'duration_seconds': duration,
                'market_records_processed': market_records,
                'news_records_processed': news_records,
                'report_path': str(report_path) if report_path else None,
                'csv_exports': [str(f) for f in csv_files if f] if csv_files else [],
                'database_stats': db_stats
            }
            
            # Log pipeline run to database
            self.storage.log_pipeline_run(status, market_records, news_records, error_message)
            
            self.logger.info("=" * 80)
            self.logger.info("PIPELINE EXECUTION SUMMARY")
            self.logger.info("=" * 80)
            self.logger.info(f"Status: {status}")
            self.logger.info(f"Duration: {duration:.2f} seconds")
            self.logger.info(f"Market records: {market_records}")
            self.logger.info(f"News records: {news_records}")
            self.logger.info(f"Total database records: {db_stats.get('total_market_records', 0)} market, {db_stats.get('total_news_records', 0)} news")
            self.logger.info("=" * 80 + "\n")
            
            return summary
            
        except Exception as e:
            status = "FAILED"
            error_message = str(e)
            
            self.logger.error("=" * 80)
            self.logger.error(f"PIPELINE FAILED: {error_message}")
            self.logger.error("=" * 80)
            
            # Log failed run
            self.storage.log_pipeline_run(status, market_records, news_records, error_message)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            summary = {
                'status': status,
                'start_time': start_time.strftime(self.config['date_format']),
                'end_time': end_time.strftime(self.config['date_format']),
                'duration_seconds': duration,
                'error': error_message
            }
            
            return summary
    
    def get_pipeline_history(self, limit=5):
        """
        Get recent pipeline execution history
        
        Args:
            limit (int): Number of recent runs to retrieve
            
        Returns:
            pd.DataFrame: Pipeline run history
        """
        return self.storage.get_pipeline_history(limit)
    
    def get_latest_data(self, data_type='market', limit=10):
        """
        Query latest data from database
        
        Args:
            data_type (str): Type of data ('market' or 'news')
            limit (int): Number of records to retrieve
            
        Returns:
            pd.DataFrame: Latest data
        """
        if data_type == 'market':
            return self.storage.query_latest_market_data(limit)
        elif data_type == 'news':
            return self.storage.query_latest_news(limit)
        else:
            self.logger.error(f"Invalid data type: {data_type}")
            return None


def main():
    """Main entry point for pipeline execution"""
    print("\n" + "=" * 80)
    print("MARKET & NEWS DATA PIPELINE")
    print("=" * 80 + "\n")
    
    # Initialize pipeline
    pipeline = DataPipeline()
    
    # Run pipeline
    summary = pipeline.run(fetch_news=True)
    
    # Display summary
    print("\n" + "=" * 80)
    print("EXECUTION COMPLETE")
    print("=" * 80)
    print(f"Status: {summary['status']}")
    print(f"Duration: {summary.get('duration_seconds', 0):.2f} seconds")
    
    if summary['status'] == 'SUCCESS':
        print(f"Market records processed: {summary['market_records_processed']}")
        print(f"News records processed: {summary['news_records_processed']}")
        print(f"\nReport saved to: {summary['report_path']}")
        print(f"CSV exports: {len(summary.get('csv_exports', []))}")
    else:
        print(f"Error: {summary.get('error', 'Unknown error')}")
    
    print("=" * 80 + "\n")


if __name__ == "__main__":
    import pandas as pd  # Required for pipeline execution
    main()
