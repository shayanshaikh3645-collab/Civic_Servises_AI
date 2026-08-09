from typing import Dict

CATEGORY_KEYWORDS = {
    'Road Damage': ['pothole', 'road', 'street', 'asphalt', 'sinkhole', 'crack'],
    'Street Light': ['light', 'street light', 'lamp', 'electricity', 'bulb', 'wiring'],
    'Garbage': ['garbage', 'trash', 'waste', 'dumpster', 'litter', 'bin'],
    'Water Supply': ['water', 'leak', 'pipe', 'tap', 'service disruption', 'pressure'],
    'Sewerage': ['sewer', 'drain', 'overflow', 'sewage', 'clog', 'manhole'],
    'Public Safety': ['danger', 'crime', 'hazard', 'security', 'unsafe', 'accident'],
}
PRIORITY_LEVELS = {
    'Critical': 90,
    'High': 70,
    'Medium': 50,
    'Low': 30,
}


def analyze_complaint(title: str, description: str) -> Dict[str, object]:
    text = f"{title} {description}".lower()
    category = 'Other'
    for label, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            category = label
            break

    if category == 'Public Safety' or 'danger' in text or 'accident' in text:
        priority = 'Critical'
    elif category in ('Road Damage', 'Water Supply', 'Sewerage'):
        priority = 'High'
    elif category == 'Street Light':
        priority = 'Medium'
    elif category == 'Garbage':
        priority = 'Medium'
    else:
        priority = 'Low'

    return {
        'category': category,
        'priority': priority,
        'priority_score': float(PRIORITY_LEVELS[priority]),
    }
