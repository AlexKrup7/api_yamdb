from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from django.db.models import Avg
from users.models import User
from .filters import TitlesFilter
from .serializers import UserSerializer

from .mixins import CustomViewSet
from .serializers import (ReviewSerializer, CommentSerializer)
from .permissions import AdminPermissionOrReadOnly
from rest_framework import mixins, viewsets, filters
from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, \
    TitleSerializerCreate


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class ReviewViewSet(CustomViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class CommentViewSet(CustomViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return Comment.objects.filter(post=post.id)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return serializer.save(author=self.request.user, review=review)


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminPermissionOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminPermissionOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminPermissionOrReadOnly,)
    http_method_names = ['get', 'post', 'delete', 'patch']
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            return TitleSerializerCreate
        return TitleSerializer
