from buttons.models import Genre


genres = [
    'Приключения',
    'Классика',
    'Ужасы',
    'Путешествия',
    'Триллер',
]


def delete_all_genres():
    for g in Genre.objects.all():
        g.delete()


def create_genres():
    for name in genres:
        Genre.objects.create(name=name)


delete_all_genres()
create_genres()