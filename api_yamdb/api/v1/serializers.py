from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework.generics import get_object_or_404

from users.models import User

from .utility import (
    generate_confirmation_code,
    send_email_with_confirmation_code,
    username_is_valid
)


class AdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор для Администратора."""
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username', },
        }
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Ошибка в валидации имени с me.')
        return value

    def validate(self, data):
        if not username_is_valid(data.get('username')):
            raise serializers.ValidationError(
                "Неожиданный паттерн"
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    role = serializers.CharField(max_length=15, read_only=True)

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username', },
        }
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Ошибка в валидации имени с me.')
        return value
    
    def validate(self, data):
        if not username_is_valid(data.get('username')):
            raise serializers.ValidationError(
                "Неожиданный паттерн"
            )
        return data


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    """Сериализатор для получения кода подтверждения."""
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            'email',
            'username'
        )
        model = User
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        )

    def create(self, validated_data):
        validated_data['confirmation_code'] = generate_confirmation_code()
        user = User.objects.create_user(**validated_data)
        send_email_with_confirmation_code(validated_data)
        return user

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Ошибка в валидации имени с me.')
        return value

    def validate(self, data):
        if not username_is_valid(data.get('username')):
            raise serializers.ValidationError(
                "Неожиданный паттерн"
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(
        max_length=250,
        write_only=True,
    )
    confirmation_code = serializers.CharField(
        max_length=255,
        write_only=True
    )

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        user_1 = User.objects.filter(
            username=user.username,
            confirmation_code=data['confirmation_code']
        ).exists()
        if not user_1:
            raise serializers.ValidationError(
                'Такого пользователя не существует.'
            )
        return data
