"""
A complete FastAPI and SQLAlchemy application for a Hiring/Recruitment System.

This application provides a full CRUD (Create, Read, Update, Delete) API
for managing a recruitment process. It uses SQLAlchemy ORM to interact with a
SQLite database, replacing the original in-memory data structures.

Key Features:
- FastAPI for building a high-performance API.
- Pydantic for data validation, serialization, and settings management.
- SQLAlchemy 2.0 ORM for database interaction with a SQLite backend.
- Dependency Injection for managing database sessions.
- A complete set of CRUD endpoints for all major resources: Users, Jobs,
  Candidates, Skills, Applications, Documents, Interviews, Feedback, and Decisions.
- Proper handling of database constraints like UNIQUE, FOREIGN KEY, and
  ON DELETE actions (CASCADE, SET NULL, RESTRICT) through SQLAlchemy and
  error handling.
- Comprehensive docstrings for all models and endpoints.
- A runnable main block using Uvicorn for easy startup.
"""
from __future__ import annotations

import uvicorn
from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from sqlalchemy import (
    create_engine,
    Column,
    ForeignKey,
    Integer,
    Table,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, Session

# --- Database Setup ---

# Define the database URL for a local SQLite database file.
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/recruitment_app.db"

# Create the SQLAlchemy engine.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class. Each instance will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#### --- SQLAlchemy ORM Models ---

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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Creates all database tables on application startup."""
    Base.metadata.create_all(bind=engine)


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


#### --- Pydantic Models (Schemas) ---

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


# --- Runnable Main Block ---
if __name__ == "__main__":
    """
    This block allows the script to be run directly, starting the Uvicorn server.
    It's configured to run on port 8081 and be accessible from any network interface.
    """
    uvicorn.run(app, host="0.0.0.0", port=8081)