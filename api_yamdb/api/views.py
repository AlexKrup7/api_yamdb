import random
import string

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .filters import TitlesFilter
from .mixins import CustomViewSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsOwnerOrModeratorOrAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegistrationSerializer,
                          ReviewSerializer, TitleSerializer,
                          TitleSerializerCreate, TokenSerializer,
                          UserSerializer)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'token': str(refresh.access_token),
    }


class APIRegistration(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=10))
            serializer.save(confirmation_code=confirmation_code, role='user')
            send_mail('Confirmation code',
                      f'Your confirmation code is {confirmation_code}',
                      'YaMDB', [serializer.validated_data['email']])
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=serializer.validated_data['username'])
            if user.confirmation_code == serializer.validated_data[
                    'confirmation_code']:
                return Response(get_tokens_for_user(user),
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)

    @action(methods=['GET', 'PATCH'], detail=False,
            url_path='me', permission_classes=[permissions.IsAuthenticated])
    def get_info_by_token(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(CustomViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = (IsOwnerOrModeratorOrAdminOrReadOnly,)


class CommentViewSet(CustomViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrModeratorOrAdminOrReadOnly,)

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
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'delete', 'patch']
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            return TitleSerializerCreate
        return TitleSerializer
