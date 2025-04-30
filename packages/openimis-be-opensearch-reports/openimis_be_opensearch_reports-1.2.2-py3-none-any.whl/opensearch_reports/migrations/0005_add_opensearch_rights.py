from django.db import migrations


opensearch_rights = [199001, 199003]
imis_administrator_system = 64


def add_rights(apps, schema_editor):
    RoleRight = apps.get_model('core', 'RoleRight')
    Role = apps.get_model('core', 'Role')
    role = Role.objects.get(is_system=imis_administrator_system)
    for right_id in opensearch_rights:
        if not RoleRight.objects.filter(validity_to__isnull=True, role=role, right_id=right_id).exists():
            _add_right_for_role(role, right_id, RoleRight)


def _add_right_for_role(role, right_id, RoleRight):
    RoleRight.objects.create(role=role, right_id=right_id, audit_user_id=1)


def remove_rights(apps, schema_editor):
    RoleRight = apps.get_model('core', 'RoleRight')
    RoleRight.objects.filter(
        role__is_system=imis_administrator_system,
        right_id__in=opensearch_rights,
        validity_to__isnull=True
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('opensearch_reports', '0004_alter_historicalopensearchdashboard_date_created_and_more')
    ]

    operations = [
        migrations.RunPython(add_rights, remove_rights),
    ]
