-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- Table for system users (HR, Recruiters, Managers)
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL CHECK(role IN ('HR Manager', 'Recruitment Coordinator', 'Hiring Manager', 'Project Manager')),
    created_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%S', 'now'))
);

-- Table for job postings
CREATE TABLE jobs (
    job_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    department TEXT,
    location TEXT,
    status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'closed', 'draft')),
    created_by_user_id INTEGER NOT NULL,
    hiring_manager_user_id INTEGER,
    created_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%S', 'now')),
    FOREIGN KEY (created_by_user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    FOREIGN KEY (hiring_manager_user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- Table for candidates/applicants
CREATE TABLE candidates (
    candidate_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    created_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%S', 'now'))
);

-- Table for skills
CREATE TABLE skills (
    skill_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Junction table for the many-to-many relationship between candidates and skills
CREATE TABLE candidate_skills (
    candidate_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    PRIMARY KEY (candidate_id, skill_id),
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE
);

-- Table representing a single application from a candidate for a job
CREATE TABLE applications (
    application_id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL,
    candidate_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'applied' CHECK(status IN ('applied', 'screening', 'interviewing', 'offer_extended', 'hired', 'rejected', 'withdrawn')),
    applied_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%S', 'now')),
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE,
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    UNIQUE (job_id, candidate_id)
);

-- Table for documents associated with an application
CREATE TABLE documents (
    document_id INTEGER PRIMARY KEY,
    application_id INTEGER NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('resume', 'cover_letter', 'portfolio', 'other')),
    file_path TEXT NOT NULL UNIQUE,
    uploaded_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%S', 'now')),
    FOREIGN KEY (application_id) REFERENCES applications(application_id) ON DELETE CASCADE
);

-- Table for scheduled interviews
CREATE TABLE interviews (
    interview_id INTEGER PRIMARY KEY,
    application_id INTEGER NOT NULL,
    scheduled_by_user_id INTEGER NOT NULL,
    interview_stage TEXT NOT NULL,
    method TEXT NOT NULL CHECK (method IN ('Phone', 'Video', 'On-site')),
    location_or_link TEXT,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%S', 'now')),
    FOREIGN KEY (application_id) REFERENCES applications(application_id) ON DELETE CASCADE,
    FOREIGN KEY (scheduled_by_user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- Junction table for interview participants (many-to-many between interviews and users)
CREATE TABLE interview_participants (
    interview_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (interview_id, user_id),
    FOREIGN KEY (interview_id) REFERENCES interviews(interview_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Table for feedback on an application, possibly linked to an interview
CREATE TABLE feedback (
    feedback_id INTEGER PRIMARY KEY,
    application_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    interview_id INTEGER,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%S', 'now')),
    FOREIGN KEY (application_id) REFERENCES applications(application_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    FOREIGN KEY (interview_id) REFERENCES interviews(interview_id) ON DELETE SET NULL
);

-- Table for logging hiring decisions
CREATE TABLE decision_logs (
    decision_log_id INTEGER PRIMARY KEY,
    application_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    decision TEXT NOT NULL CHECK (decision IN ('move_to_next_stage', 'offer', 'no_offer', 'hire', 'reject', 'on_hold')),
    reason TEXT,
    created_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%S', 'now')),
    FOREIGN KEY (application_id) REFERENCES applications(application_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- Triggers to automatically update the 'updated_at' timestamp on row modification
CREATE TRIGGER update_users_updated_at
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = STRFTIME('%Y-%m-%d %H:%M:%S', 'now') WHERE user_id = OLD.user_id;
END;

CREATE TRIGGER update_jobs_updated_at
AFTER UPDATE ON jobs
FOR EACH ROW
BEGIN
    UPDATE jobs SET updated_at = STRFTIME('%Y-%m-%d %H:%M:%S', 'now') WHERE job_id = OLD.job_id;
END;

CREATE TRIGGER update_candidates_updated_at
AFTER UPDATE ON candidates
FOR EACH ROW
BEGIN
    UPDATE candidates SET updated_at = STRFTIME('%Y-%m-%d %H:%M:%S', 'now') WHERE candidate_id = OLD.candidate_id;
END;

CREATE TRIGGER update_applications_updated_at
AFTER UPDATE ON applications
FOR EACH ROW
BEGIN
    UPDATE applications SET updated_at = STRFTIME('%Y-%m-%d %H:%M:%S', 'now') WHERE application_id = OLD.application_id;
END;

CREATE TRIGGER update_interviews_updated_at
AFTER UPDATE ON interviews
FOR EACH ROW
BEGIN
    UPDATE interviews SET updated_at = STRFTIME('%Y-%m-%d %H:%M:%S', 'now') WHERE interview_id = OLD.interview_id;
END;