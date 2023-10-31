from django.contrib import admin
from .models import Task, TasksList

admin.site.register(Task)
admin.site.register(TasksList)
