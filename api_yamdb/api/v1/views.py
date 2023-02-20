from rest_framework import filters, viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings

from users.models import User
from .permissions import (
    IsAdminOrSuperuserPermission,
)
from .serializers import (
    AdminUserSerializer,
    UserSerializer,
    ConfirmationCodeSerializer,
    TokenSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """Работа с пользователями для администратора."""
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrSuperuserPermission,
    )
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_serializer_class(self):
        if (self.request.user.role != 'admin'
            or self.request.user.is_superuser):
            return UserSerializer
        return AdminUserSerializer

    @action(
        detail=False,
        url_path='me',
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated, ],
        queryset=User.objects.all()
    )
    def me(self, request):
        """
        Профиль пользователя с редактированием.
        Поле role редактирует только администратор.
        """
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    if User.objects.filter(username=request.data.get('username'),
                           email=request.data.get('email')).exists():
        user, created = User.objects.get_or_create(
            username=request.data.get('username')
        )
        if created is False:
            confirmation_code = default_token_generator.make_token(user)
            user.confirmation_code = confirmation_code
            user.save()
            return Response('Ваш токен обновлен!', status=status.HTTP_200_OK)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.get(username=request.data.get('username'),
                            email=request.data.get('email'))
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    send_mail(f'Привет, {str(user.username)}! Ваш код подтверждения:',
              confirmation_code,
              settings.MAILING_EMAIL,
              [request.data['email']],
              fail_silently=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST', ])
def token(request):
    """Получить токен."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    user = get_object_or_404(User, **data)
    refresh = RefreshToken.for_user(user)
    return Response(
        {'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED
    )
