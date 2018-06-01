from django.conf.urls import include, url
from . import views
from django.http import HttpResponse
from .models import TBCP_MEMBER_INFO


urlpatterns = [
    url(r'^(?P<u_product>[\w/\-/]+)/(?P<u_member>[\w/]+)/(?P<u_date>[\d]+)/(?P<u_item>[\w/]+)/(?P<u_seq>[\d]+)$', views.api_list) ,
    url(r'^(?P<u_product>[\w/\-/]+)/(?P<u_member>[\w/]+)/(?P<u_date>[\d]+)/(?P<u_item>[\w/]+)$', views.api_list) ,
]

