# Generated by Django 4.2 on 2024-07-09 15:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0004_alter_project_title_alter_task_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
