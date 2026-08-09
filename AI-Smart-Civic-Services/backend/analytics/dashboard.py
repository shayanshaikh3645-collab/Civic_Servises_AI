from sqlalchemy import func
from database.models import Complaint, Department
from database.session import get_db


class DashboardAnalytics:
    def __init__(self, db):
        self.db = db

    def summary(self) -> dict:
        total = self.db.scalar(func.count(Complaint.id))
        return {
            'total_complaints': total,
            'status_counts': self._count_by(Complaint.status),
            'category_counts': self._count_by(Complaint.category),
            'priority_counts': self._count_by(Complaint.priority),
            'department_counts': self._department_counts(),
        }

    def _count_by(self, column):
        return {value: count for value, count in self.db.query(column, func.count(Complaint.id)).group_by(column).all()}

    def _department_counts(self) -> dict:
        return {
            name: count
            for name, count in self.db.query(Department.name, func.count(Complaint.id))
            .join(Complaint.assigned_department)
            .group_by(Department.name)
            .all()
        }
