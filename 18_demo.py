"""
Demo Pipeline Execution with Mock Data
Demonstrates the pipeline without requiring external API calls
"""

import logging
import json
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

# Import pipeline modules
from fetch_data import DataFetcher
from clean_data import DataCleaner
from store_data import DataStorage
from generate_report import ReportGenerator


def create_mock_market_data():
    """Generate realistic mock market data"""
    return [
        {
            'id': 'bitcoin',
            'symbol': 'btc',
            'name': 'Bitcoin',
            'current_price': 98456.78,
            'market_cap': 1923456789012,
            'total_volume': 45678901234,
            'price_change_24h': 2345.67,
            'price_change_percentage_24h': 2.44,
            'high_24h': 99123.45,
            'low_24h': 96234.56
        },
        {
            'id': 'ethereum',
            'symbol': 'eth',
            'name': 'Ethereum',
            'current_price': 3678.90,
            'market_cap': 456789012345,
            'total_volume': 23456789012,
            'price_change_24h': -45.67,
            'price_change_percentage_24h': -1.23,
            'high_24h': 3734.56,
            'low_24h': 3645.23
        },
        {
            'id': 'binancecoin',
            'symbol': 'bnb',
            'name': 'Binance Coin',
            'current_price': 612.34,
            'market_cap': 94567890123,
            'total_volume': 2345678901,
            'price_change_24h': 15.67,
            'price_change_percentage_24h': 2.63,
            'high_24h': 618.90,
            'low_24h': 598.45
        },
        {
            'id': 'cardano',
            'symbol': 'ada',
            'name': 'Cardano',
            'current_price': 1.23,
            'market_cap': 43456789012,
            'total_volume': 1234567890,
            'price_change_24h': 0.05,
            'price_change_percentage_24h': 4.23,
            'high_24h': 1.28,
            'low_24h': 1.18
        },
        {
            'id': 'solana',
            'symbol': 'sol',
            'name': 'Solana',
            'current_price': 234.56,
            'market_cap': 123456789012,
            'total_volume': 4567890123,
            'price_change_24h': 8.90,
            'price_change_percentage_24h': 3.94,
            'high_24h': 238.45,
            'low_24h': 228.67
        },
        {
            'id': 'ripple',
            'symbol': 'xrp',
            'name': 'XRP',
            'current_price': 0.87,
            'market_cap': 45678901234,
            'total_volume': 2345678901,
            'price_change_24h': -0.03,
            'price_change_percentage_24h': -3.33,
            'high_24h': 0.91,
            'low_24h': 0.85
        },
        {
            'id': 'polkadot',
            'symbol': 'dot',
            'name': 'Polkadot',
            'current_price': 12.34,
            'market_cap': 15678901234,
            'total_volume': 890123456,
            'price_change_24h': 0.56,
            'price_change_percentage_24h': 4.76,
            'high_24h': 12.67,
            'low_24h': 11.89
        },
        {
            'id': 'dogecoin',
            'symbol': 'doge',
            'name': 'Dogecoin',
            'current_price': 0.15,
            'market_cap': 21234567890,
            'total_volume': 1456789012,
            'price_change_24h': 0.01,
            'price_change_percentage_24h': 7.14,
            'high_24h': 0.16,
            'low_24h': 0.14
        },
        {
            'id': 'avalanche',
            'symbol': 'avax',
            'name': 'Avalanche',
            'current_price': 45.67,
            'market_cap': 17890123456,
            'total_volume': 789012345,
            'price_change_24h': -1.23,
            'price_change_percentage_24h': -2.62,
            'high_24h': 47.34,
            'low_24h': 44.56
        },
        {
            'id': 'chainlink',
            'symbol': 'link',
            'name': 'Chainlink',
            'current_price': 23.45,
            'market_cap': 13456789012,
            'total_volume': 678901234,
            'price_change_24h': 0.89,
            'price_change_percentage_24h': 3.94,
            'high_24h': 24.12,
            'low_24h': 22.67
        }
    ]


