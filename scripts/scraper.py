"""
Egypt Jobs AI - Automated Job Scraper
======================================
This script searches for AI/ML job opportunities in Egypt
and updates the data/jobs.json file automatically.

It uses a mock dataset by default, but can be extended to
use live LinkedIn data via RapidAPI's LinkedIn Job Search API.

Dependencies:
    pip install requests beautifulsoup4
"""

import json
import os
import datetime
import requests
import uuid

# --- CONFIGURATION ---
JOBS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'jobs.json')
AI_KEYWORDS = ['machine learning', 'deep learning', 'nlp', 'computer vision',
               'data science', 'artificial intelligence', 'ai engineer',
               'ml engineer', 'llm', 'generative ai', 'neural network']
LOCATION_KEYWORDS = ['egypt', 'cairo', 'alexandria', 'remote']

# Optional: Set your RapidAPI Key as a GitHub Secret named RAPIDAPI_KEY
RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY', None)


def load_existing_jobs():
    """Load existing jobs from the JSON file."""
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_jobs(jobs):
    """Save jobs list to the JSON file."""
    os.makedirs(os.path.dirname(JOBS_FILE), exist_ok=True)
    with open(JOBS_FILE, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"[✓] Saved {len(jobs)} jobs to {JOBS_FILE}")


def fetch_jobs_from_rapidapi():
    """
    Fetch AI/ML jobs from Egypt via RapidAPI LinkedIn Job Search API.
    Requires RAPIDAPI_KEY environment variable to be set.
    Docs: https://rapidapi.com/jaypat87/api/linkedin-jobs-search/
    """
    if not RAPIDAPI_KEY:
        print("[!] RAPIDAPI_KEY not set. Skipping live fetch.")
        return []

    url = "https://linkedin-jobs-search.p.rapidapi.com/"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "linkedin-jobs-search.p.rapidapi.com"
    }
    payload = {
        "search_terms": "Artificial Intelligence Engineer",
        "location": "Egypt",
        "page": "1"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        raw_jobs = response.json()
        parsed = []
        for j in raw_jobs:
            title = j.get('job_title', '')
            loc = j.get('job_location', '').lower()
            # Filter: must be in Egypt and AI-related
            if not any(k in loc for k in LOCATION_KEYWORDS):
                continue
            if not any(k in title.lower() for k in AI_KEYWORDS):
                continue
            parsed.append({
                "id": str(uuid.uuid4()),
                "title": title,
                "company": j.get('company_name', 'Unknown'),
                "location": j.get('job_location', 'Egypt'),
                "type": "Full-time",
                "category": "AI / ML",
                "date_posted": datetime.date.today().isoformat(),
                "link": j.get('linkedin_job_url_cleaned', '#'),
                "description": j.get('job_description', '')[:300] + '...'
            })
        print(f"[✓] Fetched {len(parsed)} live jobs from RapidAPI.")
        return parsed
    except Exception as e:
        print(f"[!] Error fetching from RapidAPI: {e}")
        return []


def merge_jobs(existing, new_jobs):
    """Merge new jobs with existing ones, avoiding duplicates by title+company."""
    existing_keys = {(j['title'].lower(), j['company'].lower()) for j in existing}
    added = 0
    for job in new_jobs:
        key = (job['title'].lower(), job['company'].lower())
        if key not in existing_keys:
            existing.append(job)
            existing_keys.add(key)
            added += 1
    print(f"[✓] Added {added} new unique jobs.")
    return existing


if __name__ == '__main__':
    print("=" * 50)
    print("   Egypt Jobs AI - Scraper Running")
    print(f"   Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    existing_jobs = load_existing_jobs()
    print(f"[i] Loaded {len(existing_jobs)} existing jobs.")

    new_jobs = fetch_jobs_from_rapidapi()

    merged = merge_jobs(existing_jobs, new_jobs)
    save_jobs(merged)

    print("=" * 50)
    print("[✓] Scraper finished successfully.")
