from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # HTML views
    path('', include('funds.urls',  namespace="funds")),

    # API routes
    path("api/", include("funds.api.urls", namespace="api")),
]
