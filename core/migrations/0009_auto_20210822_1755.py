# Generated by Django 3.2.6 on 2021-08-22 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_remove_term_num_courses"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="term",
        ),
        migrations.AddField(
            model_name="event",
            name="organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                related_query_name="event",
                to="core.organization",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                related_name="events",
                related_query_name="event",
                to="core.Tag",
            ),
        ),
    ]
