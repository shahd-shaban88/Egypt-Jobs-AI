import json
import os
import datetime
import uuid
import requests
from bs4 import BeautifulSoup

# مسار ملف البيانات
JOBS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'jobs.json')

def load_existing_jobs():
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_jobs(jobs):
    os.makedirs(os.path.dirname(JOBS_FILE), exist_ok=True)
    with open(JOBS_FILE, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

def fetch_real_linkedin_jobs():
    print("Fetching REAL jobs from LinkedIn...")
    
    # رابط البحث عن وظائف الذكاء الاصطناعي في مصر (الصفحة العامة المجانية)
    url = "https://www.linkedin.com/jobs/search?keywords=Artificial%20Intelligence&location=Egypt&f_TPR=r604800"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all('div', class_='base-card')
        
        parsed_jobs = []
        for card in job_cards:
            try:
                title_elem = card.find('h3', class_='base-search-card__title')
                title = title_elem.text.strip() if title_elem else "AI Engineer"
                
                company_elem = card.find('h4', class_='base-search-card__subtitle')
                company = company_elem.text.strip() if company_elem else "Unknown Company"
                
                location_elem = card.find('span', class_='job-search-card__location')
                location = location_elem.text.strip() if location_elem else "Egypt"
                
                link_elem = card.find('a', class_='base-card__full-link')
                link = link_elem['href'].split('?')[0] if link_elem else "https://www.linkedin.com"
                
                # تحديد نوع الوظيفة
                job_type = "Full-time"
                if "intern" in title.lower() or "تدريب" in title:
                    job_type = "Internship"
                elif "remote" in location.lower() or "عن بعد" in location:
                    location = "Remote (Egypt)"
                
                parsed_jobs.append({
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "company": company,
                    "location": location,
                    "type": job_type,
                    "category": "AI & Data",
                    "date_posted": datetime.date.today().isoformat(),
                    "link": link,
                    "description": f"Real opportunity recently posted by {company} for a {title} position in {location}. Click Apply to view full details on LinkedIn."
                })
            except Exception as e:
                continue
                
        print(f"Successfully scraped {len(parsed_jobs)} real jobs from LinkedIn.")
        return parsed_jobs
    
    except Exception as e:
        print(f"Failed to scrape LinkedIn: {e}")
        return []

def merge_jobs(existing, new_jobs):
    # منع التكرار بناءً على اسم الوظيفة والشركة
    existing_keys = {(j['title'].lower(), j['company'].lower()) for j in existing}
    added_count = 0
    
    for job in new_jobs:
        key = (job['title'].lower(), job['company'].lower())
        if key not in existing_keys:
            existing.insert(0, job) # إضافة الوظيفة الجديدة في بداية القائمة
            existing_keys.add(key)
            added_count += 1
            
    print(f"Added {added_count} brand new unique jobs to the platform.")
    return existing

if __name__ == '__main__':
    print("Starting Egypt Jobs AI Real Scraper...")
    existing = load_existing_jobs()
    real_jobs = fetch_real_linkedin_jobs()
    
    if real_jobs:
        merged = merge_jobs(existing, real_jobs)
        # الاحتفاظ بآخر 100 وظيفة فقط حتى لا يصبح الملف ضخماً جداً
        save_jobs(merged[:100])
        print("Done!")
    else:
        print("No new jobs found today.")
