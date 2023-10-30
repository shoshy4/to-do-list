from django.contrib import admin
from .models import Task, TasksList
from django.contrib.auth.admin import User


# Register your models here.
admin.site.register(Task)
admin.site.register(TasksList)
