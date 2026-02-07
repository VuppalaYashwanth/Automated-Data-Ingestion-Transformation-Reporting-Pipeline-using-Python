# 🚀 QUICK START GUIDE

## Get Started in 3 Minutes

### Step 1: Setup (30 seconds)

```bash
cd market_news_pipeline

# Create virtual environment
python -m venv venv

# Activate it
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the Pipeline (30 seconds)

**Option A: Demo with Mock Data (No Internet Required)**
```bash
cd src
python demo.py
```

**Option B: Live Data (Requires Internet)**
```bash
cd src
python main.py
```

### Step 3: Check Results (1 minute)

The pipeline creates:
- ✅ **Database**: `database/market_data.db` (SQLite)
- ✅ **Reports**: `reports/daily_report_[timestamp].txt`
- ✅ **CSV Files**: `reports/*.csv`
- ✅ **Logs**: `logs/pipeline.log`

## 📊 What You Get

### Generated Files

```
market_news_pipeline/
├── reports/
│   ├── daily_report_[timestamp].txt      # Comprehensive text report
│   ├── market_data_[timestamp].csv       # Market data export
│   ├── news_data_[timestamp].csv         # News data export
│   └── daily_summary_[timestamp].csv     # Quick summary metrics
│
├── database/
│   └── market_data.db                    # SQLite database with all data
│
└── logs/
    └── pipeline.log                      # Execution logs
```

## 🎯 Interview Talking Points

### What This Project Demonstrates

1. **End-to-End Data Engineering**
   - Data ingestion from APIs
   - ETL (Extract, Transform, Load) pipeline
   - Automated reporting

2. **Production-Ready Code**
   - Error handling and logging
   - Modular design (separation of concerns)
   - Configuration management
   - Database persistence

3. **Python Best Practices**
   - Object-oriented programming
   - Type hints and docstrings
   - Virtual environments
   - Requirements management

4. **Data Skills**
   - API integration (requests)
   - Data cleaning (pandas)
   - Data validation
   - Database operations (SQLite)

### Sample Interview Responses

**Q: "Walk me through this project"**

A: "I built an automated data pipeline that fetches market and news data daily, cleans and validates it, stores it in a database, and generates comprehensive reports. The pipeline is modular with separate components for data fetching, cleaning, storage, and reporting. It includes robust error handling, logging, and can be scheduled to run automatically."

**Q: "How did you handle data quality?"**

A: "I implemented multiple validation layers:
- Null value handling and imputation
- Duplicate detection and removal
- Data type validation
- Price and market cap range validation
- Timestamp standardization
All cleaning operations are logged for audit trails."

**Q: "How would you scale this?"**

A: "Current improvements could include:
- Migrating from SQLite to PostgreSQL for production
- Implementing data partitioning by date
- Adding parallel processing for multiple data sources
- Containerizing with Docker for deployment
- Adding monitoring and alerting
- Implementing incremental loading instead of full refresh"

## 📝 Code Examples to Highlight

### 1. Modular Design
Show how each component (fetch, clean, store, report) is separate and testable:
```python
# From main.py
fetcher = DataFetcher(config)
cleaner = DataCleaner(config)
storage = DataStorage(config)
reporter = ReportGenerator(config)
```

### 2. Error Handling
```python
# From fetch_data.py
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    # ... process data
except requests.exceptions.RequestException as e:
    self.logger.error(f"API request failed: {str(e)}")
    return None
```

### 3. Data Cleaning
```python
# From clean_data.py
# Standardize column names
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Handle missing values
numeric_columns = df.select_dtypes(include=[np.number]).columns
df[numeric_columns] = df[numeric_columns].fillna(0)

# Remove duplicates
df = df.drop_duplicates()
```

## 🔄 Daily Automated Running

### Using Cron (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9 AM
0 9 * * * cd /path/to/market_news_pipeline/src && /path/to/venv/bin/python main.py
```

### Using Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 9:00 AM
4. Action: Start a program
5. Program: `C:\path\to\venv\Scripts\python.exe`
6. Arguments: `main.py`
7. Start in: `C:\path\to\market_news_pipeline\src`

## 📊 Sample Data Output

After running the pipeline, you'll have:

**Market Data (10 records)**
- Bitcoin, Ethereum, Binance Coin, etc.
- Current prices, market caps, 24h changes
- Timestamp and data source tracking

**News Data (5 articles)**
- Headlines from major sources
- Article metadata (author, source, timestamp)
- Full content and descriptions

**Database Tables**
- `market_data`: All historical market snapshots
- `news_data`: All collected news articles
- `pipeline_metadata`: Execution history and statistics

## 🛠️ Customization

### Change Data Sources

Edit `config.json`:
```json
{
  "market_api_url": "your-api-endpoint",
  "news_api_url": "your-news-api-endpoint"
}
```

### Add More Data Processing

Create new methods in `clean_data.py`:
```python
def custom_transformation(self, df):
    # Your custom logic here
    return df
```

## ❓ Troubleshooting

**Issue: "Module not found"**
- Solution: Make sure you activated the virtual environment

**Issue: "API request failed"**
- Solution: Check internet connection or use `demo.py` for offline testing

**Issue: "Permission denied"**
- Solution: Make sure you have write permissions in the project directory

## 📚 Next Steps

1. ✅ Run the demo successfully
2. ✅ Examine the generated reports
3. ✅ Review the database schema
4. ✅ Read through the code modules
5. ✅ Customize for your use case
6. ✅ Add to your portfolio/GitHub
7. ✅ Prepare to discuss in interviews

## 🎓 Learning Resources

To understand this project better:
- **Pandas**: Data manipulation and analysis
- **SQLite**: Lightweight database
- **Requests**: HTTP library for API calls
- **Python logging**: Application logging
- **ETL Concepts**: Extract, Transform, Load

---

**Congratulations!** You now have a professional-grade data pipeline project. 

*Questions? Check the main README.md for detailed documentation.*
