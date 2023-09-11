import random as r
from django.db import models
import os
from django.core.validators import MinValueValidator, MaxValueValidator
from user_api.models import MyUser, Profile
from django.db.models import Count
from ordered_model.models import OrderedModel, OrderedModelManager




class Author(models.Model):
    name = models.CharField(# TODO add name validator and expand (name, surname)
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class BookManager(models.Manager):

    def get_queryset(self):
        return Book.objects.filter(is_public=True)



class BookImage(OrderedModel): # TODO add remove images
    img = models.ImageField(
        upload_to='book_images',
    )
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        related_name='image',
    )


class Book(models.Model):
    objects = models.Manager()
    public = BookManager()
    SIMILAR_BOOKS_COUNT = 3
    name = models.CharField(
        max_length=30
    )
    price = models.FloatField(
        default=0
    )
    genre = models.ManyToManyField(
        'Genre',
    )
    img_cover = models.ImageField(
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
        if self.img_cover:
            os.remove(self.img_cover.path)
        super().delete()

    def comments_count(self): # TODO remove? leave on;y source in serializer?
        return self.comment.count()

    # def add_to_favorite(self, user):

    def similar_books(self):
        """Получить QS похожих книг"""
        genres_ids = [genre.pk for genre in self.genre.all()]
        qs = Book.public.select_related('author').prefetch_related('genre').exclude(pk=self.pk).\
                 filter(genre__pk__in=genres_ids).distinct().order_by('?')[:Book.SIMILAR_BOOKS_COUNT]
        if len(qs) < Book.SIMILAR_BOOKS_COUNT:
            exclude_ids = [book.pk for book in qs]
            exclude_ids.append(self.pk)
            qs |= Book.public.exclude(pk__in=exclude_ids)[:Book.SIMILAR_BOOKS_COUNT - len(qs)]
        return qs

    def comments_stars_stat(self):
        """Статистика звезд у коментариев книги"""
        return Comment.stars_stat(self.comment.all())


class Comment(models.Model):
    STAR_MAX_VALUE = 5
    # TODO add star min val
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
        validators=[MaxValueValidator(STAR_MAX_VALUE),]
    )

    class Meta:
        unique_together = ['owner', 'book']

    def __str__(self):
        return f'<Comment:{self.pk}> {self.text}'

    @staticmethod
    def stars_stat(qs):
        if not isinstance(qs, models.QuerySet ):
            raise TypeError('expect QuerySet')
        if qs.model is not Comment:
            raise TypeError('Model of queryset must be Comment')
        stat = qs.values('stars').annotate(count=Count('stars')).order_by('stars')
        result = {star: 0 for star in range(1, Comment.STAR_MAX_VALUE + 1)}
        for star in stat:
            result[star['stars']] = star['count']
        return result

    def dislike_count(self):
        return self.like_set.filter(flag=False).count()

    def like_count(self):
        return self.like_set.filter(flag=True).count()

    def user_like(self, user):  # TODO запедалит на цикле
        try:
            return self.like_set.get(owner=user)
        except Like.DoesNotExist:
            return None

    def set_like(self, user):
        if not isinstance(user, MyUser):
            raise TypeError('user must be MyUser instance')
        like, created = Like.get_or_create(owner=user, comment=self, flag=True)
        like.flag = True
        if not created:
            like.save()
        return like

    def set_dislike(self, user):
        if not isinstance(user, MyUser):
            raise TypeError('user must be MyUser instance')
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
    owner = models.ForeignKey(
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
        unique_together = ['owner', 'book']


    def __str__(self):
        return f'{self.owner}:{self.book}'


class Test(models.Model):  # TODO remove
    name = models.CharField(
        max_length=20,
    )


class Like(models.Model):
    owner = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )
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

class BannerAddManager(OrderedModelManager):

    def get_queryset(self):
        return BannerAdd.objects.filter(is_public=True)

class BannerAdd(OrderedModel):

    objects = OrderedModelManager()
    public = BannerAddManager()

    title = models.CharField(
        max_length=20,
    )
    image = models.ImageField(
        upload_to='banners',
    )
    description = models.TextField(
        blank=True,
    )
    is_public = models.BooleanField(
        default=False,
    )
    add_link = models.URLField(
        blank=True,
    )

# TODO create order class Order, Basket