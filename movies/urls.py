from django.urls import path, include

from movies.views import (ActorListCreateAPIView,
                          ActorRetrieveUpdateDestroyAPIView)
from movies.routers import (movie_router,
                            create_review_router,
                            create_star_router,
                            list_create_rating_router)


urlpatterns = [
    path('', include(movie_router.urls)),
    path('', include(create_review_router.urls)),  # review
    path('', include(create_star_router.urls)),  # star
    path('', include(list_create_rating_router.urls)),  # rating
    path('actor/', ActorListCreateAPIView.as_view()),
    path('actor/<str:pk>/', ActorRetrieveUpdateDestroyAPIView.as_view())
]
