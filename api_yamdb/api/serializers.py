from rest_framework.relations import SlugRelatedField
from rest_framework import serializers
from reviews.models import Review, Comment
from users.models import CHOICES, User
from reviews.models import Category, Genre, Title

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CHOICES, default='user')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerCreate(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
        required=False
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
        required=False, many=True
    )

    class Meta:
        model = Title
        fields = '__all__'
