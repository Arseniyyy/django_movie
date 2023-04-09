from model_bakery import baker
from rest_framework_simplejwt.tokens import RefreshToken

from movies.models import Genre, Movie, Actor, Category, Review, Star, MovieShot, Rating
from users.models import CustomUser


# def create_jwt_token_factory(user):
#     """Creates a jwt token that can be attached to a specific user later."""
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }


def create_user_factory(email="test@example.com", password="12345", is_staff=False):
    user = baker.make(CustomUser, email=email,
                      password=password, is_staff=is_staff)
    return user


def create_category_factory():
    category = baker.make(Category)
    return category


def create_reviews_set(movie):
    reviews = baker.make(Review, movie=movie, _quantity=2)
    return reviews


def create_review_factory(movie, user, parent=None):
    review = baker.make(Review, movie=movie, user=user, parent=parent)
    return review


def create_movie_factory(user):
    """Creates a movie factory with all the relational fields included."""
    actors_set = baker.make(Actor, user=user, _quantity=2)
    movie = baker.make(Movie,
                       actors=actors_set,
                       directors=actors_set)
    return movie


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
