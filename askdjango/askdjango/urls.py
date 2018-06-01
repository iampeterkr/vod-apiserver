"""askdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^sample/', include('sample.urls', namespace='sample')), 
    # 동영상에서는 namespace가 있는데, 여기서는 error가난다. app 이름과 동일하는것을 추천하지 않는듯..include
    url(r'^sample/', include('sample.urls')),
    #각 종류에 따라 url을 따로 호출토록 함. 
    url(r'^api-list/ccp/', include('ccp.urls-api-list')),
    url(r'^api-detail/ccp/', include('ccp.urls-api-detail')),
    url(r'^api-post/ccp/', include('ccp.urls-api-post')),

 
]
