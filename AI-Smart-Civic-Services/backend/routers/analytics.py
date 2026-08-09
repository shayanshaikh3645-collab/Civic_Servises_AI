from fastapi import APIRouter, Depends, HTTPException, status
from database.session import get_db
from backend.analytics.dashboard import DashboardAnalytics
from backend.auth import get_current_active_user

router = APIRouter()


@router.get('/stats')
def get_dashboard_stats(db=Depends(get_db), current_user=Depends(get_current_active_user)):
    if current_user.role not in ('admin', 'staff'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Admin or staff access required')
    analytics = DashboardAnalytics(db)
    return analytics.summary()
