# Extract job data from Adzuna API

import requests
import time
import config

def fetch_jobs(keyword, location="us", results_per_page=50):
    
    url = f"https://api.adzuna.com/v1/api/jobs/{location}/search/1"
    
    params = {
        "app_id": config.ADZUNA_APP_ID,
        "app_key": config.ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": keyword,
        "content-type": "application/json"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果请求失败会报错
        data = response.json()
        jobs = data.get("results", [])
        print(f"✅ Success to fetch data for '{keyword}': {len(jobs)} jobs")
        return jobs
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Fail to fetch data: {e}")
        return []

def fetch_all_jobs():
    """
    Fetch job data for all keywords defined in config.py
    Returns:
        list: A list of job postings
    """
    all_jobs = []
    
    for keyword in config.SEARCH_KEYWORDS:
        jobs = fetch_jobs(keyword)
        all_jobs.extend(jobs)
        time.sleep(1)  # Respect API rate limits
    
    print(f"\n📊 Total jobs fetched: {len(all_jobs)}")
    return all_jobs

if __name__ == "__main__":
    jobs = fetch_all_jobs()
