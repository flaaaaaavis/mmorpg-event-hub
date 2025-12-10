from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('apps.events.urls')),
    path('api/', include('apps.guilds.urls')),
    path('api/', include('apps.players.urls')),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.awards.urls')),
    # DRF login (session) and token auth endpoints
    path('api-auth/', include('rest_framework.urls')),
    path('api/token-auth/', obtain_auth_token),
]
