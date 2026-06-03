from extract import fetch_all_jobs
from transform import transform_all_jobs
from load import create_connection, create_table, load_jobs
from analyze import get_matched_jobs, display_results, analyze_skill_gaps


def run_etl():
    print("🚀 Start ETL Pipeline...")
    print("=" * 50)
    
    # 1. Extract
    print("\n📥 First Step: Fetching Data...")
    raw_jobs = fetch_all_jobs()
    
    # 2. Transform
    print("\n🔄 Second Step: Cleaning Data...")
    cleaned_jobs = transform_all_jobs(raw_jobs)
    
    # 3. Load
    print("\n💾 Third Step: Loading Data into Database...")
    conn = create_connection()
    create_table(conn)
    load_jobs(conn, cleaned_jobs)
    conn.close()

    # 4. Analyze
    print("\n🔍 Fourth Step: Analyzing Job Matches...")
    jobs = get_matched_jobs()
    display_results(jobs, top_n=10)
    analyze_skill_gaps(jobs)
    
    print("\n" + "=" * 50)
    print("✅ ETL Pipeline completed!")

if __name__ == "__main__":
    run_etl()