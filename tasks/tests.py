from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import RequestFactory

from tasks.models import Project, Task

User = get_user_model()


class TestAuthorization(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Test User2", password="testpassword123", email="testuser2@gmail.com"
        )

    def test_registration(self):
        url = reverse("account_signup")
        data = {
            "username": "Test User",
            "password": "testpassword123",
            "email": "testuser@gmail.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorization(self):
        url = reverse("account_login")
        data = {
            "username": "Test User2",
            "password": "testpassword123",
            "email": "testuser2@gmail.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestManagerMixin(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="Test User", password="testpassword123", email="testuser@gmail.com"
        )

        self.login_url = reverse("token_obtain_pair")
        login_data = {"username": "Test User", "password": "testpassword123"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        self.test_project = Project.objects.create(title="TitleTestProject", user=self.user)

        self.test_task = Task.objects.create(
            title="TitleTestTask",
            project=self.test_project,
        )


class TestProjectsViews(TestManagerMixin):
    def test_project_creation(self):
        url = reverse("project-post")
        data = {"new_project_title": "Test Project"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_title_edit(self):
        url = reverse(viewname="project-edit", kwargs={"pk": self.test_project.id})
        data = {"title": "New Test Title"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_project(self):
        url = reverse(viewname="project-delete", kwargs={"pk": self.test_project.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTasksViews(TestManagerMixin):
    def test_task_creation(self):
        url = reverse("task-create", kwargs={"project_id": self.test_project.id})
        data = {"title": "Test Task Tile"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_priority(self):
        url = reverse("task-priority", kwargs={"task_id": self.test_task.id})
        data = {"priority": 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task_status(self):
        url = reverse("task-status", kwargs={"task_id": self.test_task.id})
        data = {"checked": True}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task_deadline(self):
        url = reverse("task-deadline", kwargs={"task_id": self.test_task.id})
        data = {"deadline": now().date()}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_task_title(self):
        url = reverse("task-edit", kwargs={"task_id": self.test_task.id})
        data = {"title": "New Task Title"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task(self):
        url = reverse("task-delete", kwargs={"task_id": self.test_task.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
