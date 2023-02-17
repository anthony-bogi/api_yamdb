from reviews.models import Category, Genre, Title
from rest_framework import filters, viewsets
from .permissions import (
    IsAdminOrSuperuserPermission,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleSerializerCreate
)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializer
    permission_classes = IsAdminOrSuperuserPermission

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = IsAdminOrSuperuserPermission
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = IsAdminOrSuperuserPermission
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
