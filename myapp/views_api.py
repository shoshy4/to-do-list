from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from .filters import TaskFilter
from to_do_list.models import TasksList, Task
from .permissions import IsOwnerPermission
from .serializers import TasksListSerializer, TaskSerializer, UserSerializer
from rest_framework import generics


class TaskCreateList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerPermission]
    serializer_class = TaskSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        tasks = Task.objects.all()
        if self.kwargs.get('pk') is None:
            return tasks.filter(owner=self.request.user).order_by('-created_date')
        else:
            return tasks.filter(
                owner=self.request.user,
                task_list_id=self.kwargs.get('pk')
            ).order_by('-created_date')

    def perform_create(self, serializer):
        if self.kwargs.get('pk') is None:
            serializer.save(owner=self.request.user)
        else:
            tasks_list = get_object_or_404(TasksList, pk=self.kwargs.get('pk'))
            serializer.save(owner=self.request.user, task_list=tasks_list)


class TaskUpdateDetailRemove(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerPermission]
    serializer_class = TaskSerializer

    def get_queryset(self):
        tasks = Task.objects.all()
        if self.kwargs.get('pk') is None:
            return tasks.filter(owner=self.request.user).order_by('-created_date')
        else:
            return tasks.filter(
                owner=self.request.user,
                task_list_id=self.kwargs.get('pk')
            ).order_by('-created_date')


class TasksListCreateList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerPermission]
    serializer_class = TasksListSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        tasks = TasksList.objects.all()
        return tasks.filter(owner=self.request.user).order_by('-created_date')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TasksListUpdateDetailRemove(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerPermission]
    serializer_class = TasksListSerializer

    def get_queryset(self):
        return TasksList.objects.filter(owner=self.request.user).order_by('-created_date')


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
