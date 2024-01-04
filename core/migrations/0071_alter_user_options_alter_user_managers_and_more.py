# Generated by Django 5.0 on 2024-01-04 12:44

import core.models.user
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0070_remove_staffmember_unique_staff_member_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "user", "verbose_name_plural": "users"},
        ),
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", core.models.user.CaseInsensitiveUserManager()),
            ],
        ),
        migrations.RemoveConstraint(
            model_name="user",
            name="username-lower-check",
        ),
    ]
