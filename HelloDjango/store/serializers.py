from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Genre, Author, Comment, Favorite, Test, Like
from rest_framework.validators import UniqueTogetherValidator
from user_api.models import MyUser, Profile


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(source='user.username', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='comments-detail')
    like_count = serializers.IntegerField(read_only=True)
    dislike_count = serializers.IntegerField(read_only=True)
    like = serializers.HyperlinkedIdentityField(view_name='comments-like')
    dislike = serializers.HyperlinkedIdentityField(view_name='comments-dislike')
    user_like = serializers.SerializerMethodField('get_user', read_only=True)

    def get_user(self, obj):
        user = self.context.get('request').user
        user_like = obj.user_like(user)
        if user_like:
            return LikeSerializer(obj.user_like(user)).data
        return None

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True},
            'book': {'read_only': True},
        }

    def to_representation(self, instance):
        obj = super().to_representation(instance)
        obj['stars'] = '*' * obj['stars']
        return obj


class BookDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments_count = serializers.IntegerField(read_only=True)
    comments = serializers.HyperlinkedIdentityField(
        view_name='book-comment-list',
        lookup_url_kwarg='book_id',
    )
    is_favorite = serializers.BooleanField(source='favorite', read_only=True)
    add_favorite = serializers.HyperlinkedIdentityField(view_name='book-favorite')

    class Meta:
        model = Book
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='book-detail')
    class Meta:
        model = Book
        exclude = ['description']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='profile-detail')
    class Meta:
        model = Profile
        fields = ['owner','first_name', 'last_name', 'age', 'sex', 'url']
        extra_kwargs = {
            'owner': {'read_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'is_staff', 'profile', 'date_joined']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class TestSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Test
        fields = '__all__'


