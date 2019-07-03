from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Actor(models.Model):
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=6)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=50)
    release_date = models.DateField()
    actors = models.ManyToManyField('MovieCast', related_name='movies')

    def __str__(self):
        return self.title


class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cast = models.ForeignKey(Actor, on_delete=models.CASCADE)
    role = models.CharField(max_length=15)

    def __str__(self):
        return self.role


class MovieRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    avg_rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    no_of_ratings = models.IntegerField()

    def __str__(self):
        return self.avg_rating
