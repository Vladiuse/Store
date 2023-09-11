from django.contrib import admin
from .models import Book, Genre, Author, Favorite, Comment, \
    Test, BannerAdd
from user_api.models import MyUser, Profile
from ordered_model.admin import OrderedModelAdmin

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Profile)
admin.site.register(Author)
admin.site.register(Favorite)
admin.site.register(Comment)
admin.site.register(Test)



class MyUserAdmin(admin.ModelAdmin):
    list_filter = ['is_staff', 'is_superuser']

class BannerAddAdmin(OrderedModelAdmin):
    list_display = ['id', 'title','is_public', 'add_link','move_up_down_links']

admin.site.register(MyUser,MyUserAdmin)
admin.site.register(BannerAdd,BannerAddAdmin)
