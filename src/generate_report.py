"""
Report Generation Module
Creates summary reports and analytics
"""

import pandas as pd
import logging
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """Generates reports and summaries from processed data"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.reports_path = Path(config['reports_path'])
        
        # Ensure reports directory exists
        self.reports_path.mkdir(parents=True, exist_ok=True)
    
    def generate_market_summary(self, df):
        """
        Generate market data summary statistics
        
        Args:
            df (pd.DataFrame): Market data
            
        Returns:
            dict: Summary statistics
        """
        try:
            summary = {
                'timestamp': datetime.now().strftime(self.config['date_format']),
                'total_records': len(df),
                'columns': list(df.columns)
            }
            
            # Calculate statistics for numeric columns
            if 'current_price' in df.columns:
                summary['price_stats'] = {
                    'average': float(df['current_price'].mean()),
                    'median': float(df['current_price'].median()),
                    'min': float(df['current_price'].min()),
                    'max': float(df['current_price'].max()),
                    'std': float(df['current_price'].std())
                }
            
            if 'market_cap' in df.columns:
                summary['market_cap_stats'] = {
                    'total': float(df['market_cap'].sum()),
                    'average': float(df['market_cap'].mean()),
                    'top_coin_cap': float(df['market_cap'].max())
                }
            
            if 'price_change_percentage_24h' in df.columns:
                summary['price_change_stats'] = {
                    'average_change': float(df['price_change_percentage_24h'].mean()),
                    'gainers': int((df['price_change_percentage_24h'] > 0).sum()),
                    'losers': int((df['price_change_percentage_24h'] < 0).sum())
                }
            
            # Top performers
            if 'name' in df.columns and 'current_price' in df.columns:
                top_5 = df.nlargest(5, 'current_price')[['name', 'current_price', 'market_cap']]
                summary['top_5_by_price'] = top_5.to_dict('records')
            
            self.logger.info("Market summary generated successfully")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating market summary: {str(e)}")
            return {}
    
    def generate_news_summary(self, df):
        """
        Generate news data summary
        
        Args:
            df (pd.DataFrame): News data
            
        Returns:
            dict: Summary statistics
        """
        try:
            summary = {
                'timestamp': datetime.now().strftime(self.config['date_format']),
                'total_articles': len(df),
                'columns': list(df.columns)
            }
            
            if 'source_name' in df.columns:
                source_counts = df['source_name'].value_counts().to_dict()
                summary['sources'] = {
                    'unique_sources': len(source_counts),
                    'source_distribution': source_counts
                }
            
            if 'author' in df.columns:
                summary['authors'] = {
                    'unique_authors': int(df['author'].nunique()),
                    'articles_with_author': int((df['author'] != '').sum())
                }
            
            # Recent headlines
            if 'title' in df.columns:
                summary['recent_headlines'] = df['title'].head(5).tolist()
            
            self.logger.info("News summary generated successfully")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating news summary: {str(e)}")
            return {}
    
    def create_daily_report(self, market_df, news_df, market_summary, news_summary):
        """
        Create comprehensive daily report
        
        Args:
            market_df (pd.DataFrame): Market data
            news_df (pd.DataFrame): News data
            market_summary (dict): Market statistics
            news_summary (dict): News statistics
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.reports_path / f"daily_report_{timestamp}.txt"
            
            with open(report_path, 'w') as f:
                f.write("=" * 80 + "\n")
                f.write("DAILY MARKET & NEWS DATA REPORT\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Report Generated: {datetime.now().strftime(self.config['date_format'])}\n\n")
                
                # Market Data Section
                f.write("-" * 80 + "\n")
                f.write("MARKET DATA SUMMARY\n")
                f.write("-" * 80 + "\n\n")
                
                f.write(f"Total Records: {market_summary.get('total_records', 0)}\n\n")
                
                if 'price_stats' in market_summary:
                    f.write("Price Statistics:\n")
                    for key, value in market_summary['price_stats'].items():
                        f.write(f"  {key.capitalize()}: ${value:,.2f}\n")
                    f.write("\n")
                
                if 'market_cap_stats' in market_summary:
                    f.write("Market Cap Statistics:\n")
                    for key, value in market_summary['market_cap_stats'].items():
                        f.write(f"  {key.replace('_', ' ').capitalize()}: ${value:,.2f}\n")
                    f.write("\n")
                
                if 'price_change_stats' in market_summary:
                    f.write("24h Price Change:\n")
                    f.write(f"  Average Change: {market_summary['price_change_stats']['average_change']:.2f}%\n")
                    f.write(f"  Gainers: {market_summary['price_change_stats']['gainers']}\n")
                    f.write(f"  Losers: {market_summary['price_change_stats']['losers']}\n\n")
                
                if 'top_5_by_price' in market_summary:
                    f.write("Top 5 Assets by Price:\n")
                    for i, asset in enumerate(market_summary['top_5_by_price'], 1):
                        f.write(f"  {i}. {asset.get('name', 'N/A')}: ${asset.get('current_price', 0):,.2f}\n")
                    f.write("\n")
                
                # News Data Section
                f.write("-" * 80 + "\n")
                f.write("NEWS DATA SUMMARY\n")
                f.write("-" * 80 + "\n\n")
                
                f.write(f"Total Articles: {news_summary.get('total_articles', 0)}\n\n")
                
                if 'sources' in news_summary:
                    f.write(f"Unique Sources: {news_summary['sources'].get('unique_sources', 0)}\n\n")
                
                if 'recent_headlines' in news_summary:
                    f.write("Recent Headlines:\n")
                    for i, headline in enumerate(news_summary['recent_headlines'], 1):
                        f.write(f"  {i}. {headline}\n")
                    f.write("\n")
                
                f.write("=" * 80 + "\n")
                f.write("END OF REPORT\n")
                f.write("=" * 80 + "\n")
            
            self.logger.info(f"Daily report saved to: {report_path}")
            return report_path
            
        except Exception as e:
            self.logger.error(f"Error creating daily report: {str(e)}")
            return None
    
    def export_to_csv(self, market_df, news_df):
        """
        Export data to CSV files
        
        Args:
            market_df (pd.DataFrame): Market data
            news_df (pd.DataFrame): News data
            
        Returns:
            tuple: Paths to exported files
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Export market data
            market_csv = self.reports_path / f"market_data_{timestamp}.csv"
            market_df.to_csv(market_csv, index=False)
            self.logger.info(f"Market data exported to: {market_csv}")
            
            # Export news data
            news_csv = self.reports_path / f"news_data_{timestamp}.csv"
            news_df.to_csv(news_csv, index=False)
            self.logger.info(f"News data exported to: {news_csv}")
            
            # Create summary CSV
            summary_csv = self.reports_path / f"daily_summary_{timestamp}.csv"
            
            summary_data = {
                'Metric': [
                    'Market Records',
                    'News Articles',
                    'Avg Current Price',
                    'Total Market Cap',
                    'Unique News Sources'
                ],
                'Value': [
                    len(market_df),
                    len(news_df),
                    f"${market_df['current_price'].mean():,.2f}" if 'current_price' in market_df.columns else 'N/A',
                    f"${market_df['market_cap'].sum():,.2f}" if 'market_cap' in market_df.columns else 'N/A',
                    news_df['source_name'].nunique() if 'source_name' in news_df.columns else 'N/A'
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_csv(summary_csv, index=False)
            self.logger.info(f"Summary exported to: {summary_csv}")
            
            return market_csv, news_csv, summary_csv
            
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {str(e)}")
            return None, None, None


if __name__ == "__main__":
    # Test module independently
    import json
    
    with open('../config.json', 'r') as f:
        config = json.load(f)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    generator = ReportGenerator(config)
    
    # Test with sample data
    sample_market = pd.DataFrame([
        {'name': 'Bitcoin', 'current_price': 50000, 'market_cap': 1000000000}
    ])
    
    sample_news = pd.DataFrame([
        {'title': 'Test Article', 'source_name': 'Test Source'}
    ])
    
    market_summary = generator.generate_market_summary(sample_market)
    news_summary = generator.generate_news_summary(sample_news)
    
    print(f"Market summary: {market_summary}")
    print(f"News summary: {news_summary}")
