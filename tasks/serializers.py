from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from tasks.models import Project, Task

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Project
        exclude = ("created_at",)

    def create(self, validated_data):
        request = self.context["request"]
        requesting_user = User.objects.get(pk=request.user.id)
        return Project.objects.create(**validated_data, user=requesting_user)

    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.save()
        return instance

    def validate(self, attrs):
        if len(attrs["title"]) > 70 or len(attrs["title"]) < 3:
            raise ValidationError(
                detail=f'Project title is {len(attrs["title"])}. '
                f'Min-length: 3, Max-length: 90.'
            )
        return attrs


class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(required=False)

    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        project_id = self.context["project_id"]
        task = Task.objects.create(
            title=validated_data["title"],
            project=Project.objects.get(pk=project_id),
        )
        return task

    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.save()
        return instance

    def validate(self, attrs):
        title_length = len(attrs["title"])
        if title_length > 70 or title_length < 3:
            raise ValidationError(
                detail=f"Task title is {title_length}. " f"Min-length: 3, Max-length: 70."
            )
        return attrs


class TaskPrioritySerializer(serializers.Serializer):
    priority = serializers.IntegerField()

    def validate(self, attrs):
        if attrs.get("priority") not in (1, 2, 3):
            raise ValidationError(detail="Invalid priority.")
        return attrs

    def update(self, instance, validated_data):
        instance.priority = validated_data["priority"]
        instance.save()
        return instance


class TaskStatusSerializer(serializers.Serializer):
    is_done = serializers.BooleanField()

    def validate(self, attrs):
        if not isinstance(attrs.get("is_done"), bool):
            raise ValidationError(detail="Invalid type for checked.")
        return attrs

    def update(self, instance, validated_data):
        instance.is_done = validated_data["is_done"]
        instance.save()
        return instance


class TaskDeadlineSerializer(serializers.Serializer):
    deadline_to = serializers.DateField()

    def validate(self, attrs):
        deadline = attrs["deadline_to"]
        if deadline < now().date():
            raise ValidationError(f"Deadline cannot be earlier then {now().date()}.")
        return attrs

    def update(self, instance, validated_data):
        instance.deadline_to = validated_data["deadline_to"]
        instance.save()
        return instance
