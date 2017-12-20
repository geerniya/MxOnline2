from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime

# Create your models here.


class UserProfile(AbstractUser):
    """
    自定义用户表单
    """
    nick_name = models.CharField(max_length=20, verbose_name='昵称', default='')
    address = models.CharField(max_length=100, verbose_name='地址', default='')
    telephone = models.CharField(max_length=11, verbose_name='手机')
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), default='male', verbose_name='性别', max_length=10)
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    image = models.ImageField(verbose_name='头像', upload_to='users/image/%Y/%m', max_length=50, default='users/image/default_big_14.png')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def get_unread_message_nums(self):
        #获取没有读过的消息数目
        return self.usermessage_set.filter(has_read='no').count()

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    """
    邮箱验证码
    """
    email = models.CharField(max_length=30, verbose_name='邮箱')
    code = models.CharField(max_length=30, verbose_name='验证码')
    send_type = models.CharField(choices=(('register', '注册'), ('forget', '忘记密码'), ('update_email', '邮箱重置')), verbose_name='验证码类型', default='register', max_length=20)
    add_time = models.DateTimeField(verbose_name='创建时间', default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    """
    首页的轮播图
    """
    title = models.CharField(verbose_name='名称', max_length=20, default='')
    url = models.CharField(verbose_name='链接', max_length=100, default='')
    image = models.ImageField(upload_to='users/banner/%Y/%m', max_length=100, verbose_name='图像')
    index = models.IntegerField(verbose_name='顺序', default=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