def create_mock_news_data():
    """Generate realistic mock news data"""
    return {
        'status': 'ok',
        'totalResults': 5,
        'articles': [
            {
                'source': {'id': 'bloomberg', 'name': 'Bloomberg'},
                'author': 'Sarah Chen',
                'title': 'Bitcoin Surges Past $98,000 as Institutional Adoption Accelerates',
                'description': 'Cryptocurrency markets show strong momentum with major institutional investments',
                'publishedAt': datetime.now().isoformat(),
                'content': 'Bitcoin reached new heights today as major financial institutions announced increased crypto allocations...'
            },
            {
                'source': {'id': 'reuters', 'name': 'Reuters'},
                'author': 'Michael Roberts',
                'title': 'Federal Reserve Maintains Interest Rates Amid Economic Uncertainty',
                'description': 'Central bank holds rates steady as economic indicators show mixed signals',
                'publishedAt': datetime.now().isoformat(),
                'content': 'The Federal Reserve announced today that it would maintain current interest rate levels...'
            },
            {
                'source': {'id': 'wsj', 'name': 'Wall Street Journal'},
                'author': 'Jennifer Martinez',
                'title': 'Tech Stocks Rally on Strong Earnings Reports',
                'description': 'Major technology companies exceed analyst expectations in Q4 earnings',
                'publishedAt': datetime.now().isoformat(),
                'content': 'Leading technology firms reported better-than-expected quarterly results...'
            },
            {
                'source': {'id': 'cnbc', 'name': 'CNBC'},
                'author': 'David Thompson',
                'title': 'Ethereum Upgrade Promises Faster Transactions and Lower Fees',
                'description': 'Network improvements aim to enhance scalability and user experience',
                'publishedAt': datetime.now().isoformat(),
                'content': 'The Ethereum network is set to implement major upgrades that will significantly improve performance...'
            },
            {
                'source': {'id': 'ft', 'name': 'Financial Times'},
                'author': 'Emma Wilson',
                'title': 'Global Markets Show Resilience Amid Geopolitical Tensions',
                'description': 'Investor sentiment remains cautiously optimistic despite ongoing challenges',
                'publishedAt': datetime.now().isoformat(),
                'content': 'International financial markets demonstrated unexpected strength today...'
            }
        ]
    }


def run_demo_pipeline():
    """Execute pipeline with mock data"""
    
    print("\n" + "=" * 80)
    print("MARKET & NEWS DATA PIPELINE - DEMO MODE")
    print("=" * 80 + "\n")
    
    # Load configuration
    with open('../config.json', 'r') as f:
        config = json.load(f)
    
    # Setup logging
    log_path = Path(config['log_path'])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    start_time = datetime.now()
    
    try:
        # Initialize components
        cleaner = DataCleaner(config)
        storage = DataStorage(config)
        reporter = ReportGenerator(config)
        
        logger.info("=" * 80)
        logger.info("DEMO PIPELINE STARTED")
        logger.info("=" * 80)
        
        # Step 1: Generate mock data
        logger.info("\nSTEP 1: Generating mock data...")
        logger.info("-" * 80)
        
        market_data = create_mock_market_data()
        news_data = create_mock_news_data()
        
        logger.info(f"✓ Generated {len(market_data)} market records")
        logger.info(f"✓ Generated {len(news_data['articles'])} news articles\n")
        
        # Step 2: Clean data
        logger.info("STEP 2: Cleaning and transforming data...")
        logger.info("-" * 80)
        
        market_df = cleaner.clean_market_data(market_data)
        news_df = cleaner.clean_news_data(news_data)
        
        logger.info(f"✓ Cleaned {len(market_df)} market records")
        logger.info(f"✓ Cleaned {len(news_df)} news records\n")
        
        # Step 3: Store data
        logger.info("STEP 3: Storing data to database...")
        logger.info("-" * 80)
        
        storage.store_market_data(market_df)
        storage.store_news_data(news_df)
        
        logger.info("✓ Data stored successfully\n")
        
        # Step 4: Generate reports
        logger.info("STEP 4: Generating reports and summaries...")
        logger.info("-" * 80)
        
        market_summary = reporter.generate_market_summary(market_df)
        news_summary = reporter.generate_news_summary(news_df)
        
        report_path = reporter.create_daily_report(
            market_df, news_df, market_summary, news_summary
        )
        
        csv_files = reporter.export_to_csv(market_df, news_df)
        
        logger.info("✓ Reports generated successfully\n")
        
        # Log pipeline run
        storage.log_pipeline_run('SUCCESS', len(market_df), len(news_df))
        
        # Get statistics
        db_stats = storage.get_database_stats()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Display summary
        print("\n" + "=" * 80)
        print("PIPELINE EXECUTION SUMMARY")
        print("=" * 80)
        print(f"Status: SUCCESS")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Market records processed: {len(market_df)}")
        print(f"News records processed: {len(news_df)}")
        print(f"\nDatabase Statistics:")
        print(f"  Total market records: {db_stats['total_market_records']}")
        print(f"  Total news records: {db_stats['total_news_records']}")
        print(f"  Total pipeline runs: {db_stats['total_pipeline_runs']}")
        print(f"\nReport saved to: {report_path}")
        print(f"CSV exports: {len([f for f in csv_files if f])}")
        print("=" * 80 + "\n")
        
        # Display sample data
        print("Sample Market Data:")
        print(market_df[['name', 'symbol', 'current_price', 'market_cap']].head())
        print("\nSample News Headlines:")
        print(news_df[['title', 'source_name']].head())
        
    except Exception as e:
        logger.error(f"Demo pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    run_demo_pipeline()
