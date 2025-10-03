#!/usr/bin/env python3
"""
Script to populate the recruitment database with test data.
Run this script to add sample jobs, candidates, and applications to test the frontend.
"""

import requests
import json

# API base URL
API_BASE_URL = "http://localhost:8081"

def create_test_data():
    """Create test users, jobs, candidates, and applications."""
    
    # Test users (HR staff)
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
            "first_name": "James",
            "last_name": "Wilson",
            "email": "james.wilson@company.com",
            "role": "Hiring Manager"
        },
        {
            "first_name": "Emma",
            "last_name": "Thompson",
            "email": "emma.thompson@company.com",
            "role": "Project Manager"
        }
    ]
    
    # Test jobs with diverse roles and locations
    jobs = [
        {
            "title": "Senior Software Engineer",
            "description": "Develop and maintain web applications using React and Python. Location: New York, NY. Full-time position with excellent benefits.",
            "created_by_user_id": 1
        },
        {
            "title": "Product Manager", 
            "description": "Lead product strategy and roadmap for our core platform. Location: San Francisco, CA. Drive cross-functional collaboration.",
            "created_by_user_id": 1
        },
        {
            "title": "UX Designer",
            "description": "Design user-centered experiences for our mobile and web applications. Location: Austin, TX. Focus on user research and prototyping.", 
            "created_by_user_id": 2
        },
        {
            "title": "Data Scientist",
            "description": "Build ML models and analyze user behavior data. Location: Seattle, WA. Experience with Python, SQL, and machine learning required.",
            "created_by_user_id": 2
        },
        {
            "title": "Marketing Coordinator",
            "description": "Coordinate marketing campaigns and manage social media presence. Location: Chicago, IL. Creative and analytical mindset needed.",
            "created_by_user_id": 1
        },
        {
            "title": "DevOps Engineer",
            "description": "Manage CI/CD pipelines and cloud infrastructure. Location: Remote. AWS and Kubernetes experience preferred.",
            "created_by_user_id": 3
        },
        {
            "title": "Frontend Developer",
            "description": "Build responsive React applications with modern JavaScript. Location: Denver, CO. Strong CSS and TypeScript skills required.",
            "created_by_user_id": 2
        },
        {
            "title": "Sales Representative",
            "description": "Drive revenue growth through new client acquisition. Location: Miami, FL. B2B sales experience preferred.",
            "created_by_user_id": 4
        },
        {
            "title": "QA Engineer",
            "description": "Develop automated test suites and ensure product quality. Location: Portland, OR. Selenium and API testing experience.",
            "created_by_user_id": 3
        },
        {
            "title": "Business Analyst",
            "description": "Analyze business requirements and translate them into technical specifications. Location: Boston, MA. SQL and reporting skills needed.",
            "created_by_user_id": 4
        },
        {
            "title": "Mobile Developer",
            "description": "Develop native iOS and Android applications. Location: Los Angeles, CA. Swift and Kotlin experience required.",
            "created_by_user_id": 2
        },
        {
            "title": "Cybersecurity Specialist",
            "description": "Implement security protocols and monitor for threats. Location: Washington, DC. Security certifications preferred.",
            "created_by_user_id": 5
        },
        {
            "title": "HR Generalist",
            "description": "Support employee lifecycle and HR operations. Location: Phoenix, AZ. SHRM certification a plus.",
            "created_by_user_id": 1
        },
        {
            "title": "Technical Writer",
            "description": "Create documentation for APIs and technical products. Location: Remote. Strong writing and technical skills required.",
            "created_by_user_id": 3
        },
        {
            "title": "Cloud Architect",
            "description": "Design scalable cloud solutions and architecture. Location: Dallas, TX. AWS/Azure certifications required.",
            "created_by_user_id": 5
        }
    ]
    
    # Test candidates with diverse backgrounds
    candidates = [
        {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@email.com",
            "phone": "555-0101"
        },
        {
            "first_name": "Bob", 
            "last_name": "Wilson",
            "email": "bob.wilson@email.com",
            "phone": "555-0102"
        },
        {
            "first_name": "Carol",
            "last_name": "Davis",
            "email": "carol.davis@email.com", 
            "phone": "555-0103"
        },
        {
            "first_name": "David",
            "last_name": "Brown",
            "email": "david.brown@email.com",
            "phone": "555-0104"
        },
        {
            "first_name": "Eva",
            "last_name": "Garcia",
            "email": "eva.garcia@email.com",
            "phone": "555-0105"
        },
        {
            "first_name": "Frank",
            "last_name": "Miller",
            "email": "frank.miller@email.com",
            "phone": "555-0106"
        },
        {
            "first_name": "Grace",
            "last_name": "Lee",
            "email": "grace.lee@email.com",
            "phone": "555-0107"
        },
        {
            "first_name": "Henry",
            "last_name": "Taylor",
            "email": "henry.taylor@email.com",
            "phone": "555-0108"
        },
        {
            "first_name": "Ivy",
            "last_name": "Anderson",
            "email": "ivy.anderson@email.com",
            "phone": "555-0109"
        },
        {
            "first_name": "Jack",
            "last_name": "Thompson",
            "email": "jack.thompson@email.com",
            "phone": "555-0110"
        },
        {
            "first_name": "Kate",
            "last_name": "White",
            "email": "kate.white@email.com",
            "phone": "555-0111"
        },
        {
            "first_name": "Leo",
            "last_name": "Martinez",
            "email": "leo.martinez@email.com",
            "phone": "555-0112"
        },
        {
            "first_name": "Maya",
            "last_name": "Singh",
            "email": "maya.singh@email.com",
            "phone": "555-0113"
        },
        {
            "first_name": "Nathan",
            "last_name": "Johnson",
            "email": "nathan.johnson@email.com",
            "phone": "555-0114"
        },
        {
            "first_name": "Olivia",
            "last_name": "Chen",
            "email": "olivia.chen@email.com",
            "phone": "555-0115"
        },
        {
            "first_name": "Paul",
            "last_name": "Rodriguez",
            "email": "paul.rodriguez@email.com",
            "phone": "555-0116"
        },
        {
            "first_name": "Quinn",
            "last_name": "Davis",
            "email": "quinn.davis@email.com",
            "phone": "555-0117"
        },
        {
            "first_name": "Ruby",
            "last_name": "Wilson",
            "email": "ruby.wilson@email.com",
            "phone": "555-0118"
        },
        {
            "first_name": "Sam",
            "last_name": "Kumar",
            "email": "sam.kumar@email.com",
            "phone": "555-0119"
        },
        {
            "first_name": "Tara",
            "last_name": "O'Connor",
            "email": "tara.oconnor@email.com",
            "phone": "555-0120"
        }
    ]
    
    created_users = []
    created_jobs = []
    created_candidates = []
    
    try:
        # Create users
        print("Creating users...")
        for user in users:
            response = requests.post(f"{API_BASE_URL}/users/", json=user)
            if response.status_code == 201:
                created_user = response.json()
                created_users.append(created_user)
                print(f"✓ Created user: {user['first_name']} {user['last_name']}")
            else:
                print(f"✗ Failed to create user {user['first_name']} {user['last_name']}: {response.text}")
        
        # Create jobs
        print("\nCreating jobs...")
        for job in jobs:
            response = requests.post(f"{API_BASE_URL}/jobs/", json=job)
            if response.status_code == 201:
                created_job = response.json()
                created_jobs.append(created_job) 
                print(f"✓ Created job: {job['title']}")
            else:
                print(f"✗ Failed to create job {job['title']}: {response.text}")
        
        # Create candidates
        print("\nCreating candidates...")
        for candidate in candidates:
            response = requests.post(f"{API_BASE_URL}/candidates/", json=candidate)
            if response.status_code == 201:
                created_candidate = response.json()
                created_candidates.append(created_candidate)
                print(f"✓ Created candidate: {candidate['first_name']} {candidate['last_name']}")
            else:
                print(f"✗ Failed to create candidate {candidate['first_name']} {candidate['last_name']}: {response.text}")
        
        # Create applications (candidates applying to jobs with diverse statuses)
        print("\nCreating applications...")
        applications = [
            # Senior Software Engineer (Job 1) - 8 applications
            {"job_id": 1, "candidate_id": 1, "status": "applied"},
            {"job_id": 1, "candidate_id": 2, "status": "screening"}, 
            {"job_id": 1, "candidate_id": 3, "status": "interviewing"},
            {"job_id": 1, "candidate_id": 4, "status": "offer_extended"},
            {"job_id": 1, "candidate_id": 5, "status": "hired"},
            {"job_id": 1, "candidate_id": 6, "status": "rejected"},
            {"job_id": 1, "candidate_id": 7, "status": "withdrawn"},
            {"job_id": 1, "candidate_id": 8, "status": "applied"},
            
            # Product Manager (Job 2) - 6 applications
            {"job_id": 2, "candidate_id": 9, "status": "applied"},
            {"job_id": 2, "candidate_id": 10, "status": "screening"},
            {"job_id": 2, "candidate_id": 11, "status": "interviewing"},
            {"job_id": 2, "candidate_id": 12, "status": "offer_extended"},
            {"job_id": 2, "candidate_id": 13, "status": "rejected"},
            {"job_id": 2, "candidate_id": 14, "status": "hired"},
            
            # UX Designer (Job 3) - 5 applications
            {"job_id": 3, "candidate_id": 15, "status": "applied"},
            {"job_id": 3, "candidate_id": 16, "status": "screening"},
            {"job_id": 3, "candidate_id": 17, "status": "interviewing"},
            {"job_id": 3, "candidate_id": 18, "status": "rejected"},
            {"job_id": 3, "candidate_id": 19, "status": "applied"},
            
            # Data Scientist (Job 4) - 4 applications
            {"job_id": 4, "candidate_id": 20, "status": "applied"},
            {"job_id": 4, "candidate_id": 1, "status": "screening"},
            {"job_id": 4, "candidate_id": 3, "status": "interviewing"},
            {"job_id": 4, "candidate_id": 5, "status": "rejected"},
            
            # Marketing Coordinator (Job 5) - 3 applications
            {"job_id": 5, "candidate_id": 7, "status": "applied"},
            {"job_id": 5, "candidate_id": 9, "status": "screening"},
            {"job_id": 5, "candidate_id": 11, "status": "hired"},
            
            # DevOps Engineer (Job 6) - 7 applications
            {"job_id": 6, "candidate_id": 2, "status": "applied"},
            {"job_id": 6, "candidate_id": 4, "status": "applied"},
            {"job_id": 6, "candidate_id": 6, "status": "screening"},
            {"job_id": 6, "candidate_id": 8, "status": "interviewing"},
            {"job_id": 6, "candidate_id": 10, "status": "interviewing"},
            {"job_id": 6, "candidate_id": 12, "status": "offer_extended"},
            {"job_id": 6, "candidate_id": 14, "status": "rejected"},
            
            # Frontend Developer (Job 7) - 6 applications
            {"job_id": 7, "candidate_id": 13, "status": "applied"},
            {"job_id": 7, "candidate_id": 15, "status": "screening"},
            {"job_id": 7, "candidate_id": 17, "status": "interviewing"},
            {"job_id": 7, "candidate_id": 19, "status": "rejected"},
            {"job_id": 7, "candidate_id": 1, "status": "withdrawn"},
            {"job_id": 7, "candidate_id": 3, "status": "applied"},
            
            # Sales Representative (Job 8) - 4 applications
            {"job_id": 8, "candidate_id": 16, "status": "applied"},
            {"job_id": 8, "candidate_id": 18, "status": "screening"},
            {"job_id": 8, "candidate_id": 20, "status": "interviewing"},
            {"job_id": 8, "candidate_id": 2, "status": "hired"},
            
            # QA Engineer (Job 9) - 5 applications
            {"job_id": 9, "candidate_id": 4, "status": "applied"},
            {"job_id": 9, "candidate_id": 6, "status": "applied"},
            {"job_id": 9, "candidate_id": 8, "status": "screening"},
            {"job_id": 9, "candidate_id": 10, "status": "interviewing"},
            {"job_id": 9, "candidate_id": 12, "status": "rejected"},
            
            # Business Analyst (Job 10) - 3 applications
            {"job_id": 10, "candidate_id": 14, "status": "applied"},
            {"job_id": 10, "candidate_id": 16, "status": "screening"},
            {"job_id": 10, "candidate_id": 18, "status": "offer_extended"},
            
            # Mobile Developer (Job 11) - 6 applications
            {"job_id": 11, "candidate_id": 5, "status": "applied"},
            {"job_id": 11, "candidate_id": 7, "status": "screening"},
            {"job_id": 11, "candidate_id": 9, "status": "interviewing"},
            {"job_id": 11, "candidate_id": 11, "status": "interviewing"},
            {"job_id": 11, "candidate_id": 13, "status": "rejected"},
            {"job_id": 11, "candidate_id": 15, "status": "hired"},
            
            # Cybersecurity Specialist (Job 12) - 2 applications
            {"job_id": 12, "candidate_id": 17, "status": "applied"},
            {"job_id": 12, "candidate_id": 19, "status": "screening"},
            
            # HR Generalist (Job 13) - 4 applications
            {"job_id": 13, "candidate_id": 1, "status": "applied"},
            {"job_id": 13, "candidate_id": 20, "status": "screening"},
            {"job_id": 13, "candidate_id": 2, "status": "interviewing"},
            {"job_id": 13, "candidate_id": 4, "status": "rejected"},
            
            # Technical Writer (Job 14) - 3 applications
            {"job_id": 14, "candidate_id": 6, "status": "applied"},
            {"job_id": 14, "candidate_id": 8, "status": "applied"},
            {"job_id": 14, "candidate_id": 10, "status": "hired"},
            
            # Cloud Architect (Job 15) - 1 application (new posting)
            {"job_id": 15, "candidate_id": 12, "status": "applied"},
        ]
        
        for app in applications:
            response = requests.post(f"{API_BASE_URL}/applications/", json=app)
            if response.status_code == 201:
                print(f"✓ Created application: Candidate {app['candidate_id']} -> Job {app['job_id']}")
            else:
                print(f"✗ Failed to create application: {response.text}")
        
        print(f"\n🎉 Test data creation complete!")
        print(f"Created {len(created_users)} users, {len(created_jobs)} jobs, {len(created_candidates)} candidates")
        print("Your Dashboard should now show real data from the database!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the FastAPI server is running on http://localhost:8081")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    create_test_data()