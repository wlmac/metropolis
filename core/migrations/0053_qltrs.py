# Generated by Django 3.2.12 on 2022-10-18 19:06

from django.db import migrations

import core.utils.fields


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0052_merge_0051_auto_20220922_1619_0051_auto_20220926_2257"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="qltrs",
            field=core.utils.fields.SetField(
                null=True, verbose_name="Qualified Trials"
            ),
        ),
    ]
