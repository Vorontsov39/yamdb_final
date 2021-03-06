from datetime import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import UserProfile


class ProfileRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=UserProfile.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=UserProfile.objects.all())]
    )

    class Meta:
        model = UserProfile
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Запрещено {value} использовать'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    confirmation_code = serializers.CharField(max_length=150, required=True)


class TokenRestoreSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(max_length=150, required=True)


class ProfileSerializerAdmin(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=UserProfile.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=UserProfile.objects.all())]
    )

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=UserProfile.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=UserProfile.objects.all())]
    )
    role = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        exclude = ('title',)

    def create(self, validated_data):
        view = self.context['view']
        title = get_object_or_404(Title, id=view.kwargs.get('title_id'))
        if Review.objects.filter(author=self.context['request'].user,
                                 title=title).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение'
            )
        return Review.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def year_validator(self, value):
        if value > datetime.now().year:
            raise ValidationError(
                ('%(value)s is not a correcrt year!'),
                params={'value': value},
            )


class TitleSerializerCreate(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=False,
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'
