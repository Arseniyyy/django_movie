from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from djoser.views import TokenCreateView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,)

from users.views import UserRetrieveUpdateDestroyAPIView, CustomActivationViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    # path('auth/activate/<str:uid>/<str:token>/', TokenCreateView.as_view(), name='activate'),
    path('auth/users/me/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user_me'),
    path('auth/users/activation/', CustomActivationViewSet.as_view({'post': 'activation'}), name='user_activation'),
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
