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

    @property
    def is_employee(self):
        try:
            self.employee
            return True
        except Employee.DoesNotExist:
            return False



class UserAddress(models.Model):
    address = models.CharField(max_length=255)
    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='addresses',
    )


class Profile(models.Model):
    NO_SEX = 'no_sex'
    MAN = 'man'

    WOMAN = 'woman'

    SEX_CHOICE = [
        (WOMAN, 'Не указан'),
        (MAN, 'Мужской'),
        (WOMAN, 'Женский'),
    ]

    owner = models.OneToOneField(
        MyUser,
        primary_key=True,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(  # toDO only leters
        blank=True,
        max_length=50,
    )
    last_name = models.CharField( # toDO only leters
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

    def delete(self, **kwargs):
        raise NotImplementedError



class Position(models.Model):
    id = models.CharField(  # TODo only ascii chars
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



