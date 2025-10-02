import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
import os

# Add the current directory to the path to allow for imports
# This is necessary for the `if __name__ == "__main__"` block to work correctly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# --- FastAPI Application Code ---
# The provided application code is placed here directly to create a single, executable file.

from __future__ import annotations

import uvicorn
from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from sqlalchemy import (
    create_engine as create_prod_engine,
    Column,
    ForeignKey,
    Integer,
    Table,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

# --- Database Setup ---

# Define the production database URL. This will be overridden for tests.
SQLALCHEMY_DATABASE_URL = "sqlite:///./recruitment_app_test.db"

# Create the SQLAlchemy engine.
prod_engine = create_prod_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class. Each instance will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=prod_engine)


# --- SQLAlchemy ORM Models ---

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass


# Association table for the many-to-many relationship between candidates and skills
candidate_skills_table = Table(
    "candidate_skills",
    Base.metadata,
    Column("candidate_id", ForeignKey("candidates.candidate_id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", ForeignKey("skills.skill_id", ondelete="CASCADE"), primary_key=True),
)

# Association table for the many-to-many relationship between interviews and users (participants)
interview_participants_table = Table(
    "interview_participants",
    Base.metadata,
    Column("interview_id", ForeignKey("interviews.interview_id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True),
)


class sqa_User(Base):
    """ORM model for the 'users' table."""
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text)
    last_name: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text, unique=True)
    role: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.utcnow
    )
    jobs_created: Mapped[list["sqa_Job"]] = relationship(
        "sqa_Job", back_populates="creator", foreign_keys="sqa_Job.created_by_user_id"
    )
    feedback: Mapped[list["sqa_Feedback"]] = relationship("sqa_Feedback", back_populates="user")
    decision_logs: Mapped[list["sqa_DecisionLog"]] = relationship("sqa_DecisionLog", back_populates="user")


class sqa_Candidate(Base):
    """ORM model for the 'candidates' table."""
    __tablename__ = "candidates"

    candidate_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text)
    last_name: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text, unique=True)
    phone: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.utcnow
    )
    applications: Mapped[list["sqa_Application"]] = relationship(
        "sqa_Application", back_populates="candidate", cascade="all, delete-orphan"
    )
    skills: Mapped[list["sqa_Skill"]] = relationship(
        "sqa_Skill", secondary=candidate_skills_table, back_populates="candidates"
    )


class sqa_Application(Base):
    """ORM model for the 'applications' table."""
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("job_id", "candidate_id", name="uq_job_candidate"),)

    application_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.job_id", ondelete="CASCADE"))
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.candidate_id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default="applied")
    applied_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.utcnow
    )
    job: Mapped["sqa_Job"] = relationship("sqa_Job", back_populates="applications")
    candidate: Mapped["sqa_Candidate"] = relationship("sqa_Candidate", back_populates="applications")
    documents: Mapped[list["sqa_Document"]] = relationship(
        "sqa_Document", back_populates="application", cascade="all, delete-orphan"
    )
    interviews: Mapped[list["sqa_Interview"]] = relationship(
        "sqa_Interview", back_populates="application", cascade="all, delete-orphan"
    )
    feedback: Mapped[list["sqa_Feedback"]] = relationship(
        "sqa_Feedback", back_populates="application", cascade="all, delete-orphan"
    )
    decision_logs: Mapped[list["sqa_DecisionLog"]] = relationship(
        "sqa_DecisionLog", back_populates="application", cascade="all, delete-orphan"
    )


class sqa_Job(Base):
    """ORM model for the 'jobs' table."""
    __tablename__ = "jobs"
    job_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="RESTRICT"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.utcnow
    )
    creator: Mapped["sqa_User"] = relationship(
        "sqa_User", back_populates="jobs_created", foreign_keys=[created_by_user_id]
    )
    applications: Mapped[list["sqa_Application"]] = relationship(
        "sqa_Application", back_populates="job", cascade="all, delete-orphan"
    )


class sqa_Skill(Base):
    """ORM model for the 'skills' table."""
    __tablename__ = "skills"
    skill_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True)
    candidates: Mapped[list["sqa_Candidate"]] = relationship(
        "sqa_Candidate", secondary=candidate_skills_table, back_populates="skills"
    )


