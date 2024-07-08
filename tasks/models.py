from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    title = models.CharField(max_length=90, null=False, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Task(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1, _("Low")
        MEDIUM = 2, _("Medium")
        HIGH = 3, _("High")

    title = models.CharField(max_length=90, null=False, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_("project"))
    is_done = models.BooleanField(null=False, default=False)
    deadline_to = models.DateField(null=True, default=None)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)

    def __str__(self):
        return self.title
