from django.db import migrations

rolerights = {
    'IMIS Administrator': ['206001', '206002'],
}


def add_rights(role_name, role_model, role_right_model):
    role = role_model.objects.get(name=role_name)
    for right_id in rolerights[role_name]:
        if not role_right_model.objects.filter(validity_to__isnull=True, role=role, right_id=right_id).exists():
            _add_right_for_role(role, right_id, role_right_model)


def _add_right_for_role(role, right_id, role_right_model):
    role_right_model.objects.create(role=role, right_id=right_id, audit_user_id=1)


def on_migration(apps, schema_editor):
    role_model = apps.get_model("core", "role")
    role_right_model = apps.get_model("core", "roleright")
    for role in rolerights:
        add_rights(role, role_model, role_right_model)


class Migration(migrations.Migration):
    dependencies = [
        ('payroll', '0015_merge_20240207_1703'),
    ]

    operations = [
        migrations.RunPython(on_migration),
    ]