class sqa_Document(Base):
    """ORM model for the 'documents' table."""
    __tablename__ = "documents"
    document_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.application_id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(Text)
    file_path: Mapped[str] = mapped_column(Text, unique=True)
    uploaded_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    application: Mapped["sqa_Application"] = relationship("sqa_Application", back_populates="documents")


class sqa_Interview(Base):
    """ORM model for the 'interviews' table."""
    __tablename__ = "interviews"
    interview_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.application_id", ondelete="CASCADE"))
    interview_stage: Mapped[str] = mapped_column(Text)
    start_time: Mapped[datetime] = mapped_column()
    end_time: Mapped[datetime] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.utcnow
    )
    application: Mapped["sqa_Application"] = relationship("sqa_Application", back_populates="interviews")
    feedback: Mapped[list["sqa_Feedback"]] = relationship("sqa_Feedback", back_populates="interview")


class sqa_Feedback(Base):
    """ORM model for the 'feedback' table."""
    __tablename__ = "feedback"
    feedback_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.application_id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="RESTRICT"))
    interview_id: Mapped[int | None] = mapped_column(ForeignKey("interviews.interview_id", ondelete="SET NULL"))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    application: Mapped["sqa_Application"] = relationship("sqa_Application", back_populates="feedback")
    user: Mapped["sqa_User"] = relationship("sqa_User", back_populates="feedback")
    interview: Mapped["sqa_Interview | None"] = relationship("sqa_Interview", back_populates="feedback")


class sqa_DecisionLog(Base):
    """ORM model for the 'decision_logs' table."""
    __tablename__ = "decision_logs"
    decision_log_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.application_id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="RESTRICT"))
    decision: Mapped[str] = mapped_column(Text)
    reason: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    application: Mapped["sqa_Application"] = relationship("sqa_Application", back_populates="decision_logs")
    user: Mapped["sqa_User"] = relationship("sqa_User", back_populates="decision_logs")


# --- FastAPI Dependency for Database Session ---

def get_db():
    """
    FastAPI dependency that provides a SQLAlchemy database session per request.
    Ensures the session is closed after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Application Setup ---
app = FastAPI(
    title="Hiring System API",
    description="An API for managing a recruitment process, using FastAPI and SQLAlchemy.",
    version="2.0.0",
)


@app.on_event("startup")
def on_startup():
    """Creates all database tables on application startup."""
    Base.metadata.create_all(bind=prod_engine)


# --- Enums for CHECK Constraints ---

class UserRole(str, Enum):
    HR_MANAGER = 'HR Manager'
    RECRUITMENT_COORDINATOR = 'Recruitment Coordinator'
    HIRING_MANAGER = 'Hiring Manager'
    PROJECT_MANAGER = 'Project Manager'


class ApplicationStatus(str, Enum):
    APPLIED = 'applied'
    SCREENING = 'screening'
    INTERVIEWING = 'interviewing'
    OFFER_EXTENDED = 'offer_extended'
    HIRED = 'hired'
    REJECTED = 'rejected'
    WITHDRAWN = 'withdrawn'


class Decision(str, Enum):
    MOVE_TO_NEXT_STAGE = 'move_to_next_stage'
    OFFER = 'offer'
    NO_OFFER = 'no_offer'
    HIRE = 'hire'
    REJECT = 'reject'
    ON_HOLD = 'on_hold'


# --- Pydantic Models (Schemas) ---

# User Schemas
class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, description="User's first name.")
    last_name: str = Field(..., min_length=1, description="User's last name.")
    email: EmailStr = Field(..., description="User's unique email address.")
    role: UserRole = Field(..., description="The role of the user in the system.")


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None


class User(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Candidate Schemas
class CandidateBase(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr
    phone: Optional[str] = None


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class Candidate(CandidateBase):
    candidate_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Job Schemas
class JobBase(BaseModel):
    title: str = Field(..., min_length=3)
    description: str
    created_by_user_id: int


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = None


class Job(JobBase):
    job_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Application Schemas
class ApplicationBase(BaseModel):
    job_id: int
    candidate_id: int
    status: ApplicationStatus = Field(default=ApplicationStatus.APPLIED)


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None


class Application(ApplicationBase):
    application_id: int
    applied_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- User Endpoints ---

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> sqa_User:
    """
    Creates a new user. The email must be unique.
    """
    db_user = db.query(sqa_User).filter(sqa_User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user.email}' already exists.",
        )
    new_user = sqa_User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/", response_model=List[User], tags=["Users"])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[sqa_User]:
    """
    Retrieves a list of all users with pagination.
    """
    return db.query(sqa_User).offset(skip).limit(limit).all()


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
def get_user(user_id: int, db: Session = Depends(get_db)) -> sqa_User:
    """
    Retrieves a single user by their ID.
    """
    db_user = db.query(sqa_User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")
    return db_user


@app.put("/users/{user_id}", response_model=User, tags=["Users"])
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)) -> sqa_User:
    """
    Updates an existing user's details.
    """
    db_user = db.query(sqa_User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")

    update_data = user_update.model_dump(exclude_unset=True)
    if 'email' in update_data:
        existing_user = db.query(sqa_User).filter(sqa_User.email == update_data['email']).first()
        if existing_user and existing_user.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email '{update_data['email']}' already exists.",
            )

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletes a user. Fails if the user is linked to jobs, feedback, or
    decisions due to RESTRICT constraints.
    """
    db_user = db.query(sqa_User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")
    try:
        db.delete(db_user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot delete user {user_id}. They are referenced by other records (e.g., jobs, feedback).",
        )
    return


# --- Candidate Endpoints ---

@app.post("/candidates/", response_model=Candidate, status_code=status.HTTP_201_CREATED, tags=["Candidates"])
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)) -> sqa_Candidate:
    """
    Creates a new candidate. The email must be unique.
    """
    db_candidate = db.query(sqa_Candidate).filter(sqa_Candidate.email == candidate.email).first()
    if db_candidate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Candidate with email '{candidate.email}' already exists.",
        )
    new_candidate = sqa_Candidate(**candidate.model_dump())
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    return new_candidate


