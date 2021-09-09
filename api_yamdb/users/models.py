from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    role = models.CharField(max_length=10, choices=CHOICES)
    bio = models.TextField(blank=True, null=True, verbose_name='Биография')
