# Generated by Django 3.2.6 on 2021-08-16 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_announcement_replaces'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='term',
            name='num_courses',
        ),
    ]