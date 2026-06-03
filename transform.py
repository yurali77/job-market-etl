# Transform raw job data into structured format

from datetime import datetime

# Skills we want to analyze
SKILLS = [
    # 编程语言
    "python", "java", "javascript", "typescript",
    "c++", "c#", "golang", "rust", "scala",
    
    # 数据库
    "sql", "mysql", "postgresql", "mongodb",
    "redis", "elasticsearch", "snowflake",
    
    # 云平台
    "aws", "azure", "gcp", "google cloud",
    
    # 工具
    "docker", "kubernetes", "git", "linux",
    "jenkins", "terraform", "ansible",
    
    # 框架
    "spring boot", "react", "node", "django",
    "flask", "fastapi", "spark", "kafka",
    
    # 概念
    "machine learning", "data engineer",
    "microservices", "rest api", "agile"
]

def extract_skills(description):
    """
    Extract skill keywords from job description
    """
    if not description:
        return ""
    
    description_lower = description.lower()
    found_skills = []
    
    for skill in SKILLS:
        if skill in description_lower:
            found_skills.append(skill)
    
    return ", ".join(found_skills)

def transform_job(job):
    """
    Transform a single job posting into a structured format
    """
    return {
        "job_id": job.get("id", ""),
        "title": job.get("title", ""),
        "company": job.get("company", {}).get("display_name", ""),
        "location": job.get("location", {}).get("display_name", ""),
        "salary_min": job.get("salary_min", 0),
        "salary_max": job.get("salary_max", 0),
        "description": job.get("description", "")[:500],  # 只取前500字
        "skills_required": extract_skills(job.get("description", "")),
        "job_url": job.get("redirect_url", ""),
        "date_posted": job.get("created", ""),
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def transform_all_jobs(raw_jobs):
    """
    Transform all job postings into a structured format
    """
    cleaned_jobs = []
    skipped = 0

    for job in raw_jobs:
        if not job.get("title") or not job.get("company"):
            skipped += 1
            continue
        
        cleaned_job = transform_job(job)
        cleaned_jobs.append(cleaned_job)

    print(f"✅ Transformation complete: {len(cleaned_jobs)} valid job postings")
    print(f"🗑️ Filtered out: {skipped} invalid job postings")
    return cleaned_jobs

# Test
if __name__ == "__main__":
    from extract import fetch_all_jobs
    raw_jobs = fetch_all_jobs()
    cleaned_jobs = transform_all_jobs(raw_jobs)
    
    # Print the first transformed job to see the result
    if cleaned_jobs:
        print("\n📋 First transformed job:")
        for key, value in cleaned_jobs[0].items():
            print(f"  {key}: {value}")