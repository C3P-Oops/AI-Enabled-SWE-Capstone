PRAGMA foreign_keys = ON;

-- Insert users (hiring managers and HR staff)
INSERT INTO users (user_id, first_name, last_name, email, role, created_at, updated_at) VALUES
(1, 'Eleanor', 'Vance', 'eleanor.vance@smarthire.tech', 'HR Manager', '2025-01-10 09:00:00', '2025-01-10 09:00:00'),
(2, 'Ben', 'Carter', 'ben.carter@smarthire.tech', 'Recruitment Coordinator', '2025-01-10 09:05:00', '2025-01-10 09:05:00'),
(3, 'Marcus', 'Cole', 'marcus.cole@smarthire.tech', 'Hiring Manager', '2025-01-11 10:20:00', '2025-01-11 10:20:00'),
(4, 'Isabelle', 'Rossi', 'isabelle.rossi@smarthire.tech', 'Hiring Manager', '2025-01-11 11:00:00', '2025-01-11 11:00:00'),
(5, 'Leo', 'Chang', 'leo.chang@smarthire.tech', 'Hiring Manager', '2025-01-12 14:00:00', '2025-01-12 14:00:00'),
(6, 'Samantha', 'Jones', 'samantha.jones@smarthire.tech', 'Project Manager', '2025-02-01 16:00:00', '2025-02-01 16:00:00'),
(7, 'Olivia', 'Chen', 'olivia.chen@smarthire.tech', 'Hiring Manager', '2025-05-01 09:30:00', '2025-05-01 09:30:00'),
(8, 'Noah', 'Patel', 'noah.patel@smarthire.tech', 'Project Manager', '2025-05-02 11:00:00', '2025-05-02 11:00:00');
-- Insert jobs (15 diverse positions across departments)
INSERT INTO jobs (job_id, title, description, department, location, status, created_by_user_id, hiring_manager_user_id, created_at, updated_at) VALUES
(1, 'Senior Software Engineer', 'We are looking for an experienced Senior Software Engineer to join our growing development team. You will be responsible for designing, developing, and maintaining scalable web applications using modern technologies. The ideal candidate has 5+ years of experience with full-stack development, strong problem-solving skills, and experience with cloud platforms.', 'Engineering', 'San Francisco, CA', 'open', 3, 3, '2025-01-15 09:00:00', '2025-01-15 09:00:00'),
(2, 'Product Manager', 'Join our product team as a Product Manager where you will drive the product strategy and roadmap for our core platform. You will work closely with engineering, design, and business stakeholders to deliver features that delight our customers. We are looking for someone with 3+ years of product management experience and strong analytical skills.', 'Product', 'New York, NY', 'open', 4, 4, '2025-01-20 10:30:00', '2025-01-20 10:30:00'),
(3, 'UX Designer', 'We are seeking a talented UX Designer to help create intuitive and engaging user experiences for our products. You will be responsible for user research, wireframing, prototyping, and working closely with our development team. The ideal candidate has a strong portfolio showcasing user-centered design principles and 2+ years of experience.', 'Design', 'Remote', 'open', 5, 5, '2025-02-01 14:00:00', '2025-02-01 14:00:00'),
(4, 'Data Scientist', 'Looking for a Data Scientist to join our analytics team. You will work with large datasets to extract insights, build predictive models, and help drive data-informed decisions across the organization. Strong skills in Python, SQL, and machine learning are required, along with 3+ years of experience in a similar role.', 'Data & Analytics', 'Austin, TX', 'open', 7, 7, '2025-02-10 11:00:00', '2025-02-10 11:00:00'),
(5, 'Marketing Coordinator', 'Join our marketing team as a Marketing Coordinator where you will support various marketing campaigns and initiatives. You will help with content creation, social media management, event coordination, and campaign analysis. We are looking for a creative individual with 1-2 years of marketing experience and strong communication skills.', 'Marketing', 'Los Angeles, CA', 'open', 1, 1, '2025-02-15 13:30:00', '2025-02-15 13:30:00'),
(6, 'DevOps Engineer', 'We are looking for a DevOps Engineer to help build and maintain our cloud infrastructure. You will work on CI/CD pipelines, monitoring systems, and automation tools. The ideal candidate has experience with AWS, Docker, Kubernetes, and infrastructure as code tools like Terraform.', 'Engineering', 'Seattle, WA', 'open', 3, 3, '2025-03-01 09:15:00', '2025-03-01 09:15:00'),
(7, 'Frontend Developer', 'Join our frontend team to build beautiful and responsive user interfaces. You will work with React, TypeScript, and modern CSS frameworks to create exceptional user experiences. We are looking for someone with 2+ years of frontend development experience and a passion for user interface design.', 'Engineering', 'Boston, MA', 'open', 3, 3, '2025-03-05 10:45:00', '2025-03-05 10:45:00'),
(8, 'Sales Representative', 'We are seeking a motivated Sales Representative to join our growing sales team. You will be responsible for generating leads, conducting product demos, and closing deals with potential customers. The ideal candidate has 2+ years of B2B sales experience and excellent communication skills.', 'Sales', 'Chicago, IL', 'open', 2, 2, '2025-03-10 08:30:00', '2025-03-10 08:30:00'),
(9, 'QA Engineer', 'Looking for a QA Engineer to ensure the quality of our software products. You will design and execute test plans, automate testing processes, and work closely with the development team to identify and resolve issues. Experience with automated testing tools and frameworks is preferred.', 'Engineering', 'Denver, CO', 'open', 3, 3, '2025-03-15 12:00:00', '2025-03-15 12:00:00'),
(10, 'Business Analyst', 'Join our business analysis team where you will work with stakeholders to gather requirements, analyze business processes, and help drive strategic decisions. The ideal candidate has strong analytical skills, experience with data analysis tools, and 2+ years of business analysis experience.', 'Operations', 'Atlanta, GA', 'open', 4, 4, '2025-03-20 15:20:00', '2025-03-20 15:20:00'),
(11, 'Mobile Developer', 'We are looking for a Mobile Developer to build and maintain our iOS and Android applications. You will work with React Native or native development frameworks to create high-quality mobile experiences. Experience with mobile app development and app store deployment is required.', 'Engineering', 'San Diego, CA', 'open', 5, 5, '2025-03-25 11:30:00', '2025-03-25 11:30:00'),
(12, 'Cybersecurity Specialist', 'Join our security team as a Cybersecurity Specialist where you will help protect our systems and data. You will conduct security assessments, implement security controls, and respond to security incidents. The ideal candidate has experience with security frameworks and 3+ years of cybersecurity experience.', 'IT Security', 'Washington, DC', 'open', 6, 6, '2025-04-01 09:45:00', '2025-04-01 09:45:00'),
(13, 'HR Generalist', 'We are seeking an HR Generalist to support our growing team. You will handle recruitment, employee relations, benefits administration, and HR policy development. The ideal candidate has 2+ years of HR experience and strong interpersonal skills.', 'Human Resources', 'Phoenix, AZ', 'open', 1, 1, '2025-04-05 14:15:00', '2025-04-05 14:15:00'),
(14, 'Technical Writer', 'Looking for a Technical Writer to create and maintain documentation for our products and APIs. You will work with engineering teams to document features, write user guides, and maintain technical knowledge bases. Strong writing skills and technical background are required.', 'Documentation', 'Portland, OR', 'open', 7, 7, '2025-04-10 10:00:00', '2025-04-10 10:00:00'),
(15, 'Cloud Architect', 'We are looking for a Cloud Architect to design and implement our cloud infrastructure strategy. You will work on system architecture, cloud migration projects, and help establish best practices for cloud deployment. The ideal candidate has 5+ years of cloud architecture experience with major cloud providers.', 'Engineering', 'Remote', 'open', 8, 8, '2025-04-15 16:30:00', '2025-04-15 16:30:00');
-- Insert candidates (20 diverse candidates with varied backgrounds)
INSERT INTO candidates (candidate_id, first_name, last_name, email, phone, created_at, updated_at) VALUES
(1, 'Alice', 'Johnson', 'alice.johnson@email.com', '555-0101', '2025-01-10 08:00:00', '2025-01-10 08:00:00'),
(2, 'Bob', 'Smith', 'bob.smith@email.com', '555-0102', '2025-01-11 09:30:00', '2025-01-11 09:30:00'),
(3, 'Carol', 'Davis', 'carol.davis@email.com', '555-0103', '2025-01-12 10:15:00', '2025-01-12 10:15:00'),
(4, 'David', 'Wilson', 'david.wilson@email.com', '555-0104', '2025-01-13 11:45:00', '2025-01-13 11:45:00'),
(5, 'Emma', 'Brown', 'emma.brown@email.com', '555-0105', '2025-01-14 13:20:00', '2025-01-14 13:20:00'),
(6, 'Frank', 'Miller', 'frank.miller@email.com', '555-0106', '2025-01-15 14:30:00', '2025-01-15 14:30:00'),
(7, 'Grace', 'Taylor', 'grace.taylor@email.com', '555-0107', '2025-01-16 15:45:00', '2025-01-16 15:45:00'),
(8, 'Henry', 'Anderson', 'henry.anderson@email.com', '555-0108', '2025-01-17 16:20:00', '2025-01-17 16:20:00'),
(9, 'Iris', 'Thomas', 'iris.thomas@email.com', '555-0109', '2025-01-18 17:10:00', '2025-01-18 17:10:00'),
(10, 'Jack', 'Martinez', 'jack.martinez@email.com', '555-0110', '2025-01-19 18:00:00', '2025-01-19 18:00:00'),
(11, 'Kate', 'Garcia', 'kate.garcia@email.com', '555-0111', '2025-01-20 08:30:00', '2025-01-20 08:30:00'),
(12, 'Liam', 'Rodriguez', 'liam.rodriguez@email.com', '555-0112', '2025-01-21 09:45:00', '2025-01-21 09:45:00'),
(13, 'Mia', 'Lewis', 'mia.lewis@email.com', '555-0113', '2025-01-22 10:20:00', '2025-01-22 10:20:00'),
(14, 'Noah', 'Walker', 'noah.walker@email.com', '555-0114', '2025-01-23 11:15:00', '2025-01-23 11:15:00'),
(15, 'Olivia', 'Hall', 'olivia.hall@email.com', '555-0115', '2025-01-24 12:30:00', '2025-01-24 12:30:00'),
(16, 'Paul', 'Young', 'paul.young@email.com', '555-0116', '2025-01-25 13:45:00', '2025-01-25 13:45:00'),
(17, 'Quinn', 'King', 'quinn.king@email.com', '555-0117', '2025-01-26 14:20:00', '2025-01-26 14:20:00'),
(18, 'Rachel', 'Wright', 'rachel.wright@email.com', '555-0118', '2025-01-27 15:35:00', '2025-01-27 15:35:00'),
(19, 'Sam', 'Lopez', 'sam.lopez@email.com', '555-0119', '2025-01-28 16:10:00', '2025-01-28 16:10:00'),
(20, 'Tara', 'Hill', 'tara.hill@email.com', '555-0120', '2025-01-29 17:25:00', '2025-01-29 17:25:00');
-- Insert skills (comprehensive skill set for various roles)
INSERT INTO skills (skill_id, name) VALUES
(1, 'Python'),
(2, 'JavaScript'),
(3, 'React'),
(4, 'Node.js'),
(5, 'SQL'),
(6, 'AWS'),
(7, 'Docker'),
(8, 'Kubernetes'),
(9, 'Git'),
(10, 'Agile'),
(11, 'Product Management'),
(12, 'UI/UX Design'),
(13, 'Machine Learning'),
(14, 'Data Analysis'),
(15, 'Java'),
(16, 'C++'),
(17, 'TypeScript'),
(18, 'Vue.js'),
(19, 'Angular'),
(20, 'DevOps'),
(21, 'Terraform'),
(22, 'Jenkins'),
(23, 'MongoDB'),
(24, 'PostgreSQL'),
(25, 'Redis'),
(26, 'Elasticsearch'),
(27, 'GraphQL'),
(28, 'REST APIs'),
(29, 'Microservices'),
(30, 'System Design');
-- Insert candidate skills (mapping candidates to their skills)
INSERT INTO candidate_skills (candidate_id, skill_id) VALUES
-- Alice Johnson - Full Stack Developer
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 9),
-- Bob Smith - Backend Engineer  
(2, 1), (2, 4), (2, 5), (2, 6), (2, 7), (2, 29),
-- Carol Davis - Product Manager
(3, 10), (3, 11), (3, 5), (3, 14),
-- David Wilson - DevOps Engineer
(4, 6), (4, 7), (4, 8), (4, 20), (4, 21), (4, 22),
-- Emma Brown - Frontend Developer
(5, 2), (5, 3), (5, 17), (5, 18), (5, 9),
-- Frank Miller - Data Scientist
(6, 1), (6, 13), (6, 14), (6, 5), (6, 26),
-- Grace Taylor - UX Designer
(7, 12), (7, 2), (7, 3),
-- Henry Anderson - QA Engineer
(8, 1), (8, 2), (8, 9), (8, 10),
-- Iris Thomas - Marketing Coordinator
(9, 14), (9, 11),
-- Jack Martinez - Sales Representative
(10, 11),
-- Kate Garcia - Mobile Developer
(11, 15), (11, 2), (11, 3), (11, 9),
-- Liam Rodriguez - Cybersecurity Specialist
(12, 1), (12, 6), (12, 20), (12, 7),
-- Mia Lewis - HR Generalist
(13, 11), (13, 10),
-- Noah Walker - Technical Writer
(14, 1), (14, 2), (14, 28),
-- Olivia Hall - Cloud Architect
(15, 6), (15, 7), (15, 8), (15, 21), (15, 30),
-- Paul Young - Business Analyst
(16, 5), (16, 14), (16, 10), (16, 11),
-- Quinn King - Software Engineer
(17, 1), (17, 15), (17, 16), (17, 5), (17, 9),
-- Rachel Wright - Frontend Developer
(18, 2), (18, 3), (18, 17), (18, 19), (18, 9),
-- Sam Lopez - Backend Engineer
(19, 1), (19, 4), (19, 5), (19, 23), (19, 24), (19, 27),
-- Tara Hill - Product Manager
(20, 10), (20, 11), (20, 5), (20, 14), (20, 9);
-- Insert applications (candidates applying to jobs with diverse statuses)
INSERT INTO applications (application_id, job_id, candidate_id, status, applied_at, updated_at) VALUES
-- Senior Software Engineer (Job 1) - 8 applications
(1, 1, 1, 'applied', '2025-01-16 09:00:00', '2025-01-16 09:00:00'),
(2, 1, 2, 'screening', '2025-01-17 10:30:00', '2025-01-18 14:00:00'),
(3, 1, 3, 'interviewing', '2025-01-18 11:15:00', '2025-01-22 16:30:00'),
(4, 1, 4, 'offer_extended', '2025-01-19 14:45:00', '2025-01-25 10:00:00'),
(5, 1, 5, 'hired', '2025-01-20 16:20:00', '2025-01-28 11:30:00'),
(6, 1, 6, 'rejected', '2025-01-21 08:30:00', '2025-01-24 09:15:00'),
(7, 1, 7, 'withdrawn', '2025-01-22 12:45:00', '2025-01-23 15:20:00'),
(8, 1, 8, 'applied', '2025-01-23 15:30:00', '2025-01-23 15:30:00'),

