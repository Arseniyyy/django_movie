from django.urls import path
from movies.views import (
    ActorListCreateAPIView,
    ActorRetrieveUpdateDestroyAPIView,
    GenreListCreateAPIView,
    ReviewListCreateAPIView,
    ReviewRetrieveUpdateDestroyAPIView,
    MovieRetrieveUpdateDestroyAPIView,
    MovieListCreateViewSet,
    RatingListCreateViewSet
)

movie_list_create_view = MovieListCreateViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('movie/', movie_list_create_view),
    path('movie/<int:pk>/', MovieRetrieveUpdateDestroyAPIView.as_view(),
         name='movie-detail'),
    path('review/', ReviewListCreateAPIView.as_view()),
    path('review/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view()),
    path('actor/', ActorListCreateAPIView.as_view()),
    path('actor/<str:name>/', ActorRetrieveUpdateDestroyAPIView.as_view(),
         name='actor-detail'),
    path('genre/', GenreListCreateAPIView.as_view()),
    path('rating/', RatingListCreateViewSet.as_view({'get': 'list',
                                                    'post': 'create'})),
]
