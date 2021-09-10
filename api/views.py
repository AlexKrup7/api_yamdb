from django.shortcuts import render
from .permissions import AdminPermissionOrReadOnly
from rest_framework import mixins, viewsets, filters
from reviews.models import Categories, Genres, Titles
from .serializers import CategorySerializer,\
    GenreSerializer,\
    TitleSerializer,\
    TitleSerializerCreate


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminPermissionOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminPermissionOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    permission_classes = (AdminPermissionOrReadOnly,)
    http_method_names = ['get', 'post', 'delete', 'patch']
    #filterset_class =
    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            return TitleSerializerCreate
        return TitleSerializer
