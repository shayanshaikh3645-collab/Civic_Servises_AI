from .auth import router as auth_router
from .complaints import router as complaints_router
from .analytics import router as analytics_router

__all__ = ['auth_router', 'complaints_router', 'analytics_router']
