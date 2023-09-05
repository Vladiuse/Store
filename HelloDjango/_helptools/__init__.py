import random as r
import string
from user_api.models import Profile, Employee, Position
from store.models import Book, Genre, Author, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
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
        group, created = Group.objects.get_or_create(name=add_group)
        user.groups.add(group)
    return employee, user


def create_genre():
    return Genre.objects.create(name=str_random())


def create_author():
    return Author.objects.create(name=str_random())

def get_book_fake_data(**kwargs):
    test_image_path = './HelloDjango/store/tests/book/book_logo.png'
    json = kwargs.pop('json', False)
    author = create_author()
    fake_data = {
        'name': str_random(),
        'is_public': True,
        'price': round(r.random() * 100, 2),
        'author': author if not json else author.pk,
        'available_in_store': r.randint(1, 5),
        'description': f.paragraph(nb_sentences=5),
        'img_cover': SimpleUploadedFile(
            name='x.jpg',
            content=open(test_image_path, 'rb').read(),
            content_type=f'image/jpg') if not json else open(test_image_path, 'rb')
    }
    fake_data.update(**kwargs)
    return fake_data

def create_book(**kwargs):
    genre = kwargs.pop('genre', create_genre())
    fake_data = get_book_fake_data(**kwargs)
    book = Book.objects.create(**fake_data)
    book.genre.add(genre)
    return book
