import json
from django.utils.dateparse import parse_datetime
from django.db import transaction
from apps.publications.models import Publication

def run():
    with open('publicaciones_ficticias-3.json') as f:
        data = json.load(f)

    publicaciones = [
        Publication(
            community_id=p['fields']['community_id'],
            user_id=p['fields']['user_id'],
            type=p['fields']['type'],
            description=p['fields']['description'],
            timestamp=parse_datetime(p['fields']['timestamp']),
            title=p['fields']['title'],
            due_date=parse_datetime(p['fields']['due_date']) if p['fields']['due_date'] else None
        )
        for p in data
    ]

    with transaction.atomic():
        Publication.objects.bulk_create(publicaciones, batch_size=500)

    print(f"✅ {len(publicaciones)} publicaciones creadas exitosamente.")
