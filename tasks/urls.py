from django.urls import path

from tasks.views import ProjectsViewAPI, TasksViewAPI

projects_urlpatterns = [
    path("", ProjectsViewAPI.as_view({"get": "get"}), name="base-page"),
    path(
        "delete/pk=<int:pk>",
        ProjectsViewAPI.as_view({"delete": "delete"}),
        name="project-delete",
    ),
    path("edit/pk=<int:pk>/", ProjectsViewAPI.edit_task_title, name="project-edit"),
    path("create/", ProjectsViewAPI.as_view({"post": "post"}), name="project-post"),
]

tasks_urlpatterns = [
    path(
        "task/create/pk=<int:project_id>",
        TasksViewAPI.as_view({"post": "post_task"}),
        name="task-create",
    ),
    path(
        "task/delete/pk=<int:task_id>",
        TasksViewAPI.as_view({"delete": "delete"}),
        name="task-delete",
    ),
    path(
        "task/priority/pk=<int:task_id>",
        TasksViewAPI.as_view({"post": "change_priority"}),
        name="task-priority",
    ),
]

urlpatterns = projects_urlpatterns + tasks_urlpatterns
