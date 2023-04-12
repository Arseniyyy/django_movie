from model_bakery import baker
from rest_framework_simplejwt.tokens import RefreshToken

from movies.models import Genre, Movie, Actor, Category, Review, Star, MovieShot, Rating
from users.models import CustomUser


def create_user_factory(email="test@example.com", password="12345", is_staff=False):
    user = baker.make(CustomUser, email=email,
                      password=password, is_staff=is_staff)


def create_category_factory():
    return baker.make(Category)


def create_reviews_set(movie):
    return baker.make(Review, movie=movie, _quantity=2)


def create_review_factory(movie, user, parent=None):
    return baker.make(Review, movie=movie, user=user, parent=parent)


def create_movie_factory(user):
    """Creates a movie factory with all the relational fields included."""
    actors_set = baker.make(Actor, user=user, _quantity=2)
    return baker.make(Movie,
                      actors=actors_set,
                      directors=actors_set)


def create_actor_factory():
    user = baker.make(CustomUser)
    return baker.make(Actor, user=user)


def create_category_factory():
    return baker.make(Category)


def create_star_factory():
    return baker.make(Star)


def create_genre_factory():
    return baker.make(Genre)


def create_movieshot_factory(movie: Movie):
    return baker.make(MovieShot, movie=movie)


def create_rating_factory(movie: Movie, star: Star):
    return baker.make(Rating, movie=movie, star=star)
