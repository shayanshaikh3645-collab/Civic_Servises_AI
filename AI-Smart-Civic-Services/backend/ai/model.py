import csv
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

DATA_PATH = Path(__file__).resolve().parent / 'civic_problems_700.csv'


class ComplaintAiModel:
    def __init__(self):
        self.pipeline = None
        self.category_encoder = LabelEncoder()
        self.priority_encoder = LabelEncoder()
        self._build_model()

    def _load_dataset(self):
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"AI training data not found: {DATA_PATH}")
        df = pd.read_csv(DATA_PATH)
        df = df.dropna(subset=['description', 'category', 'priority'])
        df['text'] = df['description'].astype(str)
        return df

    def _build_model(self):
        df = self._load_dataset()
        self.category_encoder.fit(df['category'])
        self.priority_encoder.fit(df['priority'])

        X = df['text']
        y_category = self.category_encoder.transform(df['category'])
        y_priority = self.priority_encoder.transform(df['priority'])

        self.pipeline = Pipeline([
            ('vectorizer', TfidfVectorizer(max_features=4000, ngram_range=(1, 2))),
            ('classifier', LogisticRegression(max_iter=1000, solver='liblinear')),
        ])
        self.pipeline.fit(X, y_category)

        self.priority_map = LogisticRegression(max_iter=1000, solver='liblinear')
        self.priority_map.fit(X, y_priority)

    def predict(self, title: str, description: str) -> dict:
        text = f"{title or ''} {description or ''}".strip()
        prediction = self.pipeline.predict([text])[0]
        priority_prediction = self.priority_map.predict([text])[0]

        category = self.category_encoder.inverse_transform([prediction])[0]
        priority = self.priority_encoder.inverse_transform([priority_prediction])[0]

        return {
            'category': category,
            'priority': priority,
            'priority_score': float(self._map_priority_score(priority)),
            'keywords': self._extract_keywords(text),
            'recommended_department': self._map_department(category),
            'urgency_reason': self._build_urgency_reason(text, category, priority),
            'suggested_action': self._build_suggested_action(category, priority),
            'model_name': 'logistic-regression-v1',
        }

    def _map_priority_score(self, priority: str) -> int:
        return {
            'Critical': 95,
            'High': 75,
            'Medium': 50,
            'Low': 25,
        }.get(priority, 50)

    def _map_department(self, category: str) -> str:
        department_map = {
            'Safety': 'Public Safety',
            'Water': 'Water Supply',
            'Roads': 'Roads & Works',
            'Electricity': 'Electricity',
            'Waste': 'Waste Management',
            'Drainage': 'Drainage & Sewerage',
            'Other': 'Other',
        }
        return department_map.get(category, 'Other')

    def _extract_keywords(self, text: str) -> list[str]:
        cleaned = text.lower().replace('.', '')
        tokens = [token for token in cleaned.split() if len(token) > 3]
        unique = []
        for token in tokens:
            if token not in unique:
                unique.append(token)
            if len(unique) >= 8:
                break
        return unique

    def _build_urgency_reason(self, text: str, category: str, priority: str) -> str:
        reason = f"Detected {category.lower()} issue with {priority.lower()} urgency."
        if 'urgent' in text or 'critical' in text or 'danger' in text:
            reason += ' Text indicates immediate action may be required.'
        return reason

    def _build_suggested_action(self, category: str, priority: str) -> str:
        return f"Route to the {self._map_department(category)} team and schedule an inspection based on {priority.lower()} priority."  
