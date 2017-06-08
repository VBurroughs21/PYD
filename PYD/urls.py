from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('apps.appointments.urls', namespace = 'appointments')),
    url(r'^', include('apps.users.urls', namespace = 'users'))
]
