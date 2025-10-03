"""
This module defines the SQLAlchemy ORM models that map to the database tables
for the Applicant Tracking System.

Each class represents a table in the database and is defined using the
SQLAlchemy 2.0 declarative mapping style. The `sqa_` prefix is used for
all ORM class names as per the requirements.

Relationships between tables are defined using the `relationship` construct,
allowing for easy navigation and querying of related objects. Many-to-many
relationships are implemented using secondary association tables.
"""
from __future__ import annotations

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass


# Association table for the many-to-many relationship between candidates and skills
sqa_candidate_skills_table = Table(
    "candidate_skills",
    Base.metadata,
    Column("candidate_id", ForeignKey("candidates.candidate_id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", ForeignKey("skills.skill_id", ondelete="CASCADE"), primary_key=True),
)

# Association table for the many-to-many relationship between interviews and users (participants)
sqa_interview_participants_table = Table(
    "interview_participants",
    Base.metadata,
    Column("interview_id", ForeignKey("interviews.interview_id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True),
)


class sqa_User(Base):
    """
    ORM model for the 'users' table.

    Represents a system user, such as an HR Manager, Recruiter, or Hiring Manager.
    """

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text)
    last_name: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text, unique=True)
    role: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')")
    )
    updated_at: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        server_default=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')"),
        server_onupdate=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')"),
    )

    # Relationships
    jobs_created: Mapped[list["sqa_Job"]] = relationship(
        "sqa_Job", back_populates="creator", foreign_keys="sqa_Job.created_by_user_id"
    )
    jobs_managed: Mapped[list["sqa_Job"]] = relationship(
        "sqa_Job", back_populates="hiring_manager", foreign_keys="sqa_Job.hiring_manager_user_id"
    )
    interviews_scheduled: Mapped[list["sqa_Interview"]] = relationship(
        "sqa_Interview", back_populates="scheduler", foreign_keys="sqa_Interview.scheduled_by_user_id"
    )
    interviews_participating: Mapped[list["sqa_Interview"]] = relationship(
        "sqa_Interview", secondary=sqa_interview_participants_table, back_populates="participants"
    )
    feedback: Mapped[list["sqa_Feedback"]] = relationship("sqa_Feedback", back_populates="user")
    decision_logs: Mapped[list["sqa_DecisionLog"]] = relationship("sqa_DecisionLog", back_populates="user")


class sqa_Job(Base):
    """
    ORM model for the 'jobs' table.

    Represents a job posting created by a user.
    """

    __tablename__ = "jobs"

    job_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    department: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default="open")
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="RESTRICT"))
    hiring_manager_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.user_id", ondelete="SET NULL"))
    created_at: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')")
    )
    updated_at: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        server_default=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')"),
        server_onupdate=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')"),
    )

    # Relationships
    creator: Mapped["sqa_User"] = relationship(
        "sqa_User", back_populates="jobs_created", foreign_keys=[created_by_user_id]
    )
    hiring_manager: Mapped["sqa_User" | None] = relationship(
        "sqa_User", back_populates="jobs_managed", foreign_keys=[hiring_manager_user_id]
    )
    applications: Mapped[list["sqa_Application"]] = relationship("sqa_Application", back_populates="job")


class sqa_Candidate(Base):
    """
    ORM model for the 'candidates' table.

    Represents a candidate or applicant in the system.
    """

    __tablename__ = "candidates"

    candidate_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text)
    last_name: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text, unique=True)
    phone: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')")
    )
    updated_at: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        server_default=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')"),
        server_onupdate=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')"),
    )

    # Relationships
    applications: Mapped[list["sqa_Application"]] = relationship("sqa_Application", back_populates="candidate")
    skills: Mapped[list["sqa_Skill"]] = relationship(
        "sqa_Skill", secondary=sqa_candidate_skills_table, back_populates="candidates"
    )


class sqa_Skill(Base):
    """
    ORM model for the 'skills' table.

    Represents a skill that can be associated with a candidate.
    """

    __tablename__ = "skills"

    skill_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True)

    # Relationships
    candidates: Mapped[list["sqa_Candidate"]] = relationship(
        "sqa_Candidate", secondary=sqa_candidate_skills_table, back_populates="skills"
    )


