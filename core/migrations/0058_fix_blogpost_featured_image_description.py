from django.db import migrations


def reset_description(apps, schema_editor):
    BlogPost = apps.get_model("core","BlogPost")
    BlogPost.objects.filter(featured_image_description='This image has no description.').update(featured_image_description='')

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_alter_blogpost_featured_image_description'),
    ]

    operations = [
        migrations.RunPython(reset_description),
    ]
