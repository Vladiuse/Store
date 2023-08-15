from django.db import models
import os
from django.core.validators import MinValueValidator, MaxValueValidator
from user_api.models import MyUser, Profile


class Position(models.Model):
    id = models.CharField(
        max_length=30,
        unique=True,
        primary_key=True,
    )
    name = models.CharField(
        max_length=30,
        unique=True,
    )

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
    )
    date_joined = models.DateField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.user}:{self.position}'



class Author(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class BookManager(models.Manager):

    def get_queryset(self):
        return Book.objects.filter(is_public=True)


class Book(models.Model):
    name = models.CharField(
        max_length=30
    )
    price = models.FloatField(
        default=0
    )
    genre = models.ManyToManyField(
        'Genre',
        blank=True
    )
    image = models.ImageField(
        upload_to='book_images',
        blank=True
    )
    is_public = models.BooleanField(
        default=True
    )
    description = models.TextField(
        blank=True
    )
    author = models.ForeignKey(
        Author,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    available_in_store = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['pk',]

    def __str__(self):
        return self.name

    def delete(self):
        if self.image:
            os.remove(self.image.path)
        super().delete()

    def comments_count(self):
        return self.comment.count()

    # def add_to_favorite(self, user):



class Comment(models.Model):
    owner = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    text = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True,
    )
    stars = models.PositiveIntegerField(
        validators=[MaxValueValidator(5),]
    )

    class Meta:
        unique_together = ['owner', 'book']

    def __str__(self):
        return f'<Comment:{self.pk}> {self.text}'

    def dislike_count(self):
        return self.like_set.filter(flag=False).count()

    def like_count(self):
        return self.like_set.filter(flag=True).count()

    def user_like(self, user):
        for like in self.like_set.all():
            if like.owner == user:
                return like
        return None


    def set_like(self, user):
        like, created = Like.get_or_create(owner=user, comment=self, flag=True)
        like.flag = True
        if not created:
            like.save()
        return like

    def set_dislike(self, user):
        like, created = Like.get_or_create(owner=user, comment=self, flag=False)
        like.flag = False
        if not created:
            like.save()
        return like


class Genre(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True
    )

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='favorite',
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='is_favorite',
    )


    class Meta:
        unique_together = ['user', 'book']


    def __str__(self):
        return f'{self.user}:{self.book}'


class Test(models.Model):
    name = models.CharField(max_length=20)


class Like(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    flag = models.BooleanField()

    class Meta:
        unique_together = ['owner', 'comment']

    @staticmethod
    def get_or_create(owner, comment, flag):
        created = False
        try:
            like = Like.objects.get(owner=owner, comment=comment)
        except Like.DoesNotExist:
            like = Like.objects.create(owner=owner, comment=comment, flag=flag)
            created = True
        return like, created


