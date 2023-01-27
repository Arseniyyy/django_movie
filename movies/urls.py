from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,)

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
    path('movie/<int:pk>/', MovieRetrieveUpdateDestroyAPIView.as_view()),
    path('review/', ReviewListAPIView.as_view()),
    path('review/', ReviewCreateAPIView.as_view()),
    path('actor/', ActorListCreateAPIView.as_view()),
    path('actor/<str:pk>/', ActorRetrieveUpdateDestroyAPIView.as_view()),
    path('genre/', GenreListCreateAPIView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
