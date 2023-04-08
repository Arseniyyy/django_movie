from django.urls import path

from movies.views import (ActorListCreateAPIView,
                          ActorRetrieveUpdateDestroyAPIView,
                          GenreListCreateAPIView,
                          ReviewListCreateAPIView,
                          ReviewRetrieveUpdateDestroyAPIView,
                          MovieRetrieveUpdateDestroyAPIView,
                          MovieListCreateViewSet,
                          ListCreateRatingViewSet)


urlpatterns = [
    path(
        'movie/', MovieListCreateViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('movie/<int:pk>/', MovieRetrieveUpdateDestroyAPIView.as_view(),
         name="movie-detail"),
    path('review/', ReviewListCreateAPIView.as_view()),
    path('review/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view()),
    path('actor/', ActorListCreateAPIView.as_view()),
    path('actor/<str:slug>/', ActorRetrieveUpdateDestroyAPIView.as_view()),
    path('genre/', GenreListCreateAPIView.as_view()),
    path("rating/", ListCreateRatingViewSet.as_view({"get": "list",
                                                     "post": "create"})),
]