class sqa_Application(Base):
    """
    ORM model for the 'applications' table.

    Represents a single application from a candidate for a specific job.
    """

    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("job_id", "candidate_id"),)

    application_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.job_id", ondelete="CASCADE"))
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.candidate_id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default="applied")
    applied_at: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')")
    )
    updated_at: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        server_default=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')"),
        server_onupdate=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')"),
    )

    # Relationships
    job: Mapped["sqa_Job"] = relationship("sqa_Job", back_populates="applications")
    candidate: Mapped["sqa_Candidate"] = relationship("sqa_Candidate", back_populates="applications")
    documents: Mapped[list["sqa_Document"]] = relationship("sqa_Document", back_populates="application")
    interviews: Mapped[list["sqa_Interview"]] = relationship("sqa_Interview", back_populates="application")
    feedback: Mapped[list["sqa_Feedback"]] = relationship("sqa_Feedback", back_populates="application")
    decision_logs: Mapped[list["sqa_DecisionLog"]] = relationship("sqa_DecisionLog", back_populates="application")


class sqa_Document(Base):
    """
    ORM model for the 'documents' table.

    Represents a document (e.g., resume, cover letter) associated with an application.
    """

    __tablename__ = "documents"

    document_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.application_id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(Text)
    file_path: Mapped[str] = mapped_column(Text, unique=True)
    uploaded_at: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')")
    )

    # Relationship
    application: Mapped["sqa_Application"] = relationship("sqa_Application", back_populates="documents")


class sqa_Interview(Base):
    """
    ORM model for the 'interviews' table.

    Represents a scheduled interview for a job application.
    """

    __tablename__ = "interviews"

    interview_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.application_id", ondelete="CASCADE"))
    scheduled_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="SET NULL"))
    interview_stage: Mapped[str] = mapped_column(Text)
    method: Mapped[str] = mapped_column(Text)
    location_or_link: Mapped[str | None] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')")
    )
    updated_at: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        server_default=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')"),
        server_onupdate=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')"),
    )

    # Relationships
    application: Mapped["sqa_Application"] = relationship("sqa_Application", back_populates="interviews")
    scheduler: Mapped["sqa_User"] = relationship(
        "sqa_User", back_populates="interviews_scheduled", foreign_keys=[scheduled_by_user_id]
    )
    participants: Mapped[list["sqa_User"]] = relationship(
        "sqa_User", secondary=sqa_interview_participants_table, back_populates="interviews_participating"
    )
    feedback: Mapped[list["sqa_Feedback"]] = relationship("sqa_Feedback", back_populates="interview")


class sqa_Feedback(Base):
    """
    ORM model for the 'feedback' table.

    Represents feedback provided by a user on an application,
    optionally linked to a specific interview.
    """

    __tablename__ = "feedback"

    feedback_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.application_id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="RESTRICT"))
    interview_id: Mapped[int | None] = mapped_column(ForeignKey("interviews.interview_id", ondelete="SET NULL"))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')")
    )

    # Relationships
    application: Mapped["sqa_Application"] = relationship("sqa_Application", back_populates="feedback")
    user: Mapped["sqa_User"] = relationship("sqa_User", back_populates="feedback")
    interview: Mapped["sqa_Interview" | None] = relationship("sqa_Interview", back_populates="feedback")


class sqa_DecisionLog(Base):
    """
    ORM model for the 'decision_logs' table.

    Logs hiring decisions made for an application.
    """

    __tablename__ = "decision_logs"

    decision_log_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.application_id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="RESTRICT"))
    decision: Mapped[str] = mapped_column(Text)
    reason: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=text("STRFTIME('%Y-%m-%d %H:%M:%S', 'now')")
    )

    # Relationships
    application: Mapped["sqa_Application"] = relationship("sqa_Application", back_populates="decision_logs")
    user: Mapped["sqa_User"] = relationship("sqa_User", back_populates="decision_logs")