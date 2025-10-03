"""
Quick test script to add sample data and test the API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8081"

def test_api():
    """Test the API and add sample data"""
    
    # Test if API is running
    try:
        response = requests.get(f"{BASE_URL}/")
        print("✅ API is running:", response.json())
    except requests.exceptions.ConnectionError:
        print("❌ API is not running on port 8081")
        return
    
    # Create a sample user first
    user_data = {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john.doe@company.com",
        "role": "HR Manager"
    }
    
    try:
        user_response = requests.post(f"{BASE_URL}/users/", json=user_data)
        if user_response.status_code == 201:
            user = user_response.json()
            print("✅ Created user:", user["email"])
            user_id = user["user_id"]
        else:
            # User might already exist, get existing users
            users_response = requests.get(f"{BASE_URL}/users/")
            users = users_response.json()
            if users:
                user_id = users[0]["user_id"]
                print("✅ Using existing user:", users[0]["email"])
            else:
                print("❌ No users found")
                return
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return
    
    # Create sample jobs
    sample_jobs = [
        {
            "title": "Software Engineer",
            "description": "We are looking for a skilled software engineer to join our team. Experience with Python, React, and databases required.",
            "created_by_user_id": user_id
        },
        {
            "title": "Product Manager", 
            "description": "Seeking an experienced product manager to lead our product development initiatives. Strong analytical and communication skills required.",
            "created_by_user_id": user_id
        },
        {
            "title": "UX Designer",
            "description": "Join our design team as a UX Designer. Experience with Figma, user research, and prototyping essential.",
            "created_by_user_id": user_id
        },
        {
            "title": "Data Scientist",
            "description": "Looking for a data scientist with expertise in machine learning, Python, and statistical analysis.",
            "created_by_user_id": user_id
        }
    ]
    
    created_jobs = []
    for job_data in sample_jobs:
        try:
            job_response = requests.post(f"{BASE_URL}/jobs/", json=job_data)
            if job_response.status_code == 201:
                job = job_response.json()
                created_jobs.append(job)
                print(f"✅ Created job: {job['title']}")
            else:
                print(f"❌ Failed to create job: {job_data['title']} - {job_response.text}")
        except Exception as e:
            print(f"❌ Error creating job {job_data['title']}: {e}")
    
    # Test getting all jobs
    try:
        jobs_response = requests.get(f"{BASE_URL}/jobs/")
        if jobs_response.status_code == 200:
            jobs = jobs_response.json()
            print(f"✅ Retrieved {len(jobs)} jobs from API")
            for job in jobs:
                print(f"   - {job['title']}")
        else:
            print(f"❌ Failed to get jobs: {jobs_response.text}")
    except Exception as e:
        print(f"❌ Error getting jobs: {e}")

if __name__ == "__main__":
    test_api()