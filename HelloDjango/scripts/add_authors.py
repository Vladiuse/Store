from store.models import Author


authors = [
    'Пушкин',
    'Гоголь',
    'Толстой',
    'Чехов',
    'Горький',
    'Оскар Уайлд',
    'Оурвел',
    'Есенин',
    'Маяковский',
    'Достоевский',
    'Хэменгуей',
    'Ремарк',
    'Лермонтов',
]

def delete_all_authors():
    Author.objects.all().delete()


def create_authors():
    to_create = []
    for author_name in authors:
        to_create.append(Author(name=author_name))
    Author.objects.bulk_create(to_create)
    print('Author created:', Author.objects.count())


delete_all_authors()
create_authors()