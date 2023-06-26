from django.db import models

# Create your models here.
class Text(models.Model):
    text = models.CharField(max_length=250)

    class Meta:
        abstract = True


class Note(Text):
    pass


class Record(Text):
    pass