@app.get("/candidates/", response_model=List[Candidate], tags=["Candidates"])
def get_all_candidates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[sqa_Candidate]:
    """
    Retrieves a list of all candidates with pagination.
    """
    return db.query(sqa_Candidate).offset(skip).limit(limit).all()


@app.get("/candidates/{candidate_id}", response_model=Candidate, tags=["Candidates"])
def get_candidate(candidate_id: int, db: Session = Depends(get_db)) -> sqa_Candidate:
    """
    Retrieves a single candidate by their ID.
    """
    db_candidate = db.query(sqa_Candidate).get(candidate_id)
    if not db_candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with ID {candidate_id} not found")
    return db_candidate


@app.put("/candidates/{candidate_id}", response_model=Candidate, tags=["Candidates"])
def update_candidate(candidate_id: int, candidate_update: CandidateUpdate, db: Session = Depends(get_db)) -> sqa_Candidate:
    """
    Updates an existing candidate's details.
    """
    db_candidate = db.query(sqa_Candidate).get(candidate_id)
    if not db_candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with ID {candidate_id} not found")

    update_data = candidate_update.model_dump(exclude_unset=True)
    if 'email' in update_data:
        existing_candidate = db.query(sqa_Candidate).filter(sqa_Candidate.email == update_data['email']).first()
        if existing_candidate and existing_candidate.candidate_id != candidate_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Candidate with email '{update_data['email']}' already exists.",
            )

    for key, value in update_data.items():
        setattr(db_candidate, key, value)

    db.commit()
    db.refresh(db_candidate)
    return db_candidate


@app.delete("/candidates/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Candidates"])
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """
    Deletes a candidate and all their associated data (applications, documents, etc.)
    due to CASCADE constraints.
    """
    db_candidate = db.query(sqa_Candidate).get(candidate_id)
    if not db_candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with ID {candidate_id} not found")
    db.delete(db_candidate)
    db.commit()
    return


# --- Job Endpoints ---

@app.post("/jobs/", response_model=Job, status_code=status.HTTP_201_CREATED, tags=["Jobs"])
def create_job(job: JobCreate, db: Session = Depends(get_db)) -> sqa_Job:
    """
    Creates a new job posting. The creating user must exist.
    """
    creator = db.query(sqa_User).get(job.created_by_user_id)
    if not creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {job.created_by_user_id} not found.",
        )

    new_job = sqa_Job(**job.model_dump())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


