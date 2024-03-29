# Generated by Django 2.2.3 on 2019-07-03 09:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=6)),
                ('birth_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('release_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='MovieRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('no_of_ratings', models.IntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDB.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='MovieCast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=15)),
                ('cast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDB.Actor')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMDB.Movie')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(through='IMDB.MovieCast', to='IMDB.Actor'),
        ),
    ]
