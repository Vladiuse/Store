from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Genre, MyUser, Profile, Author, Comment, Favorite, Test
from rest_framework.validators import UniqueTogetherValidator


class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Comment.objects.all(),
                fields=['user', 'book']
            )
        ]

    def to_representation(self, instance):
        obj = super().to_representation(instance)
        obj['stars'] = '*' * obj['stars']
        return obj


class BookDetailSerializer(serializers.ModelSerializer):
    # genre = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    author = serializers.StringRelatedField()
    comments_count = serializers.IntegerField(read_only=True)
    comments = serializers.HyperlinkedIdentityField(
        view_name='book-comment-list',
        lookup_url_kwarg='book_id',
        # lookup_field='id'
    )
    is_favorite = serializers.BooleanField(source='favorite', read_only=True)
    add_favorite = serializers.HyperlinkedIdentityField(view_name='book-favorite')

    class Meta:
        model = Book
        fields = '__all__'
        # fields = ['id', 'name', 'price', 'image', 'genre', 'author', 'available_in_store', 'is']


class BookListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='book-detail')
    # genre = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
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

