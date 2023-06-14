from store.models import Position, MyUser, Employee

moderator = Position.objects.get(pk='moderator')
seller = Position.objects.get(pk='seller')
manager = Position.objects.get(pk='manager')


EMPLOYEE_DATA = [
    {
        'username': 'moderator',
        'position': moderator,
    },
    {
        'username': 'manager',
        'position': manager,
    },
    {
        'username': 'seller_1',
        'position': seller,
    },
    {
        'username': 'seller_2',
        'position': seller,
    },

    {
        'username': 'seller_3',
        'position': seller,
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
    print('Employee created', Employee.objects.count())


delete_employee()
create_employee()