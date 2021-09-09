from django.urls import include, path
from rest_framework import routers
from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router_ver1 = routers.DefaultRouter()
router_ver1.register(r'genres', GenreViewSet, basename='genre')
router_ver1.register(r'categories', CategoryViewSet, basename='category')
router_ver1.register(r'titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router_ver1.urls)),
]
