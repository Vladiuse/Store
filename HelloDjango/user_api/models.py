from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.models import BaseUserManager, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator

class MyUserManager(UserManager):

    def create_user(self, *args, **kwargs):
        user = super().create_user(*args, **kwargs)
        Profile.objects.create(
            owner=user,
        )
        return user

    def create_superuser(self, *args, **kwargs):
        user = super().create_superuser(*args, **kwargs)
        Profile.objects.create(owner=user)
        return user


class MyUser(AbstractUser):
    objects = MyUserManager()


class Profile(models.Model):
    NO_SEX = 'no_sex'
    MAN = 'man'
    WOMAN = 'woman'

    SEX_CHOICE = [
        (MAN, 'Мужской'),
        (WOMAN, 'Женский'),
    ]

    owner = models.OneToOneField(
        MyUser,
        primary_key=True,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(
        blank=True,
        max_length=50,
    )
    last_name = models.CharField(
        blank=True,
        max_length=50,
    )
    age = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(13), MaxValueValidator(120)],
    )
    sex = models.CharField(
        max_length=6,
        blank=True,
        choices=SEX_CHOICE,
        default=NO_SEX,
    )
    address = models.CharField(
        max_length=150,
        blank=True,
    )

    def delete(self, **kwargs):
        raise ZeroDivisionError

    def __str__(self):
        return f'{self.pk} {self.user.username}: {self.first_name}'


