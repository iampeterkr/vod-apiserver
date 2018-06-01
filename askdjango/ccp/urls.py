from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from . import views
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import TBCP_MEMBER_REQUEST_STAT_INFO

router = DefaultRouter()
#router.register('api-list/^(?P<u_product>[\w/\-/]+)/$' , views.aaa)

#router = CustomReadOnlyRouter()
#router.register('api-list$', views.aaa, base_name='aaa')
#urlpatterns = router.urls



urlpatterns = [
    #url(r'$', views.aaa),
    url(r'^(?P<u_product>[\w/\-/]+)/$' , views.aaa) ,
    #url(r'^(?P<u_product>[\W/-/]+)/$', views.TBCP_MEMBER_REQUEST_STAT_INFO_ViewSet.public_list, name='stat_check'),
    #url(r'^(?P<u_product>[\W/-/]+)$', views.stat_info)
    #url(r'$', views.stat_info),
   # url(r'$', views.stat_info),
    #url(r'^(?P<u_product>[\W/-/]+)', views.stat_detail),

]

'''
urlpatterns = [
    #url(r'^login/(?P<u_loginid>[[a-zA-Zㄱ-힣/\d/]+)/(?P<u_loginpass>[[a-zA-Zㄱ-힣/\d/]+)/$', views.LoginView),
    # [\w/\-/]+ 영어대소문자 숫자 '-', \w/{5} 5자리
    url(r'^(?P<u_product>[\w/\-/]+)/(?P<u_member>[\w/]+)/(?P<u_date>[\d]+)/(?P<u_process>[\w/]+)/(?P<u_item>[\w/]+)/(?P<u_seq>[\d]+)/$', views.MainView) ,
    url(r'^(?P<u_product>[\w/\-/]+)/(?P<u_member>[\w/]+)/(?P<u_date>[\d]+)/(?P<u_process>[\w/]+)/(?P<u_item>[\w/]+)/$', views.MainView) ,
    url(r'^(?P<u_product>[\w/\-/]+)/(?P<u_member>[\w/]+)/(?P<u_date>[\d]+)/(?P<u_process>[\w/]+)/$', views.MainView) ,
    url(r'^(?P<u_product>[\w/\-/]+)/(?P<u_member>[\w/]+)/(?P<u_date>[\d]+)/$', views.MainView) ,
    url(r'^(?P<u_product>[\w/\-/]+)/(?P<u_member>[\w/]+)/$', views.MainView) ,
    url(r'^(?P<u_product>[\w/\-/]+)/$' , views.MainView) ,
    # url(r'^/', views.MainView) ,
    # '/'를 붙여주고 안 붙여 주는것을 완벽히 이해가 안되어 있음
    #url(r'^(?P<product>[a-zA-Zㄱ-힣/\d/]+)/(?P<u_member>[\d/]+)/$' , views.ListView) ,
    #url(r'^')
]
'''
