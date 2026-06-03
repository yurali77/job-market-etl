# load.py
# Load cleaned job data into MySQL database

import mysql.connector
import config

def create_connection():
    """
    Connect to MySQL database
    """
    conn = mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )
    print("✅ Database connection successful!")
    return conn

def create_table(conn):
    """
    Create job data table (if not exists)
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            job_id VARCHAR(50) UNIQUE,
            title VARCHAR(200),
            company VARCHAR(200),
            location VARCHAR(200),
            salary_min FLOAT,
            salary_max FLOAT,
            description TEXT,
            skills_required VARCHAR(500),
            job_url VARCHAR(500),
            date_posted VARCHAR(50),
            fetched_at VARCHAR(50)
        )
    """)
    conn.commit()
    print("✅ Data table created successfully!")

def load_jobs(conn, jobs):
    """
    Insert cleaned job data into MySQL
    """
    cursor = conn.cursor()
    inserted = 0
    skipped = 0

    for job in jobs:
        try:
            cursor.execute("""
                INSERT IGNORE INTO jobs 
                (job_id, title, company, location, salary_min, 
                salary_max, description, skills_required, 
                job_url, date_posted, fetched_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                job["job_id"],
                job["title"],
                job["company"],
                job["location"],
                job["salary_min"],
                job["salary_max"],
                job["description"],
                job["skills_required"],
                job["job_url"],
                job["date_posted"],
                job["fetched_at"]
            ))
            inserted += 1

        except Exception as e:
            print(f"❌ Failed to insert: {e}")
            skipped += 1

    conn.commit()
    print(f"✅ Successfully inserted: {inserted} records")
    print(f"⏭️ Skipped duplicates: {skipped} records")

# 测试
if __name__ == "__main__":
    from extract import fetch_all_jobs
    from transform import transform_all_jobs

    raw_jobs = fetch_all_jobs()
    cleaned_jobs = transform_all_jobs(raw_jobs)
    
    conn = create_connection()
    create_table(conn)
    load_jobs(conn, cleaned_jobs)
    conn.close()
    print("\n🎉 ETL completed! Data has been loaded into MySQL!")