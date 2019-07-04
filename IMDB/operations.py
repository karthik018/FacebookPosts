from .models import *
import random
from django.db.models import F, Sum, FloatField, functions, Count, Q, ExpressionWrapper, DurationField, Max, Avg
from django.db.models import OuterRef, Subquery
from django.db.models.functions import ExtractMonth


def setdata():
    Actor.objects.all().delete()
    actors = [{"id": 1, "name": "Prabhas", "gender": "Male", "birth_date": "1980-05-03"},
              {"id": 2, "name": "Samantha", "gender": "Female", "birth_date": "1980-05-03"},
              {"id": 3, "name": "Naga Chaitanya", "gender": "Male", "birth_date": "1980-05-03"},
              {"id": 4, "name": "Mahesh Babu", "gender": "Male", "birth_date": "1980-05-03"},
              {"id": 5, "name": "Chiranjeevi", "gender": "Male", "birth_date": "1970-01-17"},
              {"id": 6, "name": "Anushka", "gender": "Female", "birth_date": "1985-10-26"},
              {"id": 7, "name": "Kajal Agarwal", "gender": "Female", "birth_date": "1985-06-10"},
              {"id": 8, "name": "Ram Charan", "gender": "Male", "birth_date": "1985-08-10"},
              {"id": 9, "name": "Nani", "gender": "Male", "birth_date": "1985-04-10"},
              {"id": 10, "name": "Ravi Teja", "gender": "Male", "birth_date": "1981-03-10"},
              {"id": 11, "name": "Vijay Devarakonda", "gender": "Male", "birth_date": "1987-07-14"},
              {"id": 12, "name": "Bhrahmanandam", "gender": "Male", "birth_date": "1965-04-13"},
              {"id": 13, "name": "Allari Naresh", "gender": "Male", "birth_date": "1985-10-10"},
              {"id": 14, "name": "Pooja Hegde", "gender": "Female", "birth_date": "1987-02-13"},
              {"id": 15, "name": "Allu Arjun", "gender": "Male", "birth_date": "1983-01-08"},
              {"id": 16, "name": "Shruthi Hassan", "gender": "Female", "birth_date": "1986-07-18"},
              {"id": 17, "name": "Dhanush", "gender": "Male", "birth_date": "1984-03-26"},
              {"id": 18, "name": "Raana", "gender": "Male", "birth_date": "1981-05-16"}]

    Actor.objects.bulk_create(Actor(**values) for values in actors)

    Movie.objects.all().delete()
    movies = [{"id": 1, "title": "B", "release_date": "2018-05-26"},
              {"id": 2, "title": "D", "release_date": "2017-11-23"},
              {"id": 3, "title": "E", "release_date": "2016-01-12"},
              {"id": 4, "title": "C", "release_date": "2019-01-09"},
              {"id": 5, "title": "A", "release_date": "2019-05-04"},
              {"id": 6, "title": "S", "release_date": "2019-05-05"},
              {"id": 7, "title": "I", "release_date": "2015-10-03"},
              {"id": 8, "title": "F", "release_date": "2016-03-10"},
              {"id": 9, "title": "V", "release_date": "2012-02-13"},
              {"id": 10, "title": "R", "release_date": "2012-04-26"},
              {"id": 11, "title": "K", "release_date": "2013-10-26"},
              {"id": 12, "title": "M", "release_date": "2019-05-17"},
              {"id": 13, "title": "Bi", "release_date": "2012-09-09"},
              {"id": 14, "title": "Ma", "release_date": "2014-03-03"},
              {"id": 15, "title": "Y", "release_date": "2018-09-26"}]

    Movie.objects.bulk_create(Movie(**values) for values in movies)

    MovieCast.objects.all().delete()
    movie_cast = [{"id": 1, "movie_id": 1, "cast_id": 1, "role": "Hero"},
                   {"id": 2, "movie_id": 1, "cast_id": 6, "role": "Heroine"},
                   {"id": 3, "movie_id": 2, "cast_id": 17, "role": "Hero"},
                   {"id": 4, "movie_id": 2, "cast_id": 16, "role": "Heroine"},
                   {"id": 5, "movie_id": 3, "cast_id": 15, "role": "Hero"},
                   {"id": 6, "movie_id": 3, "cast_id": 14, "role": "Heroine"},
                   {"id": 7, "movie_id": 4, "cast_id": 4, "role": "Hero"},
                   {"id": 8, "movie_id": 4, "cast_id": 13, "role": "Hero"},
                   {"id": 9, "movie_id": 4, "cast_id": 14, "role": "Heroine"},
                   {"id": 10, "movie_id": 5, "cast_id": 4, "role": "Hero"},
                   {"id": 11, "movie_id": 5, "cast_id": 7, "role": "Heroine"},
                   {"id": 12, "movie_id": 6, "cast_id": 4, "role": "Hero"},
                   {"id": 13, "movie_id": 6, "cast_id": 6, "role": "Heroine"},
                   {"id": 14, "movie_id": 7, "cast_id": 15, "role": "Hero"},
                   {"id": 15, "movie_id": 7, "cast_id": 16, "role": "Heroine"},
                   {"id": 16, "movie_id": 8, "cast_id": 10, "role": "Hero"},
                   {"id": 17, "movie_id": 8, "cast_id": 7, "role": "Heroine"},
                   {"id": 18, "movie_id": 9, "cast_id": 10, "role": "Hero"},
                   {"id": 19, "movie_id": 9, "cast_id": 6, "role": "Heroine"},
                  {"id": 20, "movie_id": 10, "cast_id": 9, "role": "Hero"},
                  {"id": 21, "movie_id": 10, "cast_id": 2, "role": "Heroine"},
                  {"id": 22, "movie_id": 11, "cast_id": 3, "role": "Hero"},
                  {"id": 23, "movie_id": 11, "cast_id": 2, "role": "Heroine"},
                  {"id": 24, "movie_id": 12, "cast_id": 1, "role": "Hero"},
                  {"id": 25, "movie_id": 12, "cast_id": 7, "role": "Heroine"},
                  {"id": 26, "movie_id": 1, "cast_id": 18, "role": "Villan"},
                  {"id": 27, "movie_id": 13, "cast_id": 1, "role": "Hero"},
                  {"id": 28, "movie_id": 13, "cast_id": 6, "role": "Heroine"},
                  {"id": 29, "movie_id": 14, "cast_id": 3, "role": "Hero"},
                  {"id": 30, "movie_id": 14, "cast_id": 2, "role": "Heroine"},
                  {"id": 31, "movie_id": 15, "cast_id": 3, "role": "Hero"},
                  {"id": 32, "movie_id": 15, "cast_id": 2, "role": "Heroine"}]
    MovieCast.objects.bulk_create(MovieCast(**values) for values in movie_cast)

    MovieRating.objects.all().delete()
    ratings = []
    x = 1
    for i in range(1, len(movies) + 1):
        for j in range(1, 6):
            data = {
                "id": x,
                "movie_id": i,
                "rating_number": j,
                "no_of_ratings": random.randint(1, 50)
            }
            x += 1
            ratings.append(data)
    MovieRating.objects.bulk_create(MovieRating(**values) for values in ratings)


