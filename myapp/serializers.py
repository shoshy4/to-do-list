from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Task, TasksList


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='task.owner')
    task_list = serializers.CharField(required=False, allow_blank=True)
    created_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        fields = ['task_list', 'title', 'description', 'status', 'created_date', 'owner']


class TasksListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='taskslist.owner')
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
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
