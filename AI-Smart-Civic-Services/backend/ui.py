from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import func

from database.session import get_db
from database.models import Complaint

router = APIRouter()

TEMPLATES_DIR = Path(__file__).resolve().parent / 'templates'
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get('/ui')
def server_ui(request: Request, db=Depends(get_db)):
    """Simple server-rendered UI for quick preview (no Node required)."""
    complaints = (
        db.query(Complaint)
        .order_by(Complaint.created_at.desc())
        .limit(20)
        .all()
    )
    total = db.scalar(func.count(Complaint.id))
    return templates.TemplateResponse('index.html', {'request': request, 'complaints': complaints, 'total': total})
