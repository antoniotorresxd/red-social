import json
from apps.comunity.models import Community
from django.db import transaction

def run():
    with open('comunidades_ficticias.json') as f:
        data = json.load(f)

    comunidades = [
        Community(
            admin_id=c['fields']['admin_id'],
            name=c['fields']['name'],
            code=c['fields']['code'],
            type=c['fields']['type'],
            list_users=c['fields']['list_users']
        )
        for c in data
    ]

    with transaction.atomic():
        Community.objects.bulk_create(comunidades, batch_size=500)

    print(f"✅ {len(comunidades)} comunidades creadas exitosamente.")
