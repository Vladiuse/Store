from rest_framework import serializers
from .models import Book, Genre, Author, Comment, Favorite, Test, Like, BannerAdd, BookImage, Basket
from ordered_model.serializers import OrderedModelSerializer
from rest_framework.validators import UniqueTogetherValidator


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class CurrentBook:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['book']

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(source='user.username', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail', )
    like_count = serializers.IntegerField(read_only=True)
    dislike_count = serializers.IntegerField(read_only=True)
    like = serializers.HyperlinkedIdentityField(view_name='comment-like')
    dislike = serializers.HyperlinkedIdentityField(view_name='comment-dislike')
    user_like = serializers.SerializerMethodField('get_user', read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    book = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentBook(), )

    def get_user(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            user_like = obj.user_like(request.user)
            if user_like:
                return LikeSerializer(obj.user_like(request.user)).data
        return None

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True},
            'book': {'read_only': True},
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Comment.objects.all(),
                fields=['owner', 'book']
            )
        ]

    # def to_representation(self, instance):
    #     obj = super().to_representation(instance)
    #     obj['stars'] = '*' * obj['stars']
    #     return obj


class CommentDetailSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['pk', 'text', 'stars', 'book', 'owner']
        extra_kwargs = {
            'owner': {'read_only': True},
            'book': {'read_only': True},
        }


class BookImageSerializer(OrderedModelSerializer):
    class Meta:
        model = BookImage
        fields = '__all__'


class BookPrideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['price']


class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    author = AuthorSerializer()
    comments_count = serializers.IntegerField(read_only=True)
    comments_stars_stat = serializers.DictField(read_only=True)
    comments = serializers.HyperlinkedIdentityField(
        view_name='book-comment-list',
        lookup_url_kwarg='book_id',
    )
    is_favorite = serializers.BooleanField(source='favorite', read_only=True)
    add_favorite = serializers.HyperlinkedIdentityField(view_name='book-favorite')
    similar_books = serializers.HyperlinkedIdentityField(view_name='book-similar-books')
    images = BookImageSerializer(many=True, source='image', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='book-detail')
    genre = GenreSerializer(many=True, )
    author = AuthorSerializer()

    class Meta:
        model = Book
        exclude = ['description']
class BookCreateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='book-detail')
    genre = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = '__all__'

    def validate_genre(self,value):
        print(value, type(value))
        if not value:
            raise serializers.ValidationError("Genre cant be empty")
        return value
class TestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class BannerAddSerializer(OrderedModelSerializer):
    class Meta:
        model = BannerAdd
        fields = '__all__'


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = '__all__'
        extra_kwargs = {
            'created': {'read_only': True},
            'book': {'read_only': True},
            'owner': {'read_only': True},
        }
