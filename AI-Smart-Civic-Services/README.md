# AI Smart Civic Services

AI Smart Civic Services is an end-to-end civic complaint and service-management application. Citizens submit local civic complaints, and the system uses AI to understand, classify, prioritize, and route complaints to the correct service department.

## Project structure

- `frontend/` - React + Vite web app with Tailwind CSS and React Router
- `backend/` - FastAPI service with complaint endpoints and a mock AI layer
- `ai/` - Modular AI analysis service for future LLM/API integration
- `database/` - SQLAlchemy models and PostgreSQL session configuration
- `docs/` - Documentation and architecture notes

## Getting started

### Backend

1. Create a Python virtual environment
   ```bash
   cd AI-Smart-Civic-Services\backend
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install backend dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the example environment file
   ```bash
   copy .env.example .env
   ```
4. Edit `backend/.env` and provide your PostgreSQL `DATABASE_URL`.
5. Start the backend API
   ```bash
   uvicorn app:app --reload --host 127.0.0.1 --port 8000
   ```

### Frontend

1. Install frontend dependencies
   ```bash
   cd ../frontend
   npm install
   ```
2. Copy the example environment file
   ```bash
   copy .env.example .env
   ```
3. Start the frontend
   ```bash
   npm run dev -- --host
   ```

## API Endpoints

- `GET /api/health` - health check
- `POST /api/auth/token` - login and receive JWT token
- `POST /api/auth/register` - citizen signup
- `GET /api/complaints/public` - latest public complaints
- `GET /api/complaints` - list complaints for current user / staff / admin
- `POST /api/complaints` - submit a complaint
- `GET /api/complaints/{id}` - complaint details
- `PATCH /api/complaints/{id}/assign` - admin assigns complaint
- `PATCH /api/complaints/{id}/status` - staff/admin updates status
- `GET /api/notifications` - current user notifications
- `GET /api/stats` - staff/admin dashboard metrics

## Notes

- The AI analysis service is mocked in `ai/analysis.py` so the app works without an API key.
- PostgreSQL connection settings are configured through `backend/.env`.
- Frontend and backend are independent and communicate over REST.
