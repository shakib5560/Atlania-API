# ⚡ Atlania — Backend (FastAPI)

[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

The high-performance core of Atlania. This backend provides the RESTful API endpoints required to power the Atlania frontend, handling everything from authentication to content management.

## 🚀 Key Features

- **Asynchronous Architecture**: Built on top of Starlette and Pydantic for maximum speed.
- **Auto-Generated Docs**: Interactive API documentation available via Swagger UI and ReDoc.
- **RESTful Endpoints**: Clean and structured routes for articles, users, and admin actions.
- **Secure Auth**: Ready for JWT-based authentication and role-based access control.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)

## ⚡ Getting Started

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Run Server
It is recommended to run the server from the **backend root** directory using the provided script:

```bash
./run.sh
```

Alternatively, you can run uvicorn directly (ensure you are in the `backend` directory):
```bash
uvicorn app.main:app --reload
```

---

<p align="center">
  Part of the <b>Atlania</b> Ecosystem
</p>
