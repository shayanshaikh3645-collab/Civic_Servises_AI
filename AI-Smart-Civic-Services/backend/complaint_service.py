import uuid
from datetime import datetime
from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

CATEGORY_LABELS = ['road', 'water', 'electricity', 'sanitation', 'other']
PRIORITY_LABELS = ['low', 'medium', 'high']

class ComplaintService:
    def __init__(self):
        self.complaints: List[Dict] = []
        self.vectorizer = TfidfVectorizer(max_features=2000)
        self.classifier = LogisticRegression(max_iter=1000)
        self._train_sample_model()

    def _train_sample_model(self):
        examples = [
            ('pothole near main street', 'road', 'high'),
            ('broken street light', 'electricity', 'medium'),
            ('water leak in kitchen', 'water', 'high'),
            ('garbage not collected', 'sanitation', 'medium'),
            ('park bench damaged', 'other', 'low'),
        ]
        texts, categories, priorities = zip(*examples)
        X = self.vectorizer.fit_transform(texts)
        self.classifier.fit(X, categories)
        self.priority_map = {category: priority for category, priority in zip(categories, priorities)}

    def list_complaints(self) -> List[Dict]:
        return self.complaints

    def get_complaint(self, complaint_id: str) -> Dict | None:
        return next((c for c in self.complaints if c['id'] == complaint_id), None)

    def create_complaint(self, payload: Dict) -> Dict:
        description = payload.get('description', '').strip()
        location = payload.get('location', '').strip()
        if not description:
            raise ValueError('Description is required')

        category, priority = self._classify(description)
        complaint = {
            'id': str(uuid.uuid4()),
            'description': description,
            'location': location,
            'category': category,
            'priority': priority,
            'status': 'new',
            'submitted_at': datetime.utcnow().isoformat() + 'Z',
        }
        self.complaints.append(complaint)
        return complaint

    def update_status(self, complaint_id: str, status: str) -> Dict | None:
        complaint = self.get_complaint(complaint_id)
        if complaint is None:
            return None
        complaint['status'] = status
        return complaint

    def _classify(self, description: str) -> tuple[str, str]:
        X = self.vectorizer.transform([description])
        category = self.classifier.predict(X)[0]
        priority = self.priority_map.get(category, 'medium')
        return category, priority
