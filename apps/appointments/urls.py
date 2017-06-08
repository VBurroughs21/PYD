# appointment app

from django.conf.urls import url
from views import *

urlpatterns = [
     url(r'^appointments$', index, name = 'home'),
     url(r'^appointments/(?P<appointment_id>\w+)$', read, name = 'read'),
     url(r'^appointments/(?P<appointment_id>\w+)/delete$', delete, name = 'delete'),
     url(r'^appointments/(?P<appointment_id>\w+)/edit$', edit, name = 'edit'),
     url(r'^create/$', create, name = 'create'),
]

# edit, delete, add, show