-- Product Manager (Job 2) - 6 applications
(9, 2, 9, 'applied', '2025-01-21 09:15:00', '2025-01-21 09:15:00'),
(10, 2, 10, 'screening', '2025-01-22 11:30:00', '2025-01-23 13:45:00'),
(11, 2, 11, 'interviewing', '2025-01-23 13:20:00', '2025-01-26 10:15:00'),
(12, 2, 12, 'offer_extended', '2025-01-24 15:45:00', '2025-01-29 14:30:00'),
(13, 2, 13, 'rejected', '2025-01-25 10:20:00', '2025-01-27 16:00:00'),
(14, 2, 14, 'hired', '2025-01-26 12:30:00', '2025-01-30 09:45:00'),

-- UX Designer (Job 3) - 5 applications
(15, 3, 15, 'applied', '2025-02-02 08:45:00', '2025-02-02 08:45:00'),
(16, 3, 16, 'screening', '2025-02-03 10:20:00', '2025-02-04 11:30:00'),
(17, 3, 17, 'interviewing', '2025-02-04 14:15:00', '2025-02-07 15:45:00'),
(18, 3, 18, 'rejected', '2025-02-05 16:30:00', '2025-02-08 09:20:00'),
(19, 3, 19, 'applied', '2025-02-06 11:45:00', '2025-02-06 11:45:00'),

