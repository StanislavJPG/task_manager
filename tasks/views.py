from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet

from tasks.models import Project, Task

User = get_user_model()


class ProjectsViewAPI(ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request):
        # filter projects only by current user
        projects = (
            Project.objects.prefetch_related(
                Prefetch("task_set", queryset=Task.objects.order_by("-priority")),
            )
            .filter(user__pk=request.user.id)
            .order_by("-created_at")
            .all()
        )
        return render(request, "base.html", context={"projects": projects})

    def post(self, request: Request):
        new_project_title: str = request.POST.get("new_project_title")
        requesting_user = User.objects.get(pk=request.user.id)

        Project.objects.create(title=new_project_title, user=requesting_user)
        return self.get(request)

    def delete(self, request: Request, pk: int):
        project = Project.objects.get(pk=pk)
        project.delete()
        return HttpResponse(HTTP_200_OK)

    @staticmethod
    def edit_project_title(request: Request, pk: int):
        """
        now I should write the API using default django
        for the manage the right requests by exact url

        only reason why I'm using staticmethod
        is that if I'd use DRF API classes it may commit n+1 problem:
        two SELECT queries from PROJECT table:
        1. For the get request
        2. For the post request
        """
        project = get_object_or_404(Project, id=pk)
        if request.method == "POST":
            new_title = request.POST.get("title")
            project.title = new_title
            project.save()
            return HttpResponse(project.title)
        return render(request, "edit_project_title.html", {"project": project})


class TasksViewAPI(ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @transaction.atomic()
    def post_task(self, request: Request, project_id: int):
        title: str = request.POST.get("title")
        task = Task.objects.create(
            title=title,
            project=Project.objects.get(pk=project_id),
        )
        return render(request, "tasks-list.html", context={"project": task.project})

    @transaction.atomic()
    def change_priority(self, request: Request, task_id: int):
        priority = request.POST.get("priority")
        task = Task.objects.get(pk=task_id)
        task.priority = int(priority)
        task.save()

        return render(request, "tasks-list.html", context={"project": task.project})

    def delete(self, request: Request, task_id: int):
        task = Task.objects.get(pk=task_id)
        task.delete()
        return HttpResponse(HTTP_200_OK)

    @staticmethod
    def edit_task_title(request: Request, task_id: int):
        """
        now I should write the API using default django
        for the manage the right requests by exact url

        only reason why I'm using staticmethod
        is that if I'd use DRF API classes it may commit n+1 problem:
        two SELECT queries from PROJECT table:
        1. For the get request
        2. For the post request
        """
        task = get_object_or_404(Task, id=task_id)
        if request.method == "POST":
            new_title = request.POST.get("title")
            task.title = new_title
            task.save()
            return HttpResponse(task.title)
        return render(request, "edit_task_title.html", {"task": task})
