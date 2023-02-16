from rest_framework.routers import SimpleRouter
from django.urls import include, path

from api.views import ReviewViewSet, CommentViewSet

router = SimpleRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
urlpatterns = [
    path('', include(router.urls)),
]