@app.get("/jobs/", response_model=List[Job], tags=["Jobs"])
def get_all_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[sqa_Job]:
    """
    Retrieves a list of all jobs with pagination.
    """
    return db.query(sqa_Job).offset(skip).limit(limit).all()


@app.get("/jobs/{job_id}", response_model=Job, tags=["Jobs"])
def get_job(job_id: int, db: Session = Depends(get_db)) -> sqa_Job:
    """
    Retrieves a single job by its ID.
    """
    db_job = db.query(sqa_Job).get(job_id)
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with ID {job_id} not found")
    return db_job


# --- Application Endpoints ---

@app.post("/applications/", response_model=Application, status_code=status.HTTP_201_CREATED, tags=["Applications"])
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)) -> sqa_Application:
    """
    Creates a new job application. A candidate can only apply for a given job once.
    """
    # Check if foreign keys exist
    if not db.query(sqa_Job).get(application.job_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with ID {application.job_id} not found")
    if not db.query(sqa_Candidate).get(application.candidate_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with ID {application.candidate_id} not found")

    new_application = sqa_Application(**application.model_dump())
    db.add(new_application)
    try:
        db.commit()
        db.refresh(new_application)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Candidate {application.candidate_id} has already applied for job {application.job_id}.",
        )
    return new_application


@app.get("/applications/", response_model=List[Application], tags=["Applications"])
def get_all_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[sqa_Application]:
    """
    Retrieves a list of all applications with pagination.
    """
    return db.query(sqa_Application).offset(skip).limit(limit).all()


@app.get("/applications/{application_id}", response_model=Application, tags=["Applications"])
def get_application(application_id: int, db: Session = Depends(get_db)) -> sqa_Application:
    """
    Retrieves a single application by its ID.
    """
    db_application = db.query(sqa_Application).get(application_id)
    if not db_application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Application with ID {application_id} not found")
    return db_application


@app.put("/applications/{application_id}", response_model=Application, tags=["Applications"])
def update_application(application_id: int, app_update: ApplicationUpdate, db: Session = Depends(get_db)) -> sqa_Application:
    """
    Updates the status of an application.
    """
    db_application = db.query(sqa_Application).get(application_id)
    if not db_application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Application with ID {application_id} not found")

    update_data = app_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_application, key, value)

    db.commit()
    db.refresh(db_application)
    return db_application


@app.delete("/applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Applications"])
def delete_application(application_id: int, db: Session = Depends(get_db)):
    """
    Deletes an application and all its associated data (documents, interviews, etc.)
    due to CASCADE constraints.
    """
    db_application = db.query(sqa_Application).get(application_id)
    if not db_application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Application with ID {application_id} not found")

    db.delete(db_application)
    db.commit()
    return


# --- Welcome Endpoint ---
@app.get("/", include_in_schema=False)
def root():
    """A simple welcome message for the API root."""
    return {"message": "Welcome to the Hiring System API. Visit /docs for documentation."}


# --- Pytest Test Suite ---

# --- Test Database Setup ---
# Use an in-memory SQLite database for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Use StaticPool for in-memory DB with TestClient
)

