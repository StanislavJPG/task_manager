from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet

from tasks.models import Project, Task
from tasks.serializers import (
    ProjectSerializer,
    TaskSerializer,
    TaskPrioritySerializer,
    TaskStatusSerializer,
    TaskDeadlineSerializer,
)

User = get_user_model()


class ProjectsViewAPI(ViewSet):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        # filter projects only by current user
        projects = (
            Project.objects.prefetch_related(
                Prefetch("task_set", queryset=Task.objects.order_by("priority")),
            )
            .filter(user__pk=request.user.id)
            .order_by("-created_at")
        )
        return render(request, "base.html", context={"projects": projects})

    def post(self, request: Request):
        new_project_title: str = request.POST.get("new_project_title")
        project = ProjectSerializer(
            data={"title": new_project_title}, context={"request": request}
        )
        project.is_valid(raise_exception=True)
        project.save()

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
            new_title: str = request.POST.get("title")
            project = ProjectSerializer(
                data={"title": new_title}, instance=project, context={"request": request}
            )
            project.is_valid(raise_exception=True)
            project.save()
            return HttpResponse(project.instance.title)
        return render(request, "edit_project_title.html", {"project": project})


class TasksViewAPI(ViewSet):
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def post_task(self, request: Request, project_id: int):
        title: str = request.POST.get("title")
        task = TaskSerializer(data={"title": title}, context={"project_id": project_id})
        task.is_valid(raise_exception=True)
        task.save()
        return render(request, "tasks-list.html", context={"project": task.instance.project})

    @transaction.atomic()
    def change_priority(self, request: Request, task_id: int):
        priority = request.POST.get("priority")
        task = Task.objects.order_by("-priority").get(pk=task_id)

        task_serializer = TaskPrioritySerializer(data={"priority": priority}, instance=task)
        task_serializer.is_valid(raise_exception=True)
        task_serializer.save()

        return render(
            request, "tasks-list.html", context={"project": task_serializer.instance.project}
        )

    def update_task_status(self, request: Request, task_id: int):
        task = Task.objects.order_by("-priority").get(pk=task_id)

        checked = request.data["checked"]
        task = TaskStatusSerializer(data={"is_done": checked}, instance=task)
        task.is_valid(raise_exception=True)
        task.save()

        return render(request, "tasks-list.html", context={"project": task.instance.project})

    def update_task_deadline(self, request: Request, task_id: int):
        task = Task.objects.order_by("-priority").get(pk=task_id)
        deadline = request.POST.get("deadline")
        task = TaskDeadlineSerializer(data={"deadline_to": deadline}, instance=task)
        task.is_valid(raise_exception=True)
        task.save()
        return render(request, "tasks-list.html", context={"project": task.instance.project})

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
        task = Task.objects.order_by("-priority").get(pk=task_id)
        if request.method == "POST":
            new_title = request.POST.get("title")
            task = TaskSerializer(data={"title": new_title}, instance=task)
            task.is_valid(raise_exception=True)
            task.save()
            return HttpResponse(task.instance.title)
        return render(request, "edit_task_title.html", {"task": task})
