from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include


# importing from the views.py file
from .views import (
    home_page,
    registration_page,
    login_page
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
    path('', home_page),
    path('login/', login_page),
    path('registration/', registration_page),
]
