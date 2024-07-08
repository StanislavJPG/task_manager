from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DeleteView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.views import APIView

from tasks.models import Project


class ProjectsViewAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request):
        # filter projects only by current user
        projects = (
            Project.objects.prefetch_related("task_set").filter(user__pk=request.user.id).all()
        )
        return render(request, "base.html", context={"projects": projects})

    def patch(self): ...


class ProjectsDeleteViewAPI(DeleteView):
    model = Project

    def delete(self, request: Request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse({"success": 200})
