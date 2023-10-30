from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .filters import TaskFilter
from .models import Task, TasksList
from .permissions import IsOwnerOrReadOnly, IsTaskOwnerOrReadOnly
from .serializers import TasksListSerializer, TaskSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from django.utils import timezone
from django.contrib.auth import authenticate, login


class TaskCreateList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsTaskOwnerOrReadOnly]
    serializer_class = TaskSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        tasks = Task.objects.all()
        if self.kwargs.get('task_list_pk') is None:
            return tasks.filter(task_owner=self.request.user).order_by('-created_date')
        else:
            return tasks.filter(task_owner=self.request.user, task_list_id=self.kwargs.get('task_list_pk')).order_by(
                '-created_date')

    def perform_create(self, serializer):
        if self.kwargs.get('task_list_pk') is None:
            serializer.save(task_owner=self.request.user)
        else:
            tasks_list = get_object_or_404(TasksList, pk=self.kwargs.get('task_list_pk'))
            serializer.save(task_owner=self.request.user, task_list=tasks_list)


class TaskUpdateDetailRemove(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsTaskOwnerOrReadOnly]

    def get_queryset(self):
        tasks = Task.objects.all()
        if self.kwargs.get('task_list_pk') is None:
            return tasks.filter(task_owner=self.request.user).order_by('-created_date')
        else:
            return tasks.filter(task_owner=self.request.user, task_list_id=self.kwargs.get('task_list_pk')).order_by(
                '-created_date')
        # return Task.objects.filter(task_owner=self.request.user, task_list=None).order_by('-created_date')

    serializer_class = TaskSerializer


class TasksListCreateList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = TasksListSerializer

    def get_queryset(self):
        # return Task.objects.filter(task_owner=self.request.user, task_list=None).order_by('-created_date')
        tasks = TasksList.objects.all()
        return tasks.filter(owner=self.request.user).order_by('-created_date')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TasksListUpdateDetailRemove(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return TasksList.objects.filter(owner=self.request.user).order_by('-created_date')

    serializer_class = TasksListSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    lookup_field = "username"

    def get_queryset(self):
        return User.objects.all()
