"""MxOnline2 URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve

from users.views import LoginView, RegisterView, ActiveView, LogoutView, ForgetPwdView, ResetPwdView
from users.views import IndexView
from MxOnline2.settings import MEDIA_ROOT, STATIC_ROOT
import xadmin

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<code>.*)/$', ActiveView.as_view(), name='active'),
    url(r'^forgetpwd/$', ForgetPwdView.as_view(), name='forgetpwd'),
    url(r'^resetpwd/(?P<code>.*)/$', ResetPwdView.as_view(), name='resetpwd'),

    #课程机构
    url(r'^org/', include('organization.urls', namespace='org')),

    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),

    #配置静态文件的访问处理函数
    url(r'^static/(?P<path>.*)/$', serve, {'document_root': STATIC_ROOT}),

    #公开课列表
    url(r'^course/', include('courses.urls', namespace='course')),

    #个人信息
    url(r'^users/', include('users.urls', namespace='users')),

]

#配置全局404页面
hander404 = 'users.views.page_not_found'
#配置全局505页面
hander505 = 'users.views.page_errors'
