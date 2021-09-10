from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint

# Create your models here.
User = get_user_model()


class Titles(models.Model):
    pass


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
