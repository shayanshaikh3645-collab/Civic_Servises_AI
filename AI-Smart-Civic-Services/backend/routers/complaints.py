from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.schemas import (
    ComplaintCreate,
    ComplaintResponse,
    ComplaintAssignment,
    ComplaintStatusUpdate,
    DepartmentResponse,
    NotificationResponse,
)
from backend.services.complaint_service import ComplaintService
from database.models import Complaint, Department, Notification, ComplaintStatusHistory
from database.session import get_db
from backend.auth import get_current_active_user

router = APIRouter()


def get_complaint_or_404(db: Session, complaint_id: int):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Complaint not found')
    return complaint


@router.get('/health')
def health_check():
    return {'status': 'ok'}


@router.get('/complaints/public', response_model=list[ComplaintResponse])
def list_public_complaints(db: Session = Depends(get_db)):
    return (
        db.query(Complaint)
        .order_by(Complaint.updated_at.desc())
        .limit(12)
        .all()
    )


@router.get('/complaints', response_model=list[ComplaintResponse])
def list_complaints(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    if current_user.role == 'citizen':
        complaints = db.query(Complaint).filter(Complaint.citizen_id == current_user.id)
    elif current_user.role == 'staff':
        complaints = db.query(Complaint).filter(Complaint.assigned_staff_id == current_user.id)
    else:
        complaints = db.query(Complaint)
    return complaints.order_by(Complaint.created_at.desc()).all()


@router.post('/complaints', response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_complaint(payload: ComplaintCreate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    service = ComplaintService()
    complaint = service.create_complaint(current_user.id, payload.dict())
    service.close()
    return complaint


@router.get('/complaints/{complaint_id}', response_model=ComplaintResponse)
def get_complaint(complaint_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    complaint = get_complaint_or_404(db, complaint_id)
    if current_user.role == 'citizen' and complaint.citizen_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized')
    if current_user.role == 'staff' and complaint.assigned_staff_id != current_user.id and complaint.citizen_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized')
    return complaint


@router.patch('/complaints/{complaint_id}/assign', response_model=ComplaintResponse)
def assign_complaint(complaint_id: int, payload: ComplaintAssignment, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Admin access required')
    complaint = get_complaint_or_404(db, complaint_id)
    complaint.assigned_department_id = payload.assigned_department_id
    complaint.assigned_staff_id = payload.assigned_staff_id
    complaint.status = 'Assigned'
    complaint.updated_at = datetime.utcnow()

    status_history = ComplaintStatusHistory(
        complaint_id=complaint.id,
        status='Assigned',
        comment='Assigned by admin user',
        changed_by_id=current_user.id,
    )
    notification = Notification(
        user_id=complaint.citizen_id,
        complaint_id=complaint.id,
        message=f'Your complaint "{complaint.title}" has been assigned to the {complaint.assigned_department.name if complaint.assigned_department else "selected"} team.',
    )
    db.add_all([status_history, notification])
    db.commit()
    db.refresh(complaint)
    return complaint


@router.patch('/complaints/{complaint_id}/status', response_model=ComplaintResponse)
def update_complaint_status(complaint_id: int, payload: ComplaintStatusUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    complaint = get_complaint_or_404(db, complaint_id)
    if current_user.role == 'citizen':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Citizens cannot update complaint status')
    if current_user.role == 'staff' and complaint.assigned_staff_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized')

    complaint.status = payload.status
    complaint.updated_at = datetime.utcnow()
    if payload.status == 'Resolved':
        complaint.resolved_at = datetime.utcnow()

    history = ComplaintStatusHistory(
        complaint_id=complaint.id,
        status=payload.status,
        comment=payload.comment,
        changed_by_id=current_user.id,
    )
    notification = Notification(
        user_id=complaint.citizen_id,
        complaint_id=complaint.id,
        message=f'Your complaint "{complaint.title}" status changed to {payload.status}.',
    )
    db.add_all([history, notification])
    db.commit()
    db.refresh(complaint)
    return complaint


@router.get('/departments', response_model=list[DepartmentResponse])
def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).order_by(Department.name).all()


@router.get('/notifications', response_model=list[NotificationResponse])
def list_notifications(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )


@router.get('/stats')
def get_dashboard_stats(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    if current_user.role not in ('admin', 'staff'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Admin or staff access required')

    total = db.scalar(func.count(Complaint.id))
    by_status = {
        status: count
        for status, count in db.query(Complaint.status, func.count(Complaint.id)).group_by(Complaint.status).all()
    }
    by_category = {
        category: count
        for category, count in db.query(Complaint.category, func.count(Complaint.id)).group_by(Complaint.category).all()
    }
    by_priority = {
        priority: count
        for priority, count in db.query(Complaint.priority, func.count(Complaint.id)).group_by(Complaint.priority).all()
    }
    by_department = {
        name: count
        for name, count in db.query(Department.name, func.count(Complaint.id)).join(Complaint.assigned_department).group_by(Department.name).all()
    }

    return {
        'total_complaints': total,
        'status_counts': by_status,
        'category_counts': by_category,
        'priority_counts': by_priority,
        'department_counts': by_department,
    }
