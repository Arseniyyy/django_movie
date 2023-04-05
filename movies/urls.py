from django.urls import path

from movies.views import (ActorListCreateAPIView,
                          ActorRetrieveUpdateDestroyAPIView,
                          GenreListCreateAPIView,
                          ReviewListAPIView,
                          ReviewCreateAPIView,
                          MovieRetrieveUpdateDestroyAPIView,
                          MovieListCreateViewSet,)


urlpatterns = [
    path(
        'movie/', MovieListCreateViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('movie/<int:pk>/', MovieRetrieveUpdateDestroyAPIView.as_view(),
         name="movie-detail"),
    path('review/', ReviewListAPIView.as_view()),
    path('review/', ReviewCreateAPIView.as_view()),
    path('actor/', ActorListCreateAPIView.as_view()),
    path('actor/<str:slug>/', ActorRetrieveUpdateDestroyAPIView.as_view()),
    path('genre/', GenreListCreateAPIView.as_view()),
]
