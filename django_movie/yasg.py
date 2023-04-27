from django.urls import re_path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='Django Movie',
        default_version='v1',
        description='Desc',
        license=openapi.License('BSD License')
    ),
    public=True,
    permission_classes=(AllowAny,)
)

urlpatterns = [
   re_path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
