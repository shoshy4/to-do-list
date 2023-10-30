from django.conf import settings
from django.db import models
from django.utils import timezone


class TasksList(models.Model):
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Task(models.Model):
    task_list = models.ForeignKey('to_do_list.TasksList', blank=True, null=True, on_delete=models.CASCADE, related_name='task_list')
    task_owner = models.ForeignKey('auth.User', related_name='task', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

