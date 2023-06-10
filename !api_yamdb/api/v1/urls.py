from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentsViewSet, GenresViewSet,
                    ReviewsViewSet, TitlesViewSet, UserViewSet, get_token,
                    signup)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments',
)
router.register('titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', get_token, name='token'),
]
