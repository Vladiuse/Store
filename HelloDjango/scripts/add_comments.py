from store.models import Comment, Book, MyUser
from faker import Faker
import random as r

ru_faker = Faker('ru_RU')


def dell_all_comments():
    Comment.objects.all().delete()


def add_comments():
    comments_to_create = []
    books = Book.objects.all()
    users = MyUser.objects.all()
    for user in users:
        books_for_comments = set(r.choices(books, k=r.randint(1,len(books))))
        for book in books_for_comments:
            comment = Comment(
                user=user,
                book=book,
                text=ru_faker.sentence(nb_words=r.randint(1, 10)),
                stars=r.randint(1, 5)
            )
            comments_to_create.append(comment)
    Comment.objects.bulk_create(comments_to_create)
    print('Comments created', Comment.objects.count())


dell_all_comments()
add_comments()
