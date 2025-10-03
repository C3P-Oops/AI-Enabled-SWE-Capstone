"""
Database seeding script for the Recruitment System.
This script creates sample users, jobs, candidates, and applications.
It first cleans up any existing data to avoid conflicts.
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8081"

def cleanup_existing_data():
    """Clean up existing data to avoid conflicts."""
    print("🧹 Cleaning up existing data...")
    
    # Get and delete existing applications first (due to foreign key constraints)
    try:
        response = requests.get(f"{BASE_URL}/applications/")
        if response.status_code == 200:
            applications = response.json()
            for app in applications:
                delete_response = requests.delete(f"{BASE_URL}/applications/{app['application_id']}")
                if delete_response.status_code == 200:
                    print(f"   Deleted application {app['application_id']}")
    except Exception as e:
        print(f"   Note: Could not clean applications: {e}")
    
    # Get and delete existing jobs
    try:
        response = requests.get(f"{BASE_URL}/jobs/")
        if response.status_code == 200:
            jobs = response.json()
            for job in jobs:
                delete_response = requests.delete(f"{BASE_URL}/jobs/{job['job_id']}")
                if delete_response.status_code == 200:
                    print(f"   Deleted job: {job['title']}")
    except Exception as e:
        print(f"   Note: Could not clean jobs: {e}")
    
    # Get and delete existing candidates
    try:
        response = requests.get(f"{BASE_URL}/candidates/")
        if response.status_code == 200:
            candidates = response.json()
            for candidate in candidates:
                delete_response = requests.delete(f"{BASE_URL}/candidates/{candidate['candidate_id']}")
                if delete_response.status_code == 200:
                    print(f"   Deleted candidate: {candidate['first_name']} {candidate['last_name']}")
    except Exception as e:
        print(f"   Note: Could not clean candidates: {e}")
    
    # Get and delete existing users
    try:
        response = requests.get(f"{BASE_URL}/users/")
        if response.status_code == 200:
            users = response.json()
            for user in users:
                delete_response = requests.delete(f"{BASE_URL}/users/{user['user_id']}")
                if delete_response.status_code == 200:
                    print(f"   Deleted user: {user['first_name']} {user['last_name']}")
    except Exception as e:
        print(f"   Note: Could not clean users: {e}")
    
    print("✅ Cleanup completed")

def create_users():
    """Create sample users."""
    users = [
        {
            "first_name": "Sarah",
            "last_name": "Johnson", 
            "email": "sarah.johnson@company.com",
            "role": "HR Manager"
        },
        {
            "first_name": "Mike",
            "last_name": "Chen",
            "email": "mike.chen@company.com", 
            "role": "Hiring Manager"
        },
        {
            "first_name": "Lisa",
            "last_name": "Rodriguez",
            "email": "lisa.rodriguez@company.com",
            "role": "Recruitment Coordinator"
        },
        {
            "first_name": "David",
            "last_name": "Smith",
            "email": "david.smith@company.com",
            "role": "Project Manager"
        }
    ]
    
    created_users = []
    for user in users:
        try:
            response = requests.post(f"{BASE_URL}/users/", json=user)
            if response.status_code == 201:  # Changed from 200 to 201
                created_user = response.json()
                created_users.append(created_user)
                print(f"✅ Created user: {user['first_name']} {user['last_name']}")
            else:
                print(f"❌ Failed to create user {user['first_name']}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error creating user {user['first_name']}: {e}")
    
    return created_users

def create_jobs(users):
    """Create sample job postings."""
    if len(users) < 2:
        print("❌ Need at least 2 users to create jobs")
        return []
    
    hr_manager = users[0]  # Sarah Johnson
    hiring_manager = users[1]  # Mike Chen
    
    jobs = [
        {
            "title": "Senior Software Engineer",
            "description": "We are looking for an experienced software engineer to join our team. You will be responsible for designing, developing, and maintaining high-quality software applications. The ideal candidate should have strong programming skills in Python, JavaScript, and experience with modern frameworks.",
            "department": "Engineering",
            "location": "San Francisco, CA",
            "created_by_user_id": hr_manager["user_id"],
            "hiring_manager_id": hiring_manager["user_id"]
        },
        {
            "title": "Product Manager",
            "description": "Join our product team to drive the development of innovative solutions. You will work closely with engineering, design, and marketing teams to define product requirements, prioritize features, and ensure successful product launches.",
            "department": "Product",
            "location": "New York, NY", 
            "created_by_user_id": hr_manager["user_id"],
            "hiring_manager_id": hiring_manager["user_id"]
        },
        {
            "title": "UX Designer",
            "description": "We're seeking a creative UX Designer to craft exceptional user experiences. You will conduct user research, create wireframes and prototypes, and collaborate with cross-functional teams to deliver intuitive and engaging designs.",
            "department": "Design",
            "location": "Remote",
            "created_by_user_id": hr_manager["user_id"],
            "hiring_manager_id": hiring_manager["user_id"]
        },
        {
            "title": "Data Scientist",
            "description": "Looking for a data scientist to analyze complex datasets and generate actionable insights. You should have experience with machine learning, statistical analysis, and data visualization tools like Python, R, and Tableau.",
            "department": "Data & Analytics",
            "location": "Austin, TX",
            "created_by_user_id": hr_manager["user_id"],
            "hiring_manager_id": hiring_manager["user_id"]
        },
        {
            "title": "Marketing Specialist",
            "description": "Join our marketing team to develop and execute comprehensive marketing campaigns. You will manage social media presence, create content, analyze campaign performance, and support lead generation efforts.",
            "department": "Marketing",
            "location": "Los Angeles, CA",
            "status": "draft",
            "created_by_user_id": hr_manager["user_id"],
            "hiring_manager_id": hiring_manager["user_id"]
        }
    ]
    
    created_jobs = []
    for job in jobs:
        try:
            response = requests.post(f"{BASE_URL}/jobs/", json=job)
            if response.status_code == 201:  # Changed from 200 to 201
                created_job = response.json()
                created_jobs.append(created_job)
                print(f"✅ Created job: {job['title']}")
            else:
                print(f"❌ Failed to create job {job['title']}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error creating job {job['title']}: {e}")
    
    return created_jobs

def create_candidates():
    """Create sample candidates."""
    candidates = [
        {
            "first_name": "Alex",
            "last_name": "Thompson",
            "email": "alex.thompson@email.com",
            "phone": "+1-555-0101"
        },
        {
            "first_name": "Emma",
            "last_name": "Davis",
            "email": "emma.davis@email.com", 
            "phone": "+1-555-0102"
        },
        {
            "first_name": "James",
            "last_name": "Wilson",
            "email": "james.wilson@email.com",
            "phone": "+1-555-0103"
        },
        {
            "first_name": "Sofia",
            "last_name": "Garcia",
            "email": "sofia.garcia@email.com",
            "phone": "+1-555-0104"
        },
        {
            "first_name": "Ryan",
            "last_name": "Lee",
            "email": "ryan.lee@email.com",
            "phone": "+1-555-0105"
        }
    ]
    
    created_candidates = []
    for candidate in candidates:
        try:
            response = requests.post(f"{BASE_URL}/candidates/", json=candidate)
            if response.status_code == 201:  # Changed from 200 to 201
                created_candidate = response.json()
                created_candidates.append(created_candidate)
                print(f"✅ Created candidate: {candidate['first_name']} {candidate['last_name']}")
            else:
                print(f"❌ Failed to create candidate {candidate['first_name']}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error creating candidate {candidate['first_name']}: {e}")
    
    return created_candidates

def create_applications(jobs, candidates):
    """Create sample applications."""
    if len(jobs) < 3 or len(candidates) < 3:
        print("❌ Need at least 3 jobs and 3 candidates to create applications")
        return []
    
    applications = [
        {
            "job_id": jobs[0]["job_id"],  # Senior Software Engineer
            "candidate_id": candidates[0]["candidate_id"],  # Alex Thompson
            "status": "applied"
        },
        {
            "job_id": jobs[0]["job_id"],  # Senior Software Engineer  
            "candidate_id": candidates[1]["candidate_id"],  # Emma Davis
            "status": "screening"
        },
        {
            "job_id": jobs[1]["job_id"],  # Product Manager
            "candidate_id": candidates[2]["candidate_id"],  # James Wilson
            "status": "interviewing"
        },
        {
            "job_id": jobs[2]["job_id"],  # UX Designer
            "candidate_id": candidates[3]["candidate_id"],  # Sofia Garcia
            "status": "applied"
        },
        {
            "job_id": jobs[3]["job_id"],  # Data Scientist
            "candidate_id": candidates[4]["candidate_id"],  # Ryan Lee
            "status": "applied"
        }
    ]
    
    created_applications = []
    for application in applications:
        try:
            response = requests.post(f"{BASE_URL}/applications/", json=application)
            if response.status_code == 201:  # Changed from 200 to 201
                created_application = response.json()
                created_applications.append(created_application)
                print(f"✅ Created application: Job {application['job_id']} - Candidate {application['candidate_id']}")
            else:
                print(f"❌ Failed to create application: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error creating application: {e}")
    
    return created_applications

def main():
    """Main seeding function."""
    print("🌱 Starting database seeding...")
    print("=" * 50)
    
    # Check if API is running
    try:
        response = requests.get(f"{BASE_URL}/")
        print("✅ API is running")
    except Exception as e:
        print(f"❌ API is not running on {BASE_URL}. Please start the server first.")
        return
    
    # Clean up existing data first
    cleanup_existing_data()
    
    # Create data in order (respecting foreign key dependencies)
    print("\n📝 Creating users...")
    users = create_users()
    
    print("\n💼 Creating jobs...")
    jobs = create_jobs(users)
    
    print("\n👥 Creating candidates...")
    candidates = create_candidates()
    
    print("\n📋 Creating applications...")
    applications = create_applications(jobs, candidates)
    
    print("\n" + "=" * 50)
    print("🎉 Database seeding completed!")
    print(f"   Created: {len(users)} users, {len(jobs)} jobs, {len(candidates)} candidates, {len(applications)} applications")
    
    # Test the jobs endpoint
    print("\n🧪 Testing /jobs/ endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/jobs/")
        if response.status_code == 200:
            jobs_data = response.json()
            print(f"✅ Successfully retrieved {len(jobs_data)} jobs from API")
            for job in jobs_data:
                print(f"   - {job['title']} ({job.get('department', 'No dept')} - {job.get('location', 'No location')})")
        else:
            print(f"❌ Failed to retrieve jobs: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing jobs endpoint: {e}")

if __name__ == "__main__":
    main()