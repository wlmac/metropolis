# Generated by Django 3.2.10 on 2022-03-08 08:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0049_alter_user_timezone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="body",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="announcement",
            name="title",
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="body",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="title",
            field=models.CharField(max_length=64),
        ),
    ]
