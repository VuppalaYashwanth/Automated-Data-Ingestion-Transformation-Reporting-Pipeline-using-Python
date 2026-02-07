"""
Data Fetching Module
Handles API calls and raw data storage
"""

import requests
import json
import logging
from datetime import datetime
from pathlib import Path


class DataFetcher:
    """Fetches data from external APIs and saves raw responses"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def fetch_api_data(self, url, output_filename, headers=None):
        """
        Fetch data from API and save to raw data folder
        
        Args:
            url (str): API endpoint URL
            output_filename (str): Name for the output file
            headers (dict): Optional HTTP headers
            
        Returns:
            dict: Response data or None if failed
        """
        try:
            self.logger.info(f"Fetching data from: {url}")
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Create output path with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(self.config['raw_data_path']) / f"{output_filename}_{timestamp}.json"
            
            # Save raw data
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            self.logger.info(f"Data saved to: {output_path}")
            self.logger.info(f"Records fetched: {len(data) if isinstance(data, list) else 1}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in fetch_api_data: {str(e)}")
            return None
    
    def fetch_market_data(self):
        """Fetch market data from configured endpoint"""
        self.logger.info("Starting market data fetch...")
        return self.fetch_api_data(
            self.config['market_api_url'],
            'market_data'
        )
    
    def fetch_news_data(self, api_key=None):
        """
        Fetch news data from configured endpoint
        
        Args:
            api_key (str): API key for news service (if required)
        """
        self.logger.info("Starting news data fetch...")
        headers = {'Authorization': f'Bearer {api_key}'} if api_key else None
        
        # For demo purposes, use a mock endpoint if no API key
        url = self.config['news_api_url']
        if api_key is None:
            self.logger.warning("No API key provided for news. Using mock data.")
            return self._get_mock_news_data()
        
        return self.fetch_api_data(url, 'news_data', headers=headers)
    
    def _get_mock_news_data(self):
        """Generate mock news data for demonstration"""
        mock_data = {
            "status": "ok",
            "totalResults": 3,
            "articles": [
                {
                    "source": {"id": "mock-source", "name": "Mock News"},
                    "author": "Demo Author",
                    "title": "Market Analysis: Tech Stocks Rally",
                    "description": "Technology stocks showed strong performance today",
                    "publishedAt": datetime.now().isoformat(),
                    "content": "Full article content here"
                },
                {
                    "source": {"id": "mock-source-2", "name": "Financial Times"},
                    "author": "Finance Reporter",
                    "title": "Economic Indicators Point to Growth",
                    "description": "Latest economic data suggests positive trends",
                    "publishedAt": datetime.now().isoformat(),
                    "content": "Economic analysis content"
                },
                {
                    "source": {"id": "mock-source-3", "name": "Business Daily"},
                    "author": "Market Analyst",
                    "title": "Cryptocurrency Markets Stabilize",
                    "description": "Digital currencies show reduced volatility",
                    "publishedAt": datetime.now().isoformat(),
                    "content": "Crypto market analysis"
                }
            ]
        }
        
        # Save mock data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(self.config['raw_data_path']) / f"news_data_{timestamp}.json"
        with open(output_path, 'w') as f:
            json.dump(mock_data, f, indent=2)
        
        self.logger.info(f"Mock news data saved to: {output_path}")
        return mock_data


if __name__ == "__main__":
    # Test module independently
    import json
    
    with open('../config.json', 'r') as f:
        config = json.load(f)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    fetcher = DataFetcher(config)
    market_data = fetcher.fetch_market_data()
    news_data = fetcher.fetch_news_data()
    
    print(f"Market data records: {len(market_data) if market_data else 0}")
    print(f"News data records: {len(news_data.get('articles', [])) if news_data else 0}")
