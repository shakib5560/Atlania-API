# ⚡ Atlania — Backend API

[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

The high-performance core of the **Atlania** ecosystem. This backend provides a robust RESTful API built with **FastAPI**, handling everything from secure authentication to complex content management interactions.

## 🚀 Key Features

- **⚡ High Performance**: Built on Starlette and Pydantic for asynchronous speed.
- **🔐 Secure Authentication**: 
    - Full **JWT-based** auth flow (login, register, refresh).
    - **Google OAuth2** integration for social login.
- **📝 Content Management**: 
    - CRUD operations for **Posts** and **Categories**.
    - Rich text and media support.
- **🖼️ Media Handling**: integrated **ImageKit** support for seamless image upgrades and serving.
- **👥 User Interaction**:
    - APIs for **Comments**, **Likes**, and other social interactions.
- **🛡️ Admin Dashboard**: Dedicated administrative endpoints for system management.
- **📄 Auto-Documentation**: Interactive API docs via Swagger UI (`/docs`) and ReDoc (`/redoc`).

## 🛠️ Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | Modern, fast (high-performance) web framework. |
| **Database** | [PostgreSQL](https://www.postgresql.org/) | Robust relational database. |
| **ORM** | [SQLAlchemy](https://www.sqlalchemy.org/) | Python SQL toolkit and ORM. |
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org/) | Database migration tool for SQLAlchemy. |
| **Validation** | [Pydantic](https://docs.pydantic.dev/) | Data validation using Python type hints. |
| **Server** | [Uvicorn](https://www.uvicorn.org/) | Lightning-fast ASGI server implementation. |
| **Auth** | [Python-Jose](https://github.com/mpdavis/python-jose) | JavaScript Object Signing and Encryption implementation. |

## 📂 Project Structure

```bash
backend/
├── app/
│   ├── api/            # API Route endpoints (v1)
│   ├── core/           # Config (Settings, Security)
│   ├── models/         # SQLAlchemy Database Models
│   ├── schemas/        # Pydantic Schemas (Request/Response)
│   ├── services/       # Business Logic & External Services
│   └── main.py         # Application Entry Point
├── alembic/            # Database Migrations
├── requirements.txt    # Project Dependencies
└── run.sh              # Server Startup Script
```

## ⚡ Getting Started

### 1. Prerequisites
- Python 3.9+
- PostgreSQL installed and running.

### 2. Installation
Clone the repository and install dependencies:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the `backend/` root (copied from `.env.example` if available) and set the following:

```ini
# Core
SECRET_KEY=your_secure_random_key
API_V1_STR=/api/v1
PROJECT_NAME="Atlania API"

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/atlania_db

# Security
ACCESS_TOKEN_EXPIRE_MINUTES=11520 # 8 days
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Optional: External Services
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
IMAGEKIT_PUBLIC_KEY=...
IMAGEKIT_PRIVATE_KEY=...
IMAGEKIT_URL_ENDPOINT=...
```

### 4. Database Setup
Apply database migrations to create schemas:

```bash
alembic upgrade head
```

### 5. Running the Server
You can start the server using the helper script:

```bash
./run.sh
```

Or manually via Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

## 📚 API Documentation

Once running, explore the interactive documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

<p align="center">
  Built with ❤️ by the Atlania DEV.SHAKIB
</p>
