# Generated by Django 4.2 on 2024-07-09 12:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0003_project_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="title",
            field=models.CharField(blank=True, max_length=70),
        ),
        migrations.AlterField(
            model_name="task",
            name="title",
            field=models.CharField(blank=True, max_length=70),
        ),
    ]
