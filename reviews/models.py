from django.db import models


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
