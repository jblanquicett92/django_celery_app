from django.urls import path, include, re_path
from . import views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Wise Athena APP",
      default_version='v1',
      description="Public Documentation Wise Athena APP",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="jorgeabm1992@gmail.com"),
      license=openapi.License(name="MIT"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('v1/doc/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('v1/doc/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('v1/receive_file/', views.EventFileView.as_view()),
    path('v1/notification/<str:id>', views.NotificationView.as_view()),
    path('v1/notifications/', views.NotificationView.as_view()),
   
]