from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=200)
    birth_year = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1888), MaxValueValidator(2100)]
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )
    director = models.ForeignKey(
        Director, on_delete=models.PROTECT, related_name="movies"
    )
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name="movies")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title