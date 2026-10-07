# BhoomiScan

**Your AIvocate.**

AI-powered property due diligence platform.

Phase 1 builds the foundation: a dark royal-themed frontend, FastAPI backend, PostgreSQL, JWT authentication, property-case creation, and document upload. AI analysis, OCR, translation, risk detection, and blockchain are intentionally out of scope.

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (recommended for PostgreSQL) or a local PostgreSQL 16 instance

## PostgreSQL setup

From the project root:

```bash
docker compose up -d
```

This starts PostgreSQL on port `5432` with:

- database: `bhoomiscan`
- user: `bhoomiscan`
- password: `bhoomiscan`

If you prefer a local install, create a database and user that match `DATABASE_URL` in `.env`.

## Environment variables

Copy the examples (already created for local development):

```bash
copy .env.example .env
copy frontend\.env.example frontend\.env
```

Root `.env`:

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | SQLAlchemy URL (`postgresql+psycopg://...`) |
| `JWT_SECRET` | Secret used to sign access tokens |
| `JWT_ALGORITHM` | `HS256` |
| `JWT_EXPIRE_MINUTES` | Token lifetime (default 1440 = 24h) |
| `MAX_FILE_SIZE_MB` | Upload size limit |
| `CORS_ORIGINS` | Comma-separated frontend origins |

Frontend `.env`:

| Variable | Purpose |
| --- | --- |
| `VITE_API_URL` | Backend origin, e.g. `http://localhost:8000` |

Never put JWT secrets in the React app. Vite only exposes `VITE_*` values.

## Python setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Tables are created automatically on backend startup.

## Node setup

```bash
cd frontend
npm install
```

## Run the backend

From `backend/` with the virtual environment active:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

## Run the frontend

```bash
cd frontend
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

## Test commands

Backend (SQLite in-memory; PostgreSQL is not required for tests):

```bash
cd backend
.venv\Scripts\activate
pytest -q
```

Exercise the frontend journey manually:

1. Landing page → **Get Started**
2. Sign up with username + password
3. Login
4. Dashboard → **Start Analysis**
5. Select **Residential**
6. Choose a residential property type
7. Upload a PDF / PNG / JPG
8. Confirm the document appears as stored
9. **Analyze Document** should show: `AI analysis will be available after Phase 2.`

## Phase 1 user journey

Landing → Signup → Login → Dashboard → Property domain → Residential → Property type → Property case → Upload document → See stored file.

## API

| Method | Path | Auth |
| --- | --- | --- |
| `POST` | `/auth/signup` | No |
| `POST` | `/auth/login` | No |
| `GET` | `/auth/me` | JWT |
| `POST` | `/property-cases` | JWT |
| `GET` | `/property-cases` | JWT |
| `GET` | `/property-cases/{id}` | JWT |
| `POST` | `/property-cases/{id}/documents` | JWT |
| `GET` | `/property-cases/{id}/documents` | JWT |

Uploads are stored at `storage/documents/{property_case_id}/`. Only metadata is saved in PostgreSQL. Files are never executed.

Google, X, and phone login buttons are demo-only.
