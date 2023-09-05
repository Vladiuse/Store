import random as r
import string
from user_api.models import Profile, Employee, Position
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from faker import Faker

f = Faker()
User = get_user_model()


def str_random(len=10) -> str:
    if len <= 0:
        raise ValueError('len attr must be positive')
    return ''.join(r.choices(string.ascii_lowercase, k=len))


def create_user():
    return User.objects.create_user(username=f.first_name() + str_random(3), password='0000')


def create_employee_user(add_group=False):
    user = User.objects.create_user(username=f.first_name() + str_random(3), password='0000')
    position = Position.objects.create(id=f.first_name(), name=f.first_name())
    employee = Employee.objects.create(position=position, user=user)
    if add_group:
        group = Group.objects.create(name=add_group)
        user.groups.add(group)
    return employee, user
