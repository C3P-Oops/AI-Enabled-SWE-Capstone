PRAGMA foreign_keys = ON;
INSERT INTO users (user_id, first_name, last_name, email, role, created_at, updated_at) VALUES
(1, 'Eleanor', 'Vance', 'eleanor.vance@smarthire.tech', 'HR Manager', '2025-01-10 09:00:00', '2025-01-10 09:00:00'),
(2, 'Ben', 'Carter', 'ben.carter@smarthire.tech', 'Recruitment Coordinator', '2025-01-10 09:05:00', '2025-01-10 09:05:00'),
(3, 'Marcus', 'Cole', 'marcus.cole@smarthire.tech', 'Hiring Manager', '2025-01-11 10:20:00', '2025-01-11 10:20:00'),
(4, 'Isabelle', 'Rossi', 'isabelle.rossi@smarthire.tech', 'Hiring Manager', '2025-01-11 11:00:00', '2025-01-11 11:00:00'),
(5, 'Leo', 'Chang', 'leo.chang@smarthire.tech', 'Hiring Manager', '2025-01-12 14:00:00', '2025-01-12 14:00:00'),
(6, 'Samantha', 'Jones', 'samantha.jones@smarthire.tech', 'Project Manager', '2025-02-01 16:00:00', '2025-02-01 16:00:00'),
(7, 'Olivia', 'Chen', 'olivia.chen@smarthire.tech', 'Hiring Manager', '2025-05-01 09:30:00', '2025-05-01 09:30:00'),
(8, 'Noah', 'Patel', 'noah.patel@smarthire.tech', 'Project Manager', '2025-05-02 11:00:00', '2025-05-02 11:00:00');
INSERT INTO jobs (job_id, title, description, department, location, status, created_by_user_id, hiring_manager_user_id, created_at, updated_at) VALUES
(1, 'Senior Backend Engineer', 'Responsible for designing, developing, and maintaining our server-side logic, APIs, and microservices architecture using Go and Kubernetes.', 'Engineering', 'Remote', 'closed', 3, 3, '2025-03-01 10:00:00', '2025-04-15 11:00:00'),
(2, 'Lead Product Manager', 'Define the product vision, strategy, and roadmap for our new AI-driven analytics platform. Work with cross-functional teams to deliver exceptional products.', 'Product', 'San Francisco, CA', 'closed', 4, 4, '2025-03-05 14:00:00', '2025-04-20 09:30:00'),
(3, 'Frontend Developer', 'Build and maintain responsive, high-performance user interfaces for our web applications using React, TypeScript, and modern web technologies.', 'Engineering', 'New York, NY', 'open', 3, 3, '2025-04-10 16:30:00', '2025-04-10 16:30:00'),
(4, 'Cloud Security Engineer', 'Design and implement security solutions for our AWS cloud infrastructure. Focus on automation, compliance, and threat detection.', 'Engineering', 'Remote', 'open', 5, 5, '2025-04-12 11:00:00', '2025-04-12 11:00:00'),
(5, 'Data Scientist', 'Analyze large, complex datasets to extract meaningful insights, build predictive models, and inform business strategy.', 'Data & Analytics', 'Austin, TX', 'open', 7, 7, '2025-05-05 10:00:00', '2025-05-05 10:00:00');
INSERT INTO candidates (candidate_id, first_name, last_name, email, phone, created_at, updated_at) VALUES
(1, 'Alice', 'Williams', 'alice.w@example.net', '555-0111', '2025-03-10 08:00:00', '2025-03-10 08:00:00'),
(2, 'Brian', 'Miller', 'brian.m@example.net', '555-0112', '2025-03-11 12:30:00', '2025-03-11 12:30:00'),
(3, 'Chloe', 'Davis', 'chloe.d@example.net', '555-0113', '2025-03-12 15:00:00', '2025-03-12 15:00:00'),
(4, 'David', 'Garcia', 'david.g@example.net', '555-0114', '2025-03-14 09:45:00', '2025-03-14 09:45:00'),
(5, 'Eva', 'Rodriguez', 'eva.r@example.net', '555-0115', '2025-04-15 10:00:00', '2025-04-15 10:00:00'),
(6, 'Frank', 'Wilson', 'frank.w@example.net', '555-0116', '2025-04-16 11:20:00', '2025-04-16 11:20:00'),
(7, 'Grace', 'Moore', 'grace.m@example.net', '555-0117', '2025-05-06 14:00:00', '2025-05-06 14:00:00'),
(8, 'Henry', 'Taylor', 'henry.t@example.net', '555-0118', '2025-05-07 16:10:00', '2025-05-07 16:10:00');
INSERT INTO skills (skill_id, name) VALUES
(1, 'Go'),
(2, 'Kubernetes'),
(3, 'Microservices'),
(4, 'Product Strategy'),
(5, 'Agile Methodologies'),
(6, 'User Research'),
(7, 'React'),
(8, 'TypeScript'),
(9, 'AWS'),
(10, 'Terraform'),
(11, 'Python'),
(12, 'Machine Learning'),
(13, 'SQL');
INSERT INTO candidate_skills (candidate_id, skill_id) VALUES
(1, 1), (1, 2), (1, 3),
(2, 1), (2, 11),
(3, 4), (3, 5), (3, 6),
(4, 4), (4, 5),
(5, 7), (5, 8),
(6, 9), (6, 10),
(7, 11), (7, 12), (7, 13),
(8, 11), (8, 12);
INSERT INTO applications (application_id, job_id, candidate_id, status, applied_at, updated_at) VALUES
(1, 1, 1, 'hired', '2025-03-10 08:00:00', '2025-04-15 10:55:00'),
(2, 1, 2, 'rejected', '2025-03-11 12:30:00', '2025-03-25 17:00:00'),
(3, 2, 3, 'hired', '2025-03-12 15:00:00', '2025-04-20 09:25:00'),
(4, 2, 4, 'withdrawn', '2025-03-14 09:45:00', '2025-04-02 12:00:00'),
(5, 3, 5, 'interviewing', '2025-04-15 10:00:00', '2025-04-22 11:00:00'),
(6, 4, 6, 'screening', '2025-04-16 11:20:00', '2025-04-17 14:00:00'),
(7, 5, 7, 'screening', '2025-05-06 14:00:00', '2025-05-08 09:00:00'),
(8, 5, 8, 'applied', '2025-05-07 16:10:00', '2025-05-07 16:10:00');
INSERT INTO documents (document_id, application_id, type, file_path, uploaded_at) VALUES
(1, 1, 'resume', '/uploads/resumes/alice_williams_backend_2025.pdf', '2025-03-10 08:00:00'),
(2, 2, 'resume', '/uploads/resumes/brian_miller_backend_2025.pdf', '2025-03-11 12:30:00'),
(3, 3, 'resume', '/uploads/resumes/chloe_davis_pm_2025.pdf', '2025-03-12 15:00:00'),
(4, 3, 'cover_letter', '/uploads/cover_letters/chloe_davis_pm_2025.pdf', '2025-03-12 15:01:00'),
(5, 4, 'resume', '/uploads/resumes/david_garcia_pm_2025.pdf', '2025-03-14 09:45:00'),
(6, 5, 'resume', '/uploads/resumes/eva_rodriguez_frontend_2025.pdf', '2025-04-15 10:00:00'),
(7, 5, 'portfolio', '/uploads/portfolios/eva_rodriguez_web.url', '2025-04-15 10:01:00'),
(8, 6, 'resume', '/uploads/resumes/frank_wilson_security_2025.pdf', '2025-04-16 11:20:00'),
(9, 7, 'resume', '/uploads/resumes/grace_moore_datasci_2025.pdf', '2025-05-06 14:00:00'),
(10, 8, 'resume', '/uploads/resumes/henry_taylor_datasci_2025.pdf', '2025-05-07 16:10:00');
-- COMMENT: The tables 'interviews', 'interview_participants', 'feedback', and 'decision_logs' were not populated. According to the Product Requirements Document (PRD), these features are scheduled for versions 1.1 and 2.0. The current request is to generate seed data for version 1.0 (MVP) only, which includes core applicant data management.
-- COMMENT: The prompt requested seed data for an onboarding system, including tables like 'onboarding_workflows', 'tasks', and 'user_onboarding_progress'. However, these tables are not present in the provided SQLite schema. Furthermore, the PRD for version 1.0 explicitly states that "Comprehensive onboarding workflow management" is out of scope. Therefore, no onboarding data has been generated as it would violate the provided schema and product requirements for V1.0.
-- COMMENT: The schema does not include a 'teams' table. A logical enhancement would be to add a 'teams' table and a foreign key in the 'users' table to associate users with specific teams (e.g., Engineering, Product), which would allow for more granular permissions and reporting.