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
    actors = models.ManyToManyField('Actor', through='MovieCast')

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
    rating_number = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    no_of_ratings = models.IntegerField()

    def __str__(self):
        return str(self.movie.title)
