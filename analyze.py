# According to my resume, this script analyzes the job listings in the database and calculates how well they match my skills. It then displays the top matching jobs in a user-friendly format.

import mysql.connector
import config

# ⭐ Your skills
MY_SKILLS = [
    "python", "java", "sql", "mysql",
    "docker", "linux", "git", "javascript",
    "spring boot", "flask", "pandas", "c++", "power bi"
]

def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

def calculate_match_score(skills_required):
    """
    Calculate the match score between a job and your skills
    """
    if not skills_required:
        return 0
    
    job_skills = [s.strip().lower() for s in skills_required.split(",")]
    
    if len(job_skills) == 0:
        return 0
    
    matched = sum(1 for skill in job_skills if skill in MY_SKILLS)
    score = (matched / len(job_skills)) * 100
    return round(score, 1)

def get_matched_jobs():
    """
    Fetch all job listings from the database and calculate match scores
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Only fetch jobs that have skill requirements
    cursor.execute("""
        SELECT title, company, location, 
           salary_min, salary_max,
           skills_required, job_url
        FROM jobs
        WHERE skills_required IS NOT NULL 
        AND skills_required != ''
        AND LENGTH(skills_required) - LENGTH(REPLACE(skills_required, ',', '')) >= 2
""")
    
    jobs = cursor.fetchall()
    conn.close()
    
    # Calculate the match score for each job
    for job in jobs:
        job["match_score"] = calculate_match_score(job["skills_required"])
    
    # Sort by match score
    jobs.sort(key=lambda x: x["match_score"], reverse=True)
    
    return jobs

def display_results(jobs, top_n=10):
    """
    Display the top matching jobs in a user-friendly format
    """
    print("\n" + "=" * 60)
    print("🎯 Based on your skills, the top matching jobs are:")
    print("=" * 60)
    
    print(f"\n📚 Your skills: {', '.join(MY_SKILLS)}\n")
    
    # Only display jobs with a match score greater than 0
    matched_jobs = [j for j in jobs if j["match_score"] > 0]
    
    if not matched_jobs:
        print("❌ No matching jobs found. Please check your skills.")
        return
    
    for i, job in enumerate(matched_jobs[:top_n], 1):
        # Salary display
        if job["salary_min"] and job["salary_min"] > 0:
            salary = f"${int(job['salary_min']):,}"
            if job["salary_max"] and job["salary_max"] > job["salary_min"]:
                salary += f" - ${int(job['salary_max']):,}"
        else:
            salary = "Salary not disclosed"
        
        print(f"{'='*60}")
        print(f"#{i} Match Score: {job['match_score']}%")
        print(f"🏢 Company:   {job['company']}")
        print(f"💼 Title:   {job['title']}")
        print(f"📍 Location:   {job['location']}")
        print(f"💰 Salary:   {salary}")
        print(f"🔧 Skills:   {job['skills_required']}")
        print(f"🔗 URL:   {job['job_url']}")
    
    print(f"\n{'='*60}")
    print(f"📊 Total matching jobs found: {len(matched_jobs)}")
    print(f"✅ Displaying top {min(top_n, len(matched_jobs))} jobs")

def analyze_skill_gaps(jobs):
    """
    Analyze which skills you are missing
    """
    from collections import Counter
    
    all_required_skills = []
    for job in jobs:
        if job["skills_required"]:
            skills = [s.strip().lower() for s in job["skills_required"].split(",")]
            all_required_skills.extend(skills)
    
    skill_counts = Counter(all_required_skills)
    
    print("\n" + "=" * 60)
    print("📈 Market Skill Demand Analysis:")
    print("=" * 60)
    
    print("\n✅ Skills You Already Have:")
    have_count = 0
    for skill, count in skill_counts.most_common(30):
        if skill in MY_SKILLS:
            print(f"   ✅ {skill:<20} → {count} jobs need")
            have_count += 1
        if have_count >= 5:
            break
    
    print("\n❌ Skills You Are Missing (Recommended):")
    missing_count = 0
    for skill, count in skill_counts.most_common(30):
        if skill not in MY_SKILLS:
            suggestion = get_learning_suggestion(skill)
            print(f"   ❌ {skill:<20} → {count} jobsneed  |  {suggestion}")
            missing_count += 1
        if missing_count >= 8:
            break
    
    print(f"\n💡 Recommended: Focus on the top missing skills!")

def get_learning_suggestion(skill):
    """
    Provide learning suggestions for missing skills
    """
    suggestions = {
        "aws":              "Recommended: AWS Cloud Practitioner Certification (6 weeks)",
        "azure":            "Recommended: AZ-900 Certification (4 weeks)",
        "react":            "Recommended: YouTube React Tutorials (2 weeks)",
        "kubernetes":       "Recommended: Learn Docker (4 weeks)",
        "machine learning": "Recommended: Kaggle Free Courses (8 weeks)",
        "typescript":       "Recommended: JavaScript Fundamentals First (2 weeks)",
        "spark":            "Recommended: PySpark Introduction (4 weeks)",
        "kafka":            "Recommended: Official Documentation + Practice (3 weeks)",
        "tensorflow":       "Recommended: Google Free Courses (6 weeks)",
        "golang":           "Recommended: Tour of Go Official Tutorial (3 weeks)",
        "postgresql":       "Recommended: MySQL Knowledge is Transferable (1 week)",
        "redis":            "Recommended: Official Documentation + Practice (1 week)",
        "airflow":          "Recommended: ETL Project Fundamentals (3 weeks)",
    }
    return suggestions.get(skill, "Recommended: Search tutorials on Google + YouTube")
if __name__ == "__main__":
    print("🔍 Analyzing job matches...")
    jobs = get_matched_jobs()
    display_results(jobs, top_n=10)
    analyze_skill_gaps(jobs)
