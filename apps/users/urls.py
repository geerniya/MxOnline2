from django.conf.urls import url

from .views import UserInfoView, ImageUploadView, UpdatePwdView, UpdateEmailView, SendEmailCodeView
from .views import MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    #个人信息
    url(r'^info/$', UserInfoView.as_view(), name='info'),
    #修改头像
    url(r'^image/upload/$', ImageUploadView.as_view(), name='image_upload'),
    #修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    #修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    #获取邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    #我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    # 我的收藏_机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
    # 我的收藏_教师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 我的收藏_课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),
    # 我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),
]