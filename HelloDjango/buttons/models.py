from django.db import models
import os
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.models import BaseUserManager, UserManager
from django.contrib.auth import get_user_model


class MyUserManager(UserManager):

    def create_user(self, *args,**kwargs):
        user = super().create_user(*args, **kwargs)
        Profile.objects.create(
            first_name=kwargs['first_name'],
            last_name=kwargs['last_name'],
            user=user,
        )
        return user

class MyUser(AbstractUser):
    objects = MyUserManager()


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def delete(self, **kwargs):
        self.user.delete()

    def __str__(self):
        return f'{self.pk} {self.user.username}: {self.first_name}'


class Book(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField(default=0)
    genre = models.ManyToManyField('Genre',blank=True)
    image = models.ImageField(upload_to='book_images', blank=True)

    def __str__(self):
        return self.name

    def delete(self):
        if self.image:
            os.remove(self.image.path)
        super().delete()


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
