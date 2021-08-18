from django.contrib import admin
from django.urls import path, include
from app.views import uuid

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('uuid/', uuid)
    
]
