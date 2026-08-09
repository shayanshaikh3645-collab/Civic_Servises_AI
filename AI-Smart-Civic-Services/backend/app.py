import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

load_dotenv(ROOT_DIR / 'backend' / '.env')

from database import models
from database.session import engine
from backend.routers import auth_router, complaints_router, analytics_router
from backend.ui import router as ui_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='AI Smart Civic Services API',
    description='Backend service for the civic complaint management application.',
    version='0.1.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:5173',
        'http://127.0.0.1:5173',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router, prefix='/api/auth')
app.include_router(complaints_router, prefix='/api')
app.include_router(analytics_router, prefix='/api')
app.include_router(ui_router, prefix='')