# Create a new sessionmaker for the test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# --- Dependency Override ---
# Override the `get_db` dependency to use the test database session
def override_get_db():
    """Dependency to provide a test database session."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply the override to the FastAPI app
app.dependency_overrides[get_db] = override_get_db


# --- Pytest Fixture for Test Client and Database ---
@pytest.fixture(scope="function")
def client():
    """
    Pytest fixture to set up and tear down the database for each test function.
    It creates all tables before a test and drops them afterwards, ensuring
    a clean state for every test case.
    """
    # Create all tables in the in-memory database before each test
    Base.metadata.create_all(bind=test_engine)
    # Yield a TestClient instance
    with TestClient(app) as c:
        yield c
    # Drop all tables after each test to ensure isolation
    Base.metadata.drop_all(bind=test_engine)


# --- Helper functions for tests ---
def create_test_user(client: TestClient, email="test.user@example.com", role="HR Manager"):
    """Helper to create a user for dependency purposes."""
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": email,
        "role": role
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    return response.json()

def create_test_candidate(client: TestClient, email="test.candidate@example.com"):
    """Helper to create a candidate for dependency purposes."""
    candidate_data = {
        "first_name": "Test",
        "last_name": "Candidate",
        "email": email,
        "phone": "1234567890"
    }
    response = client.post("/candidates/", json=candidate_data)
    assert response.status_code == 201
    return response.json()

def create_test_job(client: TestClient, user_id: int):
    """Helper to create a job for dependency purposes."""
    job_data = {
        "title": "Software Engineer",
        "description": "Develop amazing software.",
        "created_by_user_id": user_id
    }
    response = client.post("/jobs/", json=job_data)
    assert response.status_code == 201
    return response.json()


# --- Test Cases ---

def test_root_endpoint(client: TestClient):
    """Test the root welcome endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Hiring System API. Visit /docs for documentation."}

# --- User Endpoint Happy Path Tests ---

def test_create_user_happy_path(client: TestClient):
    """Test successful creation of a new user."""
    user_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "role": "Hiring Manager"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["first_name"] == user_data["first_name"]
    assert "user_id" in data

def test_get_all_users_happy_path(client: TestClient):
    """Test retrieving a list of all users."""
    create_test_user(client, "user1@example.com")
    create_test_user(client, "user2@example.com")

    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == "user1@example.com"
    assert data[1]["email"] == "user2@example.com"

