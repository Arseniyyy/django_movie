from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.views import UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('auth/users/', UserListCreateAPIView.as_view()),
    path('auth/users/me/', UserRetrieveUpdateDestroyAPIView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/jwt/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/jwt/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/v1/', include('movies.urls')),
    # path('rest-auth/', include('rest_auth.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
