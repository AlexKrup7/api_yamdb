# Generated by Django 2.2.16 on 2021-09-11 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'Аутентифицированный пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='user', max_length=10, verbose_name='user role'),
        ),
    ]