from django.urls import path

from tasks.views import ProjectsViewAPI, ProjectsDeleteViewAPI

urlpatterns = [
    path("base/", ProjectsViewAPI.as_view(), name="base-page"),
    path("delete/pk=<int:pk>", ProjectsDeleteViewAPI.as_view(), name="project-delete"),
]
