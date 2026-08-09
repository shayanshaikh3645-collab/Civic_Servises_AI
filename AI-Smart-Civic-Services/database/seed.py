from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError

from database import models
from database.models import Department, User, Complaint, ComplaintStatusHistory, AIAnalysis
from database.session import SessionLocal, engine


def create_seed_data():
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    departments = [
        Department(name='Road Damage', description='Repair and maintain local road issues.'),
        Department(name='Street Light', description='Manage street lighting and electrical reports.'),
        Department(name='Garbage', description='Handle waste collection and sanitation problems.'),
        Department(name='Water Supply', description='Water distribution and leak repairs.'),
        Department(name='Sewerage', description='Sewer and drainage maintenance.'),
        Department(name='Public Safety', description='Public safety and street hazard response.'),
        Department(name='Other', description='General civic service requests.'),
    ]

    users = [
        User(email='admin@example.com', full_name='Project Admin', role='admin', hashed_password=bcrypt.hash('ChangeMe123!')),
        User(email='staff@example.com', full_name='Staff User', role='staff', hashed_password=bcrypt.hash('ChangeMe123!')),
        User(email='citizen@example.com', full_name='Citizen User', role='citizen', hashed_password=bcrypt.hash('ChangeMe123!')),
    ]

    session.add_all(departments + users)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()

    department = session.query(Department).filter_by(name='Road Damage').first()
    citizen = session.query(User).filter_by(role='citizen').first()
    staff = session.query(User).filter_by(role='staff').first()

    if department and citizen:
        complaint = Complaint(
            citizen_id=citizen.id,
            title='Pothole on Main Street',
            description='Large pothole on Main Street near the bus stop. Needs urgent repair.',
            category='Road Damage',
            priority='High',
            priority_score=80.0,
            status='Submitted',
            latitude=40.7128,
            longitude=-74.0060,
            address='Main Street and 5th Avenue',
            assigned_department_id=department.id,
            assigned_staff_id=staff.id if staff else None,
        )
        session.add(complaint)
        session.commit()

        status_history = ComplaintStatusHistory(
            complaint_id=complaint.id,
            status='Submitted',
            comment='Initial report created for development sample.',
        )
        ai_analysis = AIAnalysis(
            complaint_id=complaint.id,
            category='Road Damage',
            priority='High',
            priority_score=80.0,
            raw_input=complaint.description,
            raw_output='{"category":"Road Damage","priority":"High","priority_score":80.0}',
            model_name='mock-ai-v1',
        )
        session.add_all([status_history, ai_analysis])
        session.commit()

    session.close()


if __name__ == '__main__':
    create_seed_data()
    print('Seed data created successfully.')
