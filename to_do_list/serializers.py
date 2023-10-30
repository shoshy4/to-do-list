from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Task, TasksList


class TaskSerializer(serializers.ModelSerializer):
    task_owner = serializers.ReadOnlyField(source='task.username')
    task_list = serializers.CharField(required=False, allow_blank=True)
    created_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        fields = ['task_list', 'title', 'description', 'status', 'created_date', 'task_owner']


class TasksListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    created_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TasksList
        fields = ['title', 'created_date', 'owner']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        return token


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
