from django.urls import path, re_path
from django.conf.urls import include
from .views import location_list, location_detail

urlpatterns = [
    path('location/', location_list),
    re_path('location/(?P<pk>[0-9]+)/$', location_detail),
]
