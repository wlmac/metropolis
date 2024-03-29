# Generated by Django 3.2.15 on 2023-02-13 02:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0056_auto_20230212_0338"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="featured_image_description",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Alt text for the featured image e.g. what screen readers tell users",
                max_length=140,
            ),
        ),
    ]
