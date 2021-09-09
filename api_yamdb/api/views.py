from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Review, Comment
from rest_framework import filters, permissions, viewsets

from .mixins import CustomViewSet
from .serializers import (ReviewSerializer, CommentSerializer)


class PostViewSet(CustomViewSet):
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
