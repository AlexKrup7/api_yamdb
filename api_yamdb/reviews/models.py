from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
User = get_user_model()


class Categories(models.Model):
    name = models.CharField("", max_length=50)
    slug = models.SlugField(unique=True, default="", db_index=True)


class Genres(models.Model):
    name = models.CharField("", max_length=256)
    slug = models.SlugField(unique=True, default="")


class Titles(models.Model):
    name = models.CharField("", max_length=50)
    year = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    genre = models.ManyToManyField(Genres)
    description = models.TextField(blank=True, null=True, max_length=100)

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self) -> str:
        return self.name
        

class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='titles')
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