def top_ten_movies_with_top_avg_rating():
    ratings = MovieRating.objects.values('movie_id', 'movie__title').annotate(
        average=functions.Cast(Sum(F('rating_number') * F('no_of_ratings') * 1.0) / Sum(F('no_of_ratings')),
                               output_field=FloatField())).order_by('-average')[:10]
    top_ten_movies = []
    for movie in ratings:
        top_ten_movies.append(movie['movie__title'])
    return top_ten_movies


def get_top_5_least_5_actors():
    no_of_movies = MovieCast.objects.values('cast_id').annotate(movies=Count(F('movie_id'))).order_by('-movies')
    actors_list = list(no_of_movies)
    top_5_actors = actors_list[:5]
    least_5_actors = actors_list[-5:]
    return top_5_actors, least_5_actors


def get_movies_with_star_month():
    star_month = MovieCast.objects.filter(movie_id=OuterRef('movie_id')).values('cast__birth_date__month').annotate(
        count=Count('cast__birth_date__month')).values_list('cast__birth_date__month', flat=True).order_by('-count',
                                                                                                           'cast__birth_date__month')
    star_months = MovieCast.objects.values('movie_id', 'cast__birth_date__month').annotate(count=Count('id'),
                                                                                           star_month=Subquery(
                                                                                               star_month[:1])).filter(
        movie__release_date__month=F('star_month'), cast__birth_date__month=F('star_month')).order_by('-count')
    return list(star_months)


def get_movies_released_in_birth_month_of_actor():
    actor_movies = MovieCast.objects.values('cast_id').annotate(count=Count('movie_id'),
                                                                actor_month=ExtractMonth('cast__birth_date'),
                                                                movie_month=ExtractMonth('movie__release_date')).filter(
        movie__release_date__month=F('actor_month')).values('cast_id', 'count')
    return list(actor_movies)


def get_difference_of_one_star_five_star_ratings_for_each_actor():
    movie_rating_difference = MovieRating.objects.filter(movie_id=OuterRef('movie_id')).values('movie_id').annotate(
        one_star=Sum('no_of_ratings', filter=Q(rating_number=1)),
        five_star=Sum('no_of_ratings', filter=Q(rating_number=5)), difference=F('one_star') - F('five_star')).values(
        'difference')
    actors = MovieCast.objects.annotate(difference=Subquery(movie_rating_difference)).values('cast_id').annotate(
        difference_sum=Sum('difference')).order_by('-difference_sum')
    return list(actors)


def get_youngest_actors_of_all_movies():
    youngest_actors = MovieCast.objects.filter(movie_id=OuterRef('id')).values('movie_id').annotate(
        age=ExpressionWrapper(F('movie__release_date') - F('cast__birth_date'), output_field=DurationField())).order_by(
        'age').values('age')[:1]
    movies = Movie.objects.annotate(young_actor=Subquery(youngest_actors)).values('id', 'young_actor').order_by(
        'young_actor')[:10]
    return list(movies)


def get_year_in_which_most_cast_movies_released():
    casts_count_in_movie_year = MovieCast.objects.values('movie__release_date__year').annotate(cast_count=Count('cast_id')).order_by('-cast_count').values('movie__release_date__year')[:1]
    return list(casts_count_in_movie_year)


def get_twin_stars():
    movies = MovieCast.objects.filter(movie__moviecast__movie_id=F('movie_id')).annotate(
        second_cast_id=F('movie__moviecast__cast_id')).exclude(cast_id=F('second_cast_id')).filter(
        cast_id__lt=F('second_cast_id')).values('cast_id', 'second_cast_id').annotate(count=Count('id'))
    max_count = movies.aggregate(Max('count'))
    cast = movies.filter(count=max_count['count__max'])
    return list(cast)


def get_top_youngest_oldest_movies():
    cast_age = MovieCast.objects.values('movie_id').annotate(cast_avg_age=Avg(
        ExpressionWrapper((F('movie__release_date') - F('cast__birth_date')), output_field=DurationField())))
    youngest_movies = cast_age.values('movie_id').order_by('cast_avg_age')[:5]
    oldest_movies = cast_age.values('movie_id').order_by('-cast_avg_age')[:5]
    return list(youngest_movies), list(oldest_movies)
