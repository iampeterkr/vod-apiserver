from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from . import views
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import TBCP_MEMBER_INFO

router = DefaultRouter()
#router.register('api-list/^(?P<u_product>[\w/\-/]+)/$' , views.aaa)

#router = CustomReadOnlyRouter()
#router.register('api-list$', views.aaa, base_name='aaa')
#urlpatterns = router.urls



urlpatterns = [
    url(r'^(?P<u_product>[\w/\-/]+)/$' , views.api_post) ,
]

