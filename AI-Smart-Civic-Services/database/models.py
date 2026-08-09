from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(150), nullable=False)
    role = Column(String(50), nullable=False, default='citizen')
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    complaints = relationship('Complaint', back_populates='citizen', foreign_keys='Complaint.citizen_id')
    assignments = relationship('Complaint', back_populates='assigned_staff', foreign_keys='Complaint.assigned_staff_id')
    notifications = relationship('Notification', back_populates='user', cascade='all, delete-orphan')


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    complaints = relationship('Complaint', back_populates='assigned_department')


class Complaint(Base):
    __tablename__ = 'complaints'
    __table_args__ = (
        UniqueConstraint('title', 'citizen_id', name='uq_complaint_title_citizen'),
        Index('ix_complaint_status_priority', 'status', 'priority'),
        Index('ix_complaint_category_status', 'category', 'status'),
    )

    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    priority = Column(String(50), nullable=False)
    priority_score = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default='Submitted')
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String(255), nullable=True)
    assigned_department_id = Column(Integer, ForeignKey('departments.id', ondelete='SET NULL'), nullable=True, index=True)
    assigned_staff_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    resolved_at = Column(DateTime, nullable=True)

    citizen = relationship('User', back_populates='complaints', foreign_keys=[citizen_id])
    assigned_department = relationship('Department', back_populates='complaints')
    assigned_staff = relationship('User', back_populates='assignments', foreign_keys=[assigned_staff_id])
    images = relationship('ComplaintImage', back_populates='complaint', cascade='all, delete-orphan')
    status_history = relationship('ComplaintStatusHistory', back_populates='complaint', cascade='all, delete-orphan')
    ai_analyses = relationship('AIAnalysis', back_populates='complaint', cascade='all, delete-orphan')


class ComplaintImage(Base):
    __tablename__ = 'complaint_images'

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey('complaints.id', ondelete='CASCADE'), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(1024), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    complaint = relationship('Complaint', back_populates='images')


class ComplaintStatusHistory(Base):
    __tablename__ = 'complaint_status_history'

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey('complaints.id', ondelete='CASCADE'), nullable=False, index=True)
    status = Column(String(50), nullable=False)
    comment = Column(Text, nullable=True)
    changed_by_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    complaint = relationship('Complaint', back_populates='status_history')


class AIAnalysis(Base):
    __tablename__ = 'ai_analyses'

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey('complaints.id', ondelete='CASCADE'), nullable=False, index=True)
    category = Column(String(50), nullable=False)
    priority = Column(String(50), nullable=False)
    priority_score = Column(Float, nullable=False)
    recommended_department = Column(String(100), nullable=False)
    urgency_reason = Column(Text, nullable=True)
    suggested_action = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    possible_duplicates = Column(Text, nullable=True)
    raw_input = Column(Text, nullable=True)
    raw_output = Column(Text, nullable=True)
    model_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    complaint = relationship('Complaint', back_populates='ai_analyses')


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    complaint_id = Column(Integer, ForeignKey('complaints.id', ondelete='CASCADE'), nullable=True, index=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='notifications')
