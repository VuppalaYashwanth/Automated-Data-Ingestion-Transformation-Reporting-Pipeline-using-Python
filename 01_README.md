# 📊 Automated Data Ingestion, Cleaning & Reporting Pipeline

A production-ready Python pipeline that automates daily market and news data collection, cleaning, storage, and reporting. This project demonstrates core data engineering skills including API integration, data transformation, database management, and automated reporting.

## 🎯 Project Overview

This pipeline performs end-to-end data engineering tasks:

1. **Data Ingestion**: Fetches market data from CoinGecko API and news data
2. **Data Cleaning**: Standardizes, validates, and transforms raw data
3. **Data Storage**: Persists cleaned data in SQLite database
4. **Report Generation**: Creates CSV exports and text-based summary reports
5. **Logging & Monitoring**: Comprehensive logging and pipeline execution tracking

## 🏗️ Architecture

```
┌─────────────────┐
│   API Sources   │
│  (Market/News)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Fetcher   │ ──► Raw JSON files
│  (fetch_data)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Cleaner   │ ──► Processed CSV files
│  (clean_data)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Database Store  │ ──► SQLite Database
│  (store_data)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Report Generator│ ──► Daily Reports & CSV
│(generate_report)│
└─────────────────┘
```

## 🛠️ Technologies Used

| Purpose | Technology |
|---------|-----------|
| Language | Python 3.8+ |
| Data Processing | Pandas, NumPy |
| API Integration | Requests |
| Database | SQLite3 |
| Logging | Python logging module |
| Configuration | JSON |

## 📁 Project Structure

```
market_news_pipeline/
│
├── data/
│   ├── raw/                    # Raw API responses (JSON)
│   └── processed/              # Cleaned data (CSV)
│
├── database/
│   └── market_data.db          # SQLite database
│
├── reports/
│   ├── daily_summary.csv       # Daily summary metrics
│   ├── daily_report.txt        # Detailed text report
│   ├── market_data_*.csv       # Market data exports
│   └── news_data_*.csv         # News data exports
│
├── logs/
│   └── pipeline.log            # Pipeline execution logs
│
├── src/
│   ├── fetch_data.py           # API data fetching module
│   ├── clean_data.py           # Data cleaning & transformation
│   ├── store_data.py           # Database operations
│   ├── generate_report.py      # Report generation
│   └── main.py                 # Pipeline orchestrator
│
├── config.json                 # Configuration settings
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for API calls)

### Installation

1. **Clone or download this project**

```bash
cd market_news_pipeline
```

2. **Create virtual environment (recommended)**

```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

### Running the Pipeline

**Basic execution:**

```bash
cd src
python main.py
```

**The pipeline will:**
- ✅ Fetch latest market data (cryptocurrency prices)
- ✅ Fetch news articles (business news)
- ✅ Clean and standardize all data
- ✅ Store data in SQLite database
- ✅ Generate daily reports and CSV exports
- ✅ Log all operations

## 📊 Sample Output

### Console Output
```
================================================================================
MARKET & NEWS DATA PIPELINE
================================================================================

2026-02-07 10:30:15 - __main__ - INFO - ====================================
2026-02-07 10:30:15 - __main__ - INFO - DATA PIPELINE INITIALIZED
2026-02-07 10:30:15 - __main__ - INFO - ====================================

2026-02-07 10:30:15 - __main__ - INFO - STEP 1: Fetching data from APIs...
2026-02-07 10:30:16 - fetch_data - INFO - Fetching data from: https://api.coingecko.com/...
2026-02-07 10:30:17 - fetch_data - INFO - Records fetched: 10
2026-02-07 10:30:17 - __main__ - INFO - ✓ Data fetch completed

2026-02-07 10:30:17 - __main__ - INFO - STEP 2: Cleaning and transforming data...
2026-02-07 10:30:17 - clean_data - INFO - Starting market data cleaning...
2026-02-07 10:30:17 - clean_data - INFO - Cleaned records: 10
2026-02-07 10:30:17 - __main__ - INFO - ✓ Data cleaning completed

2026-02-07 10:30:17 - __main__ - INFO - STEP 3: Storing data to database...
2026-02-07 10:30:17 - store_data - INFO - Storing 10 market records to database...
2026-02-07 10:30:17 - __main__ - INFO - ✓ Data storage completed

2026-02-07 10:30:17 - __main__ - INFO - STEP 4: Generating reports and summaries...
2026-02-07 10:30:17 - generate_report - INFO - Market summary generated successfully
2026-02-07 10:30:17 - __main__ - INFO - ✓ Report generation completed

================================================================================
Status: SUCCESS
Duration: 2.34 seconds
Market records processed: 10
News records processed: 3
================================================================================
```