-- Data Scientist (Job 4) - 4 applications
(20, 4, 20, 'applied', '2025-02-11 09:30:00', '2025-02-11 09:30:00'),
(21, 4, 1, 'screening', '2025-02-12 13:15:00', '2025-02-13 10:45:00'),
(22, 4, 3, 'interviewing', '2025-02-13 15:20:00', '2025-02-16 14:30:00'),
(23, 4, 5, 'rejected', '2025-02-14 11:10:00', '2025-02-17 16:15:00'),

-- Marketing Coordinator (Job 5) - 3 applications
(24, 5, 7, 'applied', '2025-02-16 10:45:00', '2025-02-16 10:45:00'),
(25, 5, 9, 'screening', '2025-02-17 14:20:00', '2025-02-18 11:30:00'),
(26, 5, 11, 'hired', '2025-02-18 16:35:00', '2025-02-22 09:15:00'),

-- DevOps Engineer (Job 6) - 7 applications
(27, 6, 2, 'applied', '2025-03-02 08:20:00', '2025-03-02 08:20:00'),
(28, 6, 4, 'applied', '2025-03-03 10:15:00', '2025-03-03 10:15:00'),
(29, 6, 6, 'screening', '2025-03-04 12:30:00', '2025-03-05 14:45:00'),
(30, 6, 8, 'interviewing', '2025-03-05 15:45:00', '2025-03-08 11:20:00'),
(31, 6, 10, 'interviewing', '2025-03-06 09:30:00', '2025-03-09 16:15:00'),
(32, 6, 12, 'offer_extended', '2025-03-07 13:20:00', '2025-03-12 10:30:00'),
(33, 6, 14, 'rejected', '2025-03-08 16:45:00', '2025-03-11 14:20:00'),

