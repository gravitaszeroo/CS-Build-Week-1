from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('get_room', api.get_room),
    url('say', api.say),
]
