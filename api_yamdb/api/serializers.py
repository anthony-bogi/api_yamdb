from rest_framework import serializers
from titles.models import Review, Comment, Title
from users.models import User
from rest_framework.validators import UniqueTogetherValidator


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели отзывов.
    """
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        queryset=Title.objects.all(),
        slug_field='title',
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('id', 'author', 'title', 'created')
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели комментариев.
    """
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    review = serializers.SlugRelatedField(
        queryset=Review.objects.all(),
        slug_field='review',
    )

    class Meta:
        model = Comment
        read_only_fields = ('id', 'author', 'review', 'created')
        fields = '__all__'
