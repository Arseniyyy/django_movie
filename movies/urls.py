from django.urls import path
from movies.views import (
    ActorListCreateAPIView,
    ActorRetrieveUpdateDestroyAPIView,
    GenreListCreateAPIView,
    ReviewListCreateAPIView,
    ReviewRetrieveUpdateDestroyAPIView,
    MovieRetrieveUpdateDestroyAPIView,
    MovieListCreateViewSet,
    RatingListCreateViewSet,
)

movie_list_create_view = MovieListCreateViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    path('movie/', movie_list_create_view, name='movie_list_create'),
    path('movie/<int:pk>/', MovieRetrieveUpdateDestroyAPIView.as_view(), name='movie_detail'),
    path('review/', ReviewListCreateAPIView.as_view(), name='review'),
    path('review/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review_detail'),
    path('actor/', ActorListCreateAPIView.as_view(), name='actor'),
    path('actor/<str:name>/', ActorRetrieveUpdateDestroyAPIView.as_view(), name='actor_detail'),
    path('genre/', GenreListCreateAPIView.as_view(), name='genre'),
    path('rating/', RatingListCreateViewSet.as_view({'get': 'list',
                                                     'post': 'create',
                                                     'patch': 'update'})),
]