-- Frontend Developer (Job 7) - 6 applications
(34, 7, 13, 'applied', '2025-03-06 11:15:00', '2025-03-06 11:15:00'),
(35, 7, 15, 'screening', '2025-03-07 14:30:00', '2025-03-08 09:45:00'),
(36, 7, 17, 'interviewing', '2025-03-08 16:20:00', '2025-03-11 13:30:00'),
(37, 7, 19, 'rejected', '2025-03-09 10:45:00', '2025-03-12 15:15:00'),
(38, 7, 1, 'withdrawn', '2025-03-10 13:30:00', '2025-03-11 10:20:00'),
(39, 7, 3, 'applied', '2025-03-11 15:45:00', '2025-03-11 15:45:00'),

-- Sales Representative (Job 8) - 4 applications
(40, 8, 16, 'applied', '2025-03-11 09:20:00', '2025-03-11 09:20:00'),
(41, 8, 18, 'screening', '2025-03-12 11:45:00', '2025-03-13 14:30:00'),
(42, 8, 20, 'interviewing', '2025-03-13 13:15:00', '2025-03-16 10:45:00'),
(43, 8, 2, 'hired', '2025-03-14 15:30:00', '2025-03-18 11:20:00'),

-- QA Engineer (Job 9) - 5 applications
(44, 9, 4, 'applied', '2025-03-16 08:45:00', '2025-03-16 08:45:00'),
(45, 9, 6, 'applied', '2025-03-17 10:30:00', '2025-03-17 10:30:00'),
(46, 9, 8, 'screening', '2025-03-18 12:15:00', '2025-03-19 14:20:00'),
(47, 9, 10, 'interviewing', '2025-03-19 14:45:00', '2025-03-22 16:30:00'),
(48, 9, 12, 'rejected', '2025-03-20 16:20:00', '2025-03-23 09:15:00'),

