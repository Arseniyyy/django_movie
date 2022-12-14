from datetime import date

from django.db import models
from django.urls import reverse

import uuid


class Category(models.Model):
    name = models.CharField("category", max_length=150)
    description = models.TextField("description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Actor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("name", max_length=100)
    age = models.PositiveSmallIntegerField("age", default=0)
    description = models.TextField("description")
    image = models.ImageField("picture", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actors"


class Genre(models.Model):
    name = models.CharField('name', max_length=100)
    description = models.TextField('description')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    title = models.CharField('Title', max_length=100)
    tagline = models.CharField('Tagline', max_length=100, default='')
    description = models.TextField('Description')
    poster = models.ImageField(
        'Poster', upload_to="movies/", blank=True, null=True)
    year = models.PositiveSmallIntegerField('Year', default=2022)
    country = models.CharField('Country', max_length=30)
    directors = models.ManyToManyField(Actor,
                                       verbose_name='Director',
                                       related_name='movie_director')
    actors = models.ManyToManyField(Actor,
                                    verbose_name='Actors',
                                    related_name='movie_actor')
    genres = models.ManyToManyField(Genre,
                                    verbose_name='Genres',
                                    related_name='movie_genre')
    world_premiere = models.DateField('World premiere', default=date.today)
    budget = models.PositiveIntegerField('Budget',
                                         default=0,
                                         help_text='type the sum in dollars')
    fees_in_usa = models.PositiveIntegerField('Fees in USA',
                                              default=0,
                                              help_text='type the sum in dollars')
    fees_in_world = models.PositiveIntegerField('Fees in the world',
                                                default=0,
                                                help_text='type the sum in dollars')
    category = models.ForeignKey(Category,
                                 verbose_name='Category',
                                 on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    is_draft = models.BooleanField('Is draft', default=False)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent_isnull=True)


class MovieShot(models.Model):
    "Movie picture"
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description')
    image = models.ImageField('Image', upload_to="movie_shots/")
    movie = models.ForeignKey(
        Movie, verbose_name='Movie', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class RatingStar(models.Model):
    value = models.SmallIntegerField('Value', default=0)

    def __str__(self) -> str:
        return f"{self.value}"


class Rating(models.Model):
    ip = models.CharField('IP address', max_length=15)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, verbose_name='Movie', related_name='ratings')
    star = models.ForeignKey(
        RatingStar, on_delete=models.CASCADE, verbose_name='Star')

    def __str__(self) -> str:
        return f"{self.star} - {self.movie}"


class Review(models.Model):
    "Comments and reviews"
    email = models.EmailField()
    name = models.CharField('name', max_length=100)
    text = models.TextField('message', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='parent', related_name='children',
                               on_delete=models.SET_NULL, blank=True,
                               null=True)
    movie = models.ForeignKey(
        Movie, verbose_name='movie', related_name='reviews', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
