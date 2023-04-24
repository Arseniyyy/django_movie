import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.db import models
from django.urls import reverse
from datetime import date

from users.models import CustomUser
from movies.abstract_models import CommonInfo


class Category(CommonInfo):
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Actor(CommonInfo):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    age = models.PositiveSmallIntegerField("age", default=0)
    image = models.ImageField("picture", upload_to="actors/")
    first_creation_time = models.DateTimeField(
        auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='user who created this actor', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Gets a url for a specified actor instance."""
        return reverse('actor_detail', kwargs={"name": self.name})

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actors"


class Genre(CommonInfo):
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
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

    def __str__(self):
        return f'{self.title} - {self.year}'

    def get_absolute_url(self):
        """Gets a url for a specified movie instance."""
        return reverse('movie_detail', kwargs={"pk": self.id})


class MovieShot(models.Model):
    "Movie picture"
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description')
    image = models.ImageField('Image', upload_to="movie_shots/")
    movie = models.ForeignKey(
        Movie, verbose_name='Movie', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Rating(models.Model):
    ip = models.CharField('IP address', max_length=15)
    movie = models.ForeignKey(
        Movie, verbose_name='Movie', related_name='ratings', on_delete=models.CASCADE)
    star = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    def __str__(self) -> str:
        return f"{self.star} - {self.movie}"


class Review(models.Model):
    "Comments and reviews"
    name = models.CharField('name', max_length=100)
    text = models.TextField('message', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='parent', related_name='children',
                               on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(
        Movie, verbose_name='movie', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, related_name="reviews", on_delete=models.CASCADE, default=1)

    def __str__(self) -> str:
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name_plural = 'Reviews'
