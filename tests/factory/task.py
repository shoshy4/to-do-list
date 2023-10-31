import factory
import factory.fuzzy
from to_do_list.models import Task, TasksList
from datetime import datetime

from .tasks_list import TasksListFactory
from .user import UserFactory


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    task_list = factory.SubFactory(TasksListFactory)
    owner = factory.SubFactory(UserFactory)
    title = factory.fuzzy.FuzzyText()
    description = factory.fuzzy.FuzzyText()
    status = factory.fuzzy.FuzzyText()
    created_date = factory.fuzzy.FuzzyDate(datetime.now().date())

