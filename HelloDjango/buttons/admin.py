from django.contrib import admin
from .models import Book, Genre, Profile
from .models import MyUser


admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(MyUser)
admin.site.register(Profile)
