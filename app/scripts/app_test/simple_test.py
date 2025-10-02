import pytest
from fastapi.testclient import TestClient
from main import app, get_db, Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_recruitment_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test tables
Base.metadata.create_all(bind=engine)

# Dependency override for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def setup_users():
    users = [
        {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "role": "HR Manager"},
        {"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "role": "Recruitment Coordinator"},
    ]
    for user in users:
        client.post("/users/", json=user)
    return users

@pytest.fixture
def setup_candidates():
    candidates = [
        {"first_name": "Alice", "last_name": "Smith", "email": "alice.smith@example.com", "phone": "1234567890"},
        {"first_name": "Bob", "last_name": "Brown", "email": "bob.brown@example.com", "phone": "0987654321"},
    ]
    for candidate in candidates:
        client.post("/candidates/", json=candidate)
    return candidates

@pytest.fixture
def setup_jobs(setup_users):
    jobs = [
        {"title": "Backend Developer", "description": "Develop backend services.", "created_by_user_id": 1},
        {"title": "Frontend Developer", "description": "Develop frontend interfaces.", "created_by_user_id": 2},
    ]
    for job in jobs:
        client.post("/jobs/", json=job)
    return jobs

@pytest.fixture
def setup_applications(setup_candidates, setup_jobs):
    applications = [
        {"job_id": 1, "candidate_id": 1},
        {"job_id": 2, "candidate_id": 2},
    ]
    for application in applications:
        client.post("/applications/", json=application)
    return applications

def test_create_user():
    response = client.post("/users/", json={"first_name": "Test", "last_name": "User", "email": "test.user@example.com", "role": "HR Manager"})
    assert response.status_code == 201
    assert response.json()["email"] == "test.user@example.com"

def test_get_all_users(setup_users):
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["email"] == "john.doe@example.com"

def test_update_user():
    response = client.put("/users/1", json={"first_name": "Johnathan"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "Johnathan"

def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 204

def test_create_candidate():
    response = client.post("/candidates/", json={"first_name": "New", "last_name": "Candidate", "email": "new.candidate@example.com", "phone": "1231231234"})
    assert response.status_code == 201
    assert response.json()["email"] == "new.candidate@example.com"

def test_get_all_candidates(setup_candidates):
    response = client.get("/candidates/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_candidate():
    response = client.get("/candidates/1")
    assert response.status_code == 200
    assert response.json()["email"] == "alice.smith@example.com"

def test_update_candidate():
    response = client.put("/candidates/1", json={"first_name": "Alicia"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "Alicia"

def test_delete_candidate():
    response = client.delete("/candidates/1")
    assert response.status_code == 204

def test_create_job(setup_users):
    response = client.post("/jobs/", json={"title": "Data Scientist", "description": "Analyze data.", "created_by_user_id": 2})
    assert response.status_code == 201
    assert response.json()["title"] == "Data Scientist"

def test_get_all_jobs(setup_jobs):
    response = client.get("/jobs/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_job():
    response = client.get("/jobs/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Backend Developer"

def test_create_application(setup_jobs, setup_candidates):
    response = client.post("/applications/", json={"job_id": 1, "candidate_id": 2})
    assert response.status_code == 201
    assert response.json()["job_id"] == 1

def test_get_all_applications(setup_applications):
    response = client.get("/applications/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_application():
    response = client.get("/applications/1")
    assert response.status_code == 200
    assert response.json()["candidate_id"] == 1

def test_update_application():
    response = client.put("/applications/1", json={"status": "interviewing"})
    assert response.status_code == 200
    assert response.json()["status"] == "interviewing"

def test_delete_application():
    response = client.delete("/applications/1")
    assert response.status_code == 204

if __name__ == "__main__":
    pytest.main()