def test_get_user_by_id_happy_path(client: TestClient):
    """Test retrieving a single user by their ID."""
    user = create_test_user(client)
    user_id = user["user_id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["email"] == user["email"]

def test_update_user_happy_path(client: TestClient):
    """Test successfully updating a user's details."""
    user = create_test_user(client)
    user_id = user["user_id"]
    update_data = {"first_name": "John", "role": "Project Manager"}

    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["first_name"] == "John"
    assert data["role"] == "Project Manager"
    assert data["email"] == user["email"]  # Email should not have changed

def test_delete_user_happy_path(client: TestClient):
    """Test successfully deleting a user who has no dependencies."""
    user = create_test_user(client)
    user_id = user["user_id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verify user is gone
    response_get = client.get(f"/users/{user_id}")
    assert response_get.status_code == 404

# --- User Endpoint Edge Case and Error Tests ---

def test_create_user_duplicate_email(client: TestClient):
    """Test creating a user with an email that already exists."""
    email = "duplicate@example.com"
    create_test_user(client, email=email)
    user_data = {"first_name": "Another", "last_name": "User", "email": email, "role": "HR Manager"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

@pytest.mark.parametrize("invalid_payload, error_detail", [
    ({"last_name": "Doe", "email": "a@b.com", "role": "HR Manager"}, "Field required"),
    ({"first_name": "", "last_name": "Doe", "email": "a@b.com", "role": "HR Manager"}, "String should have at least 1 character"),
    ({"first_name": "Jane", "last_name": "Doe", "email": "not-an-email", "role": "HR Manager"}, "value is not a valid email address"),
    ({"first_name": "Jane", "last_name": "Doe", "email": "a@b.com", "role": "Invalid Role"}, "Input should be 'HR Manager'"),
])
def test_create_user_invalid_data(client: TestClient, invalid_payload, error_detail):
    """Test creating a user with various invalid inputs."""
    response = client.post("/users/", json=invalid_payload)
    assert response.status_code == 422
    assert error_detail in str(response.json()["detail"])

def test_get_nonexistent_user(client: TestClient):
    """Test retrieving a user that does not exist."""
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User with ID 999 not found"

def test_update_nonexistent_user(client: TestClient):
    """Test updating a user that does not exist."""
    response = client.put("/users/999", json={"first_name": "Ghost"})
    assert response.status_code == 404

def test_update_user_email_conflict(client: TestClient):
    """Test updating a user's email to one that is already in use."""
    user1 = create_test_user(client, email="user1@example.com")
    user2 = create_test_user(client, email="user2@example.com")
    response = client.put(f"/users/{user2['user_id']}", json={"email": user1["email"]})
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

def test_delete_nonexistent_user(client: TestClient):
    """Test deleting a user that does not exist."""
    response = client.delete("/users/999")
    assert response.status_code == 404

def test_delete_user_with_dependencies_fails(client: TestClient):
    """Test that deleting a user with a job dependency fails due to RESTRICT constraint."""
    user = create_test_user(client)
    create_test_job(client, user["user_id"])
    response = client.delete(f"/users/{user['user_id']}")
    assert response.status_code == 409
    assert "referenced by other records" in response.json()["detail"]

def test_get_all_users_empty(client: TestClient):
    """Test retrieving users when none exist."""
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []

# --- Candidate Endpoint Happy Path Tests ---

def test_create_candidate_happy_path(client: TestClient):
    """Test successful creation of a new candidate."""
    candidate_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com",
        "phone": "555-1234"
    }
    response = client.post("/candidates/", json=candidate_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == candidate_data["email"]
    assert data["phone"] == candidate_data["phone"]
    assert "candidate_id" in data

def test_get_all_candidates_happy_path(client: TestClient):
    """Test retrieving a list of all candidates."""
    create_test_candidate(client, "candidate1@example.com")
    create_test_candidate(client, "candidate2@example.com")

    response = client.get("/candidates/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == "candidate1@example.com"

def test_get_candidate_by_id_happy_path(client: TestClient):
    """Test retrieving a single candidate by their ID."""
    candidate = create_test_candidate(client)
    candidate_id = candidate["candidate_id"]

    response = client.get(f"/candidates/{candidate_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["candidate_id"] == candidate_id
    assert data["email"] == candidate["email"]

def test_update_candidate_happy_path(client: TestClient):
    """Test successfully updating a candidate's details."""
    candidate = create_test_candidate(client)
    candidate_id = candidate["candidate_id"]
    update_data = {"phone": "555-5678", "last_name": "Jones"}

    response = client.put(f"/candidates/{candidate_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["candidate_id"] == candidate_id
    assert data["phone"] == "555-5678"
    assert data["last_name"] == "Jones"

def test_delete_candidate_happy_path(client: TestClient):
    """Test successfully deleting a candidate."""
    candidate = create_test_candidate(client)
    candidate_id = candidate["candidate_id"]

    response = client.delete(f"/candidates/{candidate_id}")
    assert response.status_code == 204

    # Verify candidate is gone
    response_get = client.get(f"/candidates/{candidate_id}")
    assert response_get.status_code == 404

# --- Candidate Endpoint Edge Case and Error Tests ---

def test_create_candidate_duplicate_email(client: TestClient):
    """Test creating a candidate with a duplicate email fails."""
    email = "taken@example.com"
    create_test_candidate(client, email=email)
    candidate_data = {"first_name": "Duplicate", "last_name": "Person", "email": email}
    response = client.post("/candidates/", json=candidate_data)
    assert response.status_code == 409

def test_get_nonexistent_candidate(client: TestClient):
    """Test retrieving a candidate that does not exist."""
    response = client.get("/candidates/999")
    assert response.status_code == 404

def test_update_nonexistent_candidate(client: TestClient):
    """Test updating a candidate that does not exist."""
    response = client.put("/candidates/999", json={"first_name": "Ghost"})
    assert response.status_code == 404

def test_update_candidate_email_conflict(client: TestClient):
    """Test updating a candidate's email to one that is already in use."""
    candidate1 = create_test_candidate(client, email="c1@example.com")
    candidate2 = create_test_candidate(client, email="c2@example.com")
    response = client.put(f"/candidates/{candidate2['candidate_id']}", json={"email": candidate1["email"]})
    assert response.status_code == 409

def test_delete_nonexistent_candidate(client: TestClient):
    """Test deleting a candidate that does not exist."""
    response = client.delete("/candidates/999")
    assert response.status_code == 404

def test_delete_candidate_cascades_to_application(client: TestClient):
    """Test that deleting a candidate also deletes their applications via CASCADE."""
    user = create_test_user(client)
    job = create_test_job(client, user["user_id"])
    candidate = create_test_candidate(client)
    
    app_data = {"job_id": job["job_id"], "candidate_id": candidate["candidate_id"]}
    app_response = client.post("/applications/", json=app_data)
    assert app_response.status_code == 201
    application_id = app_response.json()["application_id"]

    # Delete the candidate
    delete_response = client.delete(f"/candidates/{candidate['candidate_id']}")
    assert delete_response.status_code == 204

    # Verify the application is also gone
    get_app_response = client.get(f"/applications/{application_id}")
    assert get_app_response.status_code == 404

# --- Job Endpoint Happy Path Tests ---

def test_create_job_happy_path(client: TestClient):
    """Test successful creation of a new job."""
    user = create_test_user(client)
    job_data = {
        "title": "Senior Python Developer",
        "description": "Looking for an expert in Python and FastAPI.",
        "created_by_user_id": user["user_id"]
    }
    response = client.post("/jobs/", json=job_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == job_data["title"]
    assert data["created_by_user_id"] == user["user_id"]
    assert "job_id" in data

def test_get_all_jobs_happy_path(client: TestClient):
    """Test retrieving a list of all jobs."""
    user = create_test_user(client)
    response1 = client.post("/jobs/", json={"title": "Job 1", "description": "Desc 1", "created_by_user_id": user["user_id"]})
    response2 = client.post("/jobs/", json={"title": "Job 2", "description": "Desc 2", "created_by_user_id": user["user_id"]})
    assert response1.status_code == 201
    assert response2.status_code == 201

    response = client.get("/jobs/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Job 1"
    assert data[1]["title"] == "Job 2"

def test_get_job_by_id_happy_path(client: TestClient):
    """Test retrieving a single job by its ID."""
    user = create_test_user(client)
    job = create_test_job(client, user["user_id"])
    job_id = job["job_id"]

    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == job_id
    assert data["title"] == job["title"]

# --- Job Endpoint Edge Case and Error Tests ---

def test_create_job_with_nonexistent_user(client: TestClient):
    """Test creating a job with a user ID that does not exist."""
    job_data = {
        "title": "Ghost Job",
        "description": "This job has no creator.",
        "created_by_user_id": 999
    }
    response = client.post("/jobs/", json=job_data)
    assert response.status_code == 404
    assert "User with ID 999 not found" in response.json()["detail"]

def test_create_job_with_invalid_title(client: TestClient):
    """Test creating a job with a title that is too short."""
    user = create_test_user(client)
    job_data = {
        "title": "J",
        "description": "Short title job.",
        "created_by_user_id": user["user_id"]
    }
    response = client.post("/jobs/", json=job_data)
    assert response.status_code == 422
    assert "String should have at least 3 characters" in str(response.json()["detail"])

def test_get_nonexistent_job(client: TestClient):
    """Test retrieving a job that does not exist."""
    response = client.get("/jobs/999")
    assert response.status_code == 404

# --- Application Endpoint Happy Path Tests ---

def test_create_application_happy_path(client: TestClient):
    """Test successful creation of a new application."""
    user = create_test_user(client)
    candidate = create_test_candidate(client)
    job = create_test_job(client, user["user_id"])

    application_data = {
        "job_id": job["job_id"],
        "candidate_id": candidate["candidate_id"],
        "status": "applied"
    }
    response = client.post("/applications/", json=application_data)
    assert response.status_code == 201
    data = response.json()
    assert data["job_id"] == job["job_id"]
    assert data["candidate_id"] == candidate["candidate_id"]
    assert data["status"] == "applied"
    assert "application_id" in data

def test_get_all_applications_happy_path(client: TestClient):
    """Test retrieving a list of all applications."""
    user = create_test_user(client)
    candidate1 = create_test_candidate(client, "c1@example.com")
    candidate2 = create_test_candidate(client, "c2@example.com")
    job = create_test_job(client, user["user_id"])

    client.post("/applications/", json={"job_id": job["job_id"], "candidate_id": candidate1["candidate_id"]})
    client.post("/applications/", json={"job_id": job["job_id"], "candidate_id": candidate2["candidate_id"]})

    response = client.get("/applications/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["candidate_id"] == candidate1["candidate_id"]
    assert data[1]["candidate_id"] == candidate2["candidate_id"]

def test_get_application_by_id_happy_path(client: TestClient):
    """Test retrieving a single application by its ID."""
    user = create_test_user(client)
    candidate = create_test_candidate(client)
    job = create_test_job(client, user["user_id"])
    app_response = client.post("/applications/", json={"job_id": job["job_id"], "candidate_id": candidate["candidate_id"]})
    application_id = app_response.json()["application_id"]

    response = client.get(f"/applications/{application_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["application_id"] == application_id
    assert data["job_id"] == job["job_id"]

def test_update_application_happy_path(client: TestClient):
    """Test successfully updating an application's status."""
    user = create_test_user(client)
    candidate = create_test_candidate(client)
    job = create_test_job(client, user["user_id"])
    app_response = client.post("/applications/", json={"job_id": job["job_id"], "candidate_id": candidate["candidate_id"]})
    application_id = app_response.json()["application_id"]

    update_data = {"status": "screening"}
    response = client.put(f"/applications/{application_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["application_id"] == application_id
    assert data["status"] == "screening"

def test_delete_application_happy_path(client: TestClient):
    """Test successfully deleting an application."""
    user = create_test_user(client)
    candidate = create_test_candidate(client)
    job = create_test_job(client, user["user_id"])
    app_response = client.post("/applications/", json={"job_id": job["job_id"], "candidate_id": candidate["candidate_id"]})
    application_id = app_response.json()["application_id"]

    response = client.delete(f"/applications/{application_id}")
    assert response.status_code == 204

    # Verify application is gone
    response_get = client.get(f"/applications/{application_id}")
    assert response_get.status_code == 404

# --- Application Endpoint Edge Case and Error Tests ---

def test_create_application_duplicate(client: TestClient):
    """Test that a candidate cannot apply for the same job twice."""
    user = create_test_user(client)
    candidate = create_test_candidate(client)
    job = create_test_job(client, user["user_id"])
    application_data = {"job_id": job["job_id"], "candidate_id": candidate["candidate_id"]}
    
    # First application should succeed
    response1 = client.post("/applications/", json=application_data)
    assert response1.status_code == 201

    # Second application should fail
    response2 = client.post("/applications/", json=application_data)
    assert response2.status_code == 409
    assert "has already applied" in response2.json()["detail"]

def test_create_application_with_nonexistent_job(client: TestClient):
    """Test creating an application for a job that does not exist."""
    candidate = create_test_candidate(client)
    application_data = {"job_id": 999, "candidate_id": candidate["candidate_id"]}
    response = client.post("/applications/", json=application_data)
    assert response.status_code == 404
    assert "Job with ID 999 not found" in response.json()["detail"]

def test_create_application_with_nonexistent_candidate(client: TestClient):
    """Test creating an application for a candidate that does not exist."""
    user = create_test_user(client)
    job = create_test_job(client, user["user_id"])
    application_data = {"job_id": job["job_id"], "candidate_id": 999}
    response = client.post("/applications/", json=application_data)
    assert response.status_code == 404
    assert "Candidate with ID 999 not found" in response.json()["detail"]

def test_get_nonexistent_application(client: TestClient):
    """Test retrieving an application that does not exist."""
    response = client.get("/applications/999")
    assert response.status_code == 404

def test_update_nonexistent_application(client: TestClient):
    """Test updating an application that does not exist."""
    response = client.put("/applications/999", json={"status": "hired"})
    assert response.status_code == 404

def test_update_application_invalid_status(client: TestClient):
    """Test updating an application with an invalid status enum value."""
    user = create_test_user(client)
    candidate = create_test_candidate(client)
    job = create_test_job(client, user["user_id"])
    app_response = client.post("/applications/", json={"job_id": job["job_id"], "candidate_id": candidate["candidate_id"]})
    application_id = app_response.json()["application_id"]

    response = client.put(f"/applications/{application_id}", json={"status": "invalid_status"})
    assert response.status_code == 422
    assert "Input should be 'applied', 'screening'" in str(response.json()["detail"])

def test_delete_nonexistent_application(client: TestClient):
    """Test deleting an application that does not exist."""
    response = client.delete("/applications/999")
    assert response.status_code == 404


if __name__ == "__main__":
    """
    This block allows the script to be run directly, executing the pytest tests.
    """
    # We pass the filename to pytest.main to ensure it runs tests from this file.
    # The '-v' flag is for verbose output.
    sys.exit(pytest.main([__file__, "-v"]))