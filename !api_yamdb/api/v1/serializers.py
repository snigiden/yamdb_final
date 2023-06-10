from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import SCORES, Category, Comment, Genre, Review, Title
from users.models import User

from .validators import username_validator


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    rating = serializers.IntegerField(read_only=True)
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = (
            'name',
            'year',
            'category',
            'genre',
            'rating',
            'description',
            'id',
        )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[username_validator],
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )

    def validate(self, data):
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким именем уже зарегистрирован'
            )
        return data


class RegisterSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )

    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    def validate(self, data):
        username = data['username']
        if username == 'me':
            raise serializers.ValidationError(
                {'Недопустимое имя пользователя'}
            )
        return data


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if default_token_generator.check_token(
            user,
            data['confirmation_code']
        ):
            return data
        raise serializers.ValidationError(
            {'confirmation_code': 'Неверный код подтверждения'}
        )


class ReviewsSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='id',
        many=False,
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    score = serializers.ChoiceField(choices=SCORES)

    class Meta:
        fields = (
            'id',
            'title',
            'text',
            'author',
            'score',
            'pub_date',
        )
        model = Review

    def validate(self, data):
        title_id = self.context['request'].parser_context[
            'kwargs'
        ].get('title_id')
        author = self.context['request'].user
        title = get_object_or_404(Title, id=title_id)
        if (
            self.context['request'].method == 'POST'
            and title.reviews.filter(author=author).exists()
        ):
            raise serializers.ValidationError(
                'Вы не можете оставить более одного отзыва'
            )
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = (
            'review',
            'text',
            'author',
            'pub_date',
            'id',
        )
        model = Comment
        read_only_fields = ('review', )


class ReadTitleSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer(required=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
