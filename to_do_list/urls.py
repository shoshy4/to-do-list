from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views_api import TaskCreateList, TaskUpdateDetailRemove, TasksListCreateList, \
    TasksListUpdateDetailRemove
from django.views.generic import TemplateView
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path


urlpatterns = [
    path('task/', TaskCreateList.as_view(), name="task_list_create_api"),
    path('task/<int:pk>/', TaskUpdateDetailRemove.as_view(), name="task_update_detail_remove_api"),
    path('tasks_list/', TasksListCreateList.as_view(), name="tasks_list_list_create_api"),
    path('tasks_list/<int:pk>/', TasksListUpdateDetailRemove.as_view(), name="tasks_list_update_detail_remove_api"),
    path('tasks_list/<int:task_list_pk>/task/', TaskCreateList.as_view(), name="task_list_create_api"),  # TODO: name совпадает с 13 строкой
    path('tasks_list/<int:task_list_pk>/task/<int:pk>/', TaskUpdateDetailRemove.as_view(), name="task_update_detail_remove_api"),
    # TODO: Привести к одному виду pk + длина строки
]
