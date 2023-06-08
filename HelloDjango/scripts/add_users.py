from django.contrib.auth import get_user_model
from faker import Faker

f = Faker()
MyUser = get_user_model()

def delete_all_users():
    MyUser.objects.all().delete()


def create_vlad():
    MyUser.objects.create_superuser(
        username='vlad',
        password='2030',
    )


def create_fake_users(num=5):
    for _ in range(num):
        MyUser.objects.create_user(
            username=f.first_name(),
            password='0000',
        )
    print('User created:', MyUser.objects.count())


delete_all_users()
create_vlad()
create_fake_users()