-- Business Analyst (Job 10) - 3 applications
(49, 10, 14, 'applied', '2025-03-21 11:30:00', '2025-03-21 11:30:00'),
(50, 10, 16, 'screening', '2025-03-22 13:45:00', '2025-03-23 15:20:00'),
(51, 10, 18, 'offer_extended', '2025-03-23 15:15:00', '2025-03-27 10:45:00'),

-- Mobile Developer (Job 11) - 6 applications
(52, 11, 5, 'applied', '2025-03-26 09:45:00', '2025-03-26 09:45:00'),
(53, 11, 7, 'screening', '2025-03-27 11:20:00', '2025-03-28 13:30:00'),
(54, 11, 9, 'interviewing', '2025-03-28 14:15:00', '2025-03-31 10:20:00'),
(55, 11, 11, 'interviewing', '2025-03-29 16:30:00', '2025-04-01 14:45:00'),
(56, 11, 13, 'rejected', '2025-03-30 10:15:00', '2025-04-02 11:30:00'),
(57, 11, 15, 'hired', '2025-03-31 12:45:00', '2025-04-04 09:20:00'),

-- Cybersecurity Specialist (Job 12) - 2 applications
(58, 12, 17, 'applied', '2025-04-02 13:30:00', '2025-04-02 13:30:00'),
(59, 12, 19, 'screening', '2025-04-03 15:45:00', '2025-04-04 11:15:00'),

