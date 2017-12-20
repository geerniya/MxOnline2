from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course

# Create your models here.


class UserComment(models.Model):
    """
    用户对课程的评论
    """
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    comment = models.TextField(verbose_name='内容')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name


class UserAsk(models.Model):
    """
    用户咨询
    """
    name = models.CharField(max_length=20, verbose_name='姓名')
    telephone = models.CharField(max_length=11, verbose_name='手机')
    course_name = models.CharField(max_length=20, verbose_name='课程名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


class UserFavourite(models.Model):
    """
    用户收藏的课程/机构/教师
    """
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    fav_id = models.IntegerField(verbose_name='数据ID')
    fav_type = models.IntegerField(choices=((1, '课程'), (2, '机构'), (3, '教师')), verbose_name='类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    """
    用户学习的课程
    """
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户学习'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    """
    用户收到的消息
    """
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    message = models.TextField(max_length=300, verbose_name='消息')
    has_read = models.CharField(choices=(('yes','已读'), ('no','没读')), max_length=10, default='no', verbose_name='消息是否读过')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name





