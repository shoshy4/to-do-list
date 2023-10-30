import factory
import factory.fuzzy
from to_do_list.models import TasksList
from django.contrib import auth
from datetime import datetime
from .user import UserFactory


class TasksListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TasksList

    title = factory.fuzzy.FuzzyText()
    created_date = factory.fuzzy.FuzzyDate(datetime.now().date())
    owner = factory.SubFactory(UserFactory)
