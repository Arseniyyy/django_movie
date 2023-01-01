from django.urls import path, include

from movies.views import (MovieViewSet,
                          ReviewViewSet,
                          CreateStarViewSet,
                          ListCreateRatingViewSet,
                          ListCreateActorViewSet)
from movies.routers import (movie_router,
                            create_review_router,
                            create_star_router,
                            list_create_rating_router,
                            list_create_actor_router)


movie_router.register(r'movie', MovieViewSet)
create_review_router.register(r'review', ReviewViewSet)
create_star_router.register(r'star', CreateStarViewSet)
list_create_rating_router.register(r'rating', ListCreateRatingViewSet)
list_create_actor_router.register(r'actor', ListCreateActorViewSet)


urlpatterns = [
    path('', include(movie_router.urls)),  # movie
    path('', include(create_review_router.urls)),  # review
    path('', include(create_star_router.urls)),  # star
    path('', include(list_create_rating_router.urls)),  # rating
    path('', include(list_create_actor_router.urls)),  # actor
]