-- HR Generalist (Job 13) - 4 applications
(60, 13, 1, 'applied', '2025-04-06 10:20:00', '2025-04-06 10:20:00'),
(61, 13, 20, 'screening', '2025-04-07 12:15:00', '2025-04-08 14:30:00'),
(62, 13, 2, 'interviewing', '2025-04-08 14:45:00', '2025-04-11 16:20:00'),
(63, 13, 4, 'rejected', '2025-04-09 16:30:00', '2025-04-12 09:45:00'),

-- Technical Writer (Job 14) - 3 applications
(64, 14, 6, 'applied', '2025-04-11 11:45:00', '2025-04-11 11:45:00'),
(65, 14, 8, 'applied', '2025-04-12 13:20:00', '2025-04-12 13:20:00'),
(66, 14, 10, 'hired', '2025-04-13 15:30:00', '2025-04-17 10:15:00'),

-- Cloud Architect (Job 15) - 1 application (new posting)
(67, 15, 12, 'applied', '2025-04-16 09:30:00', '2025-04-16 09:30:00');
-- Insert documents (resumes and cover letters for applications)
INSERT INTO documents (document_id, application_id, type, file_path, uploaded_at) VALUES
-- Documents for Senior Software Engineer applications
(1, 1, 'resume', '/uploads/resumes/alice_johnson_resume.pdf', '2025-01-16 09:00:00'),
(2, 2, 'resume', '/uploads/resumes/bob_smith_resume.pdf', '2025-01-17 10:30:00'),
(3, 3, 'resume', '/uploads/resumes/carol_davis_resume.pdf', '2025-01-18 11:15:00'),
(4, 3, 'cover_letter', '/uploads/cover_letters/carol_davis_cover_letter.pdf', '2025-01-18 11:16:00'),
(5, 4, 'resume', '/uploads/resumes/david_wilson_resume.pdf', '2025-01-19 14:45:00'),
(6, 5, 'resume', '/uploads/resumes/emma_brown_resume.pdf', '2025-01-20 16:20:00'),
(7, 5, 'portfolio', '/uploads/portfolios/emma_brown_portfolio.pdf', '2025-01-20 16:21:00'),
(8, 6, 'resume', '/uploads/resumes/frank_miller_resume.pdf', '2025-01-21 08:30:00'),
(9, 7, 'resume', '/uploads/resumes/grace_taylor_resume.pdf', '2025-01-22 12:45:00'),
(10, 8, 'resume', '/uploads/resumes/henry_anderson_resume.pdf', '2025-01-23 15:30:00'),

