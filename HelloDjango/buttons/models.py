from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()
    genre = models.ManyToManyField('Genre',blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
