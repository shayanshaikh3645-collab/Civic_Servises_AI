from datetime import datetime
from typing import Optional

from backend.ai import ai_model
from database.models import AIAnalysis, Complaint, ComplaintStatusHistory, Notification
from database.session import SessionLocal


class ComplaintService:
    def __init__(self):
        self.db = SessionLocal()

    def create_complaint(self, citizen_id: int, payload: dict) -> Complaint:
        ai_result = ai_model.predict(payload.get('title', ''), payload.get('description', ''))
        complaint = Complaint(
            title=payload['title'],
            description=payload['description'],
            citizen_id=citizen_id,
            category=ai_result['category'],
            priority=ai_result['priority'],
            priority_score=ai_result['priority_score'],
            status='AI Analyzed',
            latitude=payload.get('latitude'),
            longitude=payload.get('longitude'),
            address=payload.get('address'),
            assigned_department_id=self._get_department_id(ai_result['recommended_department']),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        self.db.add(complaint)
        self.db.commit()
        self.db.refresh(complaint)

        analysis = AIAnalysis(
            complaint_id=complaint.id,
            category=ai_result['category'],
            priority=ai_result['priority'],
            priority_score=ai_result['priority_score'],
            recommended_department=ai_result['recommended_department'],
            urgency_reason=ai_result['urgency_reason'],
            suggested_action=ai_result['suggested_action'],
            keywords=','.join(ai_result['keywords']),
            possible_duplicates='',
            raw_input=f"{payload.get('title', '')} {payload.get('description', '')}",
            raw_output=str(ai_result),
            model_name=ai_result['model_name'],
        )

        status_history = ComplaintStatusHistory(
            complaint_id=complaint.id,
            status='AI Analyzed',
            comment='AI analysis completed',
            changed_by_id=citizen_id,
            created_at=datetime.utcnow(),
        )

        notification = Notification(
            user_id=citizen_id,
            complaint_id=complaint.id,
            message=f'Your complaint "{complaint.title}" was analyzed and routed to {ai_result["recommended_department"]}.',
        )

        self.db.add_all([analysis, status_history, notification])
        self.db.commit()
        return complaint

    def _get_department_id(self, department_name: str) -> Optional[int]:
        from database.models import Department

        department = self.db.query(Department).filter(Department.name == department_name).first()
        return department.id if department else None

    def close(self):
        self.db.close()