-- Documents for Product Manager applications
(11, 9, 'resume', '/uploads/resumes/iris_thomas_resume.pdf', '2025-01-21 09:15:00'),
(12, 10, 'resume', '/uploads/resumes/jack_martinez_resume.pdf', '2025-01-22 11:30:00'),
(13, 11, 'resume', '/uploads/resumes/kate_garcia_resume.pdf', '2025-01-23 13:20:00'),
(14, 12, 'resume', '/uploads/resumes/liam_rodriguez_resume.pdf', '2025-01-24 15:45:00'),
(15, 13, 'resume', '/uploads/resumes/mia_lewis_resume.pdf', '2025-01-25 10:20:00'),
(16, 14, 'resume', '/uploads/resumes/noah_walker_resume.pdf', '2025-01-26 12:30:00'),

-- Documents for UX Designer applications
(17, 15, 'resume', '/uploads/resumes/olivia_hall_resume.pdf', '2025-02-02 08:45:00'),
(18, 15, 'portfolio', '/uploads/portfolios/olivia_hall_portfolio.pdf', '2025-02-02 08:46:00'),
(19, 16, 'resume', '/uploads/resumes/paul_young_resume.pdf', '2025-02-03 10:20:00'),
(20, 17, 'resume', '/uploads/resumes/quinn_king_resume.pdf', '2025-02-04 14:15:00'),
(21, 18, 'resume', '/uploads/resumes/rachel_wright_resume.pdf', '2025-02-05 16:30:00'),
(22, 19, 'resume', '/uploads/resumes/sam_lopez_resume.pdf', '2025-02-06 11:45:00'),

-- Documents for Data Scientist applications
(23, 20, 'resume', '/uploads/resumes/tara_hill_resume.pdf', '2025-02-11 09:30:00'),
(24, 21, 'resume', '/uploads/resumes/alice_johnson_ds_resume.pdf', '2025-02-12 13:15:00'),
(25, 22, 'resume', '/uploads/resumes/carol_davis_ds_resume.pdf', '2025-02-13 15:20:00'),
(26, 23, 'resume', '/uploads/resumes/emma_brown_ds_resume.pdf', '2025-02-14 11:10:00'),

-- Additional documents for selected high-value applications
(27, 26, 'resume', '/uploads/resumes/kate_garcia_marketing_resume.pdf', '2025-02-18 16:35:00'),
(28, 32, 'resume', '/uploads/resumes/liam_rodriguez_devops_resume.pdf', '2025-03-07 13:20:00'),
(29, 36, 'resume', '/uploads/resumes/quinn_king_frontend_resume.pdf', '2025-03-08 16:20:00'),
(30, 43, 'resume', '/uploads/resumes/bob_smith_sales_resume.pdf', '2025-03-14 15:30:00'),
(31, 51, 'resume', '/uploads/resumes/rachel_wright_ba_resume.pdf', '2025-03-23 15:15:00'),
(32, 57, 'resume', '/uploads/resumes/olivia_hall_mobile_resume.pdf', '2025-03-31 12:45:00'),
(33, 66, 'resume', '/uploads/resumes/jack_martinez_writer_resume.pdf', '2025-04-13 15:30:00'),
(34, 67, 'resume', '/uploads/resumes/liam_rodriguez_cloud_resume.pdf', '2025-04-16 09:30:00');
-- COMMENT: Database seeded with comprehensive test data for recruitment system MVP v1.0
-- COMMENT: Includes 15 diverse job positions across multiple departments and locations
-- COMMENT: Contains 20 candidates with varied skill sets and backgrounds
-- COMMENT: Features 67 applications with realistic status distribution across all hiring stages
-- COMMENT: Tables 'interviews', 'interview_participants', 'feedback', and 'decision_logs' not populated
-- COMMENT: These advanced features are scheduled for versions 1.1 and 2.0 per PRD requirements
-- COMMENT: Current data supports full testing of core applicant tracking functionality