from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint

from users.models import User


class Category(models.Model):
    name = models.CharField("", max_length=50)
    slug = models.SlugField(unique=True, default="", db_index=True)


class Genre(models.Model):
    name = models.CharField("", max_length=256)
    slug = models.SlugField(unique=True, default="")


class Title(models.Model):
    name = models.CharField("", max_length=50)
    year = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    description = models.TextField(blank=True, null=True, max_length=100)

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='titles')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(score__range=(0, 10)), name='valid_score'),
            UniqueConstraint(fields=['author', 'title'], name='rating_once')
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
