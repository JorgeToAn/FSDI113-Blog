# Generated by Django 4.1.1 on 2022-09-29 01:29

from django.db import migrations


def populate_status(apps, schemaeditor):
    entries = {
        "published": "A post that appears on site (to all users).",
        "draft": "A post that is being worked on, or not ready to be viewed by other users.",
        "archived": "A post that no longer appears on the main site."
    }
    Status = apps.get_model("posts", "Status")
    for name, desc in entries.items():
        status_obj = Status(name=name, description=desc)
        status_obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_status'),
    ]

    operations = [
        migrations.RunPython(populate_status)
    ]
