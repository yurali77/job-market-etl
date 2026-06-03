# Job Market ETL Pipeline 🚀

A Python ETL pipeline that fetches real US job postings from the Adzuna API, stores them in MySQL, and analyzes skill demand to guide my job search strategy.

## Motivation

As a recent CS graduate job hunting in the US, I built this to answer: **"Which skills should I learn first?"** — using real market data instead of guessing.

## What It Does

- **Extract** — Fetches 400+ job postings from Adzuna API
- **Transform** — Cleans data and extracts required skills
- **Load** — Stores structured data into MySQL
- **Analyze** — Matches your skills to job demand and flags skill gaps

## Tech Stack

Python 3.12 | MySQL | Adzuna API | requests | mysql-connector-python

## Setup

```bash
# Clone and install
git clone https://github.com/yurali77/job-market-etl.git
cd job-market-etl
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your config.py (see config.py section below)
# Create MySQL database
# Run
python3 main.py
```

## config.py

```python
ADZUNA_APP_ID = "your_app_id"
ADZUNA_APP_KEY = "your_app_key"
SEARCH_KEYWORDS = ["software engineer", "python developer", ...]
SEARCH_LOCATION = "us"
RESULTS_PER_PAGE = 50
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "job_market"
DB_USER = "root"
DB_PASSWORD = "your_password"
```

## Key Findings

| Skill | Jobs | Have It? |
|---|---|---|
| SQL | 30 | ✅ |
| Python | 27 | ✅ |
| Java | 23 | ✅ |
| AWS | 22 | ❌ Learning next |
| React | 7 | ❌ In progress |

## Author

Yura Li — CS & Mathematics, Dordt University 2026
GitHub: [yurali77](https://github.com/yurali77)