# AI-Enabled SWE Capstone

## Overview
The AI-Enabled SWE Capstone project is a comprehensive application designed to streamline the hiring and recruitment process. It leverages FastAPI, SQLAlchemy, and SQLite to provide a high-performance API for managing users, jobs, candidates, and other recruitment-related entities.

## Features
- **FastAPI Framework**: High-performance API for CRUD operations.
- **SQLAlchemy ORM**: Database interaction with SQLite backend.
- **Pydantic Models**: Data validation and serialization.
- **Comprehensive Endpoints**: Manage users, jobs, candidates, applications, interviews, feedback, and decisions.
- **Database Constraints**: Proper handling of UNIQUE, FOREIGN KEY, and ON DELETE actions.
- **Dependency Injection**: Efficient database session management.
- **Extensive Documentation**: Auto-generated API docs with Swagger UI.

## Installation

### Prerequisites
- Python 3.11+
- SQLite
- Git

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/C3P-Oops/AI-Enabled-SWE-Capstone.git
   cd AI-Enabled-SWE-Capstone
   ```
2. Create and activate a virtual environment:
   ```bash
   project root>>> python -m venv .venv
   project root>>> source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```terminal
   project root>>> pip install -r requirements.txt
   ```
4. Install vite
   ```bash
   project root>>> npm create vite@latest app
   project root>>> cd app
   ```
5. Install `tailwindcss` and `@tailwindcss/vite` via npm
   ```bash
   project root\app>>> npm install tailwindcss @tailwindcss/vite
   ```


## Usage
- Access the API documentation at `http://127.0.0.1:8081/docs`.
- Use the provided endpoints to manage recruitment data.

## Project Structure
```
├── app/
│   ├── scripts/
│   │   ├── main.py          # Main FastAPI application
│   │   ├── database.py      # Database session setup
│   │   ├── models.py        # SQLAlchemy models
│   ├── public/              # Static assets
│   ├── src/                 # Frontend source code
├── notebooks/               # Jupyter notebooks for development
├── artifacts/               # Generated artifacts (e.g., schema, seed data)
├── utils/                   # Utility scripts
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore rules
├── readme.md                # Project documentation
```

## Contributing
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

## License
This project is not licensed for use, derivation, or the creation of derivative projects or products by anyone without the express permission of the developers.

## Acknowledgments
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)