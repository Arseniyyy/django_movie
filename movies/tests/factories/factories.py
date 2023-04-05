from model_bakery import baker
from rest_framework_simplejwt.tokens import RefreshToken

from movies.models import Movie, Actor, Category, Review
from users.models import CustomUser


# def create_jwt_token_factory(user):
#     """Creates a jwt token that can be attached to a specific user later."""
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }


def create_user_factory():
    user = baker.make(CustomUser)
    return user


def create_category_factory():
    category = baker.make(Category)
    return category


def create_reviews_set(movie):
    reviews = baker.make(Review, movie=movie, _quantity=2)
    return reviews


def create_movie_factory(user, category):
    """Creates a movie factory with all the relational fields included."""
    actors_set = baker.make(Actor, user=user, _quantity=2)
    movie = baker.make(Movie,
                       category=category,
                       actors=actors_set,
                       directors=actors_set)
    return movie


def create_actor_factory():
    user = baker.make(CustomUser)
    return baker.make(Actor, user=user)


def create_category_factory():
    return baker.make(Category)
