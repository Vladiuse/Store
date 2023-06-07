import os
from buttons.models import Book, Genre
from django.core.files.uploadedfile import SimpleUploadedFile
import random as r

IMAGES_PATH = './scripts/books/images/'
books_data = [
    {
        'name': 'повелитель мух',
        'image_name': 'pig_head.jpg'
    },
    {
        'name': 'Онегин',
        'image_name': 'o.webp'
    },
    {
        'name': '1984',
        'image_name': '1984.webp'
    },
    {
        'name': 'Идиот',
        'image_name': 'i.webp'
    },
    {
        'name': 'Карамазовы',
        'image_name': 'b.webp'
    },
    {
        'name': 'Бесы',
        'image_name': 'bb.webp'
    },
    {
        'name': 'Преступление и наказание',
        'image_name': 'pp.webp'
    },
    # {
    #     'name': 'XXXXX',
    #     'image_name': 'XXXXXXX'
    # },
]



def delete_all_books():
    for book in Book.objects.all():
        book.delete()
    print('All books deleted')


def create_books():
    genres = Genre.objects.all()
    print(genres)
    for book in books_data:
        image_path = os.path.join(IMAGES_PATH, book['image_name'])
        book = Book.objects.create(
            name=book['name'],
            image=SimpleUploadedFile(
                name='x.jpg',
                content=open(image_path, 'rb').read(),
                content_type=f'image/jpg'),
        )
        g = r.choices(genres, k=r.randint(1,3))
        book.genre.set(g)
    print('Books created')


delete_all_books()
create_books()
