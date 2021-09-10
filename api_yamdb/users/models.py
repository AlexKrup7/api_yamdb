from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class UserRole:
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    choices = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )


class User(AbstractUser):
    role = models.CharField(
<<<<<<< HEAD
        max_length=10, choices=UserRole.choices, verbose_name='user role',
        default=UserRole.USER)
=======
        blank=True, max_length=10, verbose_name='user role')
>>>>>>> users
    bio = models.TextField(blank=True, null=True, verbose_name='biography')
    first_name = models.CharField(
        blank=True, max_length=150, verbose_name='first name')
    email = models.EmailField(
        blank=False, unique=True, max_length=254, verbose_name='email address')
<<<<<<< HEAD
=======
    confirmation_code = models.CharField(
        blank=True, max_length=10, verbose_name='confirmation code')
>>>>>>> users
