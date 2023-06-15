from store.models import Position, MyUser, Employee
from django.contrib.auth.models import Group

moderator = Position.objects.get(pk='moderator')
seller = Position.objects.get(pk='seller')
manager = Position.objects.get(pk='manager')

moderator_group = Group.objects.get(name='moderator')
seller_group = Group.objects.get(name='seller')
manager_group = Group.objects.get(name='manager')


EMPLOYEE_DATA = [
    {
        'username': 'moderator',
        'position': moderator,
        'group':moderator_group,
    },
    {
        'username': 'manager',
        'position': manager,
        'group': manager_group,
    },
    {
        'username': 'seller_1',
        'position': seller,
        'group': seller_group,
    },
    {
        'username': 'seller_2',
        'position': seller,
        'group': seller_group,
    },

    {
        'username': 'seller_3',
        'position': seller,
        'group': seller_group,
    },
]


def delete_employee():
    MyUser.objects.filter(is_staff=True).exclude(username='vlad').delete()


def create_employee():
    for item in EMPLOYEE_DATA:
        user = MyUser.objects.create_user(
            username=item['username'],
            password='0000',
            is_staff=True,
        )
        Employee.objects.create(
            user=user,
            position=item['position']
        )
        user.groups.add(item['group'])
    print('Employee created', Employee.objects.count())


delete_employee()
create_employee()