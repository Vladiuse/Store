from django.contrib import admin
from .models import Book, Genre, Profile, Author, Favorite, Comment
from .models import MyUser


admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(MyUser)
admin.site.register(Profile)
admin.site.register(Author)
admin.site.register(Favorite)
admin.site.register(Comment)
