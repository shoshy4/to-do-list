from django.conf import settings
from django.db import models
from django.utils import timezone


class TasksList(models.Model):
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasklists', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Task(models.Model):
    task_list = models.ForeignKey('TasksList', blank=True, null=True,
                                  on_delete=models.CASCADE,
                                  related_name='tasks_lists')
    owner = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

