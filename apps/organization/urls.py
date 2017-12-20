from django.conf.urls import url

from .views import OrgListView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView
from .views import AddFavView, TeacherListView, TeacherDetailView


urlpatterns = [
    #机构列表
    url(r'^list/$', OrgListView.as_view(), name='org_list'),
    #用户咨询
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    #机构首页
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='home'),
    #机构课程
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='course'),
    #机构介绍
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='desc'),
    # 机构讲师
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='teacher'),
    #用户收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
    #讲师列表
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    #讲师详情
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
]