# users app

from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', index, name = 'home'),
    url(r'^main/$', index, name = 'home'),
    url(r'^register/$', register, name = 'register'),
    url(r'^login/$', login, name = 'login'),
    url(r'^logout/$', logout, name = 'logout'),
]

# add, login, logout