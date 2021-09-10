from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, CategoryViewSet, GenreViewSet, TitleViewSet, CommentViewSet, ReviewViewSet
from .views import APIRegistration, APIToken, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='review')
router_v1.register(r'titles/(?P<title_id>\d+)/(?P<review_id>\d+)/comments',
                   CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APIRegistration.as_view()),
    path('v1/auth/token/', APIToken.as_view())
]
