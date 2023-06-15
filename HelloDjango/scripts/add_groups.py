from django.contrib.auth.models import Group

GROUP_DATA = [
    {'name': 'moderator'},
    {'name': 'manager'},
    {'name': 'seller'},
]

def dell_all_groups():
    Group.objects.all().delete()

def create_groups():
    for item in GROUP_DATA:
        Group.objects.create(name=item['name'])
    print('Group created', Group.objects.count())


dell_all_groups()
create_groups()