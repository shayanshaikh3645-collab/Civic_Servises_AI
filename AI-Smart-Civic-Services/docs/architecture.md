# AI Smart Civic Services Architecture

## Overview

The project is organized into independent frontend and backend components.

- `frontend/`: React + Vite app with Tailwind CSS for UI.
- `backend/`: FastAPI service with REST endpoints.
- `ai/`: Mock AI analysis service that determines category and priority.
- `database/`: SQLAlchemy models and PostgreSQL connection.

## Backend flow

1. Frontend submits a complaint to `POST /api/complaints`.
2. The backend validates request data with Pydantic models.
3. `ai/analysis.py` classifies the complaint category and priority.
4. The complaint is saved into PostgreSQL via SQLAlchemy.
5. `GET /api/complaints` returns stored complaints.

## Frontend flow

1. React form submits a complaint via Axios.
2. The frontend uses React Router for navigation.
3. The complaint list and detail views read from `/api/complaints`.
