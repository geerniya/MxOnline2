from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseVideoView, CourseCommentView, AddCommentView


urlpatterns = [
    #公开课列表
    url(r'^list/$', CourseListView.as_view(), name='list'),
    #公开课详情
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='detail'),
    #课程章节
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name='video'),
    #课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='comment'),
    #添加评论
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),

]