### Daily Report (daily_report.txt)
```
================================================================================
DAILY MARKET & NEWS DATA REPORT
================================================================================

Report Generated: 2026-02-07 10:30:17

--------------------------------------------------------------------------------
MARKET DATA SUMMARY
--------------------------------------------------------------------------------

Total Records: 10

Price Statistics:
  Average: $42,567.89
  Median: $38,234.50
  Min: $1.23
  Max: $98,456.78
  Std: $25,678.90

Market Cap Statistics:
  Total: $1,234,567,890.00
  Average: $123,456,789.00

24h Price Change:
  Average Change: +2.35%
  Gainers: 7
  Losers: 3

Top 5 Assets by Price:
  1. Bitcoin: $98,456.78
  2. Ethereum: $45,678.90
  ...
```

### Database Schema

**market_data table:**
```sql
CREATE TABLE market_data (
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
```

**news_data table:**
```sql
CREATE TABLE news_data (
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
```

## ⚙️ Configuration

Edit `config.json` to customize:

```json
{
  "market_api_url": "https://api.coingecko.com/api/v3/...",
  "news_api_url": "https://newsapi.org/v2/...",
  "database_path": "database/market_data.db",
  "log_path": "logs/pipeline.log",
  "raw_data_path": "data/raw/",
  "processed_data_path": "data/processed/",
  "reports_path": "reports/"
}
```

## 🧪 Testing Individual Modules

Each module can be tested independently:

```bash
# Test data fetcher
python src/fetch_data.py

# Test data cleaner
python src/clean_data.py

# Test database storage
python src/store_data.py

# Test report generator
python src/generate_report.py
```

## 📈 Key Features

### 1. Robust Error Handling
- Try-catch blocks for all operations
- Graceful failure with detailed error logging
- Pipeline continues on non-critical errors

### 2. Comprehensive Logging
- Timestamped logs for all operations
- Both file and console logging
- Debug, info, warning, and error levels

### 3. Data Quality
- Null value handling
- Duplicate removal
- Data type validation
- Standardized column names

### 4. Modular Design
- Separation of concerns
- Easy to test and maintain
- Reusable components

### 5. Pipeline Monitoring
- Execution history tracking
- Performance metrics
- Database statistics

## 🔧 Advanced Usage

### Programmatic Usage

```python
from main import DataPipeline

# Initialize pipeline
pipeline = DataPipeline(config_path='config.json')

# Run pipeline
summary = pipeline.run(fetch_news=True)

# Get pipeline history
history = pipeline.get_pipeline_history(limit=10)
print(history)

# Query latest data
latest_market = pipeline.get_latest_data('market', limit=5)
print(latest_market)
```

### Schedule Automated Runs

**Using cron (Linux/Mac):**
```bash
# Run daily at 9 AM
0 9 * * * cd /path/to/project/src && python main.py
```

**Using Windows Task Scheduler:**
- Create a batch file `run_pipeline.bat`
- Schedule it in Task Scheduler

## 📝 Project Highlights for Resume/Portfolio

✅ **Python Automation** - Fully automated data pipeline  
✅ **API Integration** - RESTful API calls with error handling  
✅ **Data Processing** - Pandas transformations and cleaning  
✅ **Database Management** - SQLite with normalized schema  
✅ **Error Handling** - Comprehensive try-catch and logging  
✅ **Code Quality** - Clean, modular, documented code  
✅ **Production-Ready** - Configuration management, logging, monitoring

## 🤝 Skills Demonstrated

- Python programming (OOP, error handling, file I/O)
- Data engineering (ETL pipeline design)
- API integration and data ingestion
- Data cleaning and transformation with Pandas
- SQL and database management
- Logging and monitoring
- Configuration management
- Code organization and modularity

## 📌 Next Steps / Future Enhancements

- [ ] Add data visualization dashboard
- [ ] Implement email notifications
- [ ] Add data quality checks and alerts
- [ ] Cloud deployment (AWS/GCP)
- [ ] Containerization with Docker
- [ ] Add unit tests
- [ ] Implement incremental loading
- [ ] Add data versioning

## 📄 License

This project is open source and available for educational purposes.

## 👤 Author

Vuppala Yashwanth - [Yashwanthvuppala123@gmail.com]

---

**Note**: This pipeline uses free public APIs. For production use with NewsAPI, you'll need to register for an API key at https://newsapi.org/
