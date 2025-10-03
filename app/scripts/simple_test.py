import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db, Base

# Set up the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./recruitment_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a new database session for testing
Base.metadata.create_all(bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Before each test, clear the database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # After each test, clear the database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_create_and_get_user():
    # Create a user
    response = client.post(
        "/users/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "role": "HR Manager",
        },
    )
    assert response.status_code == 201
    user_id = response.json()["user_id"]

    # Get the created user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "john.doe@example.com"

def test_create_and_get_candidate():
    # Create a candidate
    response = client.post(
        "/candidates/",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "phone": "1234567890",
        },
    )
    assert response.status_code == 201
    candidate_id = response.json()["candidate_id"]

    # Get the created candidate
    response = client.get(f"/candidates/{candidate_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "jane.doe@example.com"

def test_create_and_get_job():
    # First, create a user to be the job creator
    response = client.post(
        "/users/",
        json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com",
            "role": "Hiring Manager",
        },
    )
    assert response.status_code == 201
    user_id = response.json()["user_id"]

    # Create a job
    response = client.post(
        "/jobs/",
        json={
            "title": "Software Engineer",
            "description": "Develop and maintain software solutions.",
            "created_by_user_id": user_id,
        },
    )
    assert response.status_code == 201
    job_id = response.json()["job_id"]

    # Get the created job
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Software Engineer"

def test_create_and_get_application():
    # Create user, candidate, and job first
    response = client.post(
        "/users/",
        json={
            "first_name": "Bob",
            "last_name": "Brown",
            "email": "bob.brown@example.com",
            "role": "Recruitment Coordinator",
        },
    )
    assert response.status_code == 201
    user_id = response.json()["user_id"]

    response = client.post(
        "/candidates/",
        json={
            "first_name": "Mary",
            "last_name": "Johnson",
            "email": "mary.johnson@example.com",
            "phone": "0987654321",
        },
    )
    assert response.status_code == 201
    candidate_id = response.json()["candidate_id"]

    response = client.post(
        "/jobs/",
        json={
            "title": "Data Scientist",
            "description": "Analyze and interpret complex data.",
            "created_by_user_id": user_id,
        },
    )
    assert response.status_code == 201
    job_id = response.json()["job_id"]

    # Create an application
    response = client.post(
        "/applications/",
        json={
            "job_id": job_id,
            "candidate_id": candidate_id,
            "status": "applied",
        },
    )
    assert response.status_code == 201
    application_id = response.json()["application_id"]

    # Get the created application
    response = client.get(f"/applications/{application_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "applied"

if __name__ == "__main__":
    pytest.main()