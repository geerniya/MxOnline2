from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    """
    课程
    """
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构')
    teacher = models.ForeignKey(Teacher, verbose_name='机构讲师')
    name = models.CharField(max_length=20, verbose_name='课程名称')
    desc = models.TextField(verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), default='cj', max_length=10, verbose_name='课程难度')
    learn_time = models.IntegerField(verbose_name='学习时长', default=0)
    lesson_nums = models.IntegerField(verbose_name='章节数', default=0)
    fav_nums = models.IntegerField(verbose_name='收藏数', default=0)
    students = models.IntegerField(verbose_name='学习人数', default=0)
    click_nums = models.IntegerField(verbose_name='点击数', default=0)
    category = models.CharField(max_length=30, verbose_name='课程类别', default='后台开发')
    tag = models.CharField(max_length=20, default='', verbose_name='标签')
    is_banner = models.CharField(choices=(('yes', '是'), ('no', '不是')), default='no', verbose_name='是否轮播图', max_length=10)
    image = models.ImageField(upload_to='course/image/%Y/%m', max_length=100, verbose_name='封面图')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_learn_users(self):
        """
        获取学习该课程的用户
        """
        return self.usercourse_set.all()

    def get_all_lession(self):
        """
        获取课程所有章节
        """
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    课程章节
    """
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=20, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = verbose_name

    def get_all_video(self):
        """
        获取章节所有视频
        """
        return self.video_set.all()


    def __str__(self):
        return self.name


class Video(models.Model):
    """\
    课程视频
    """
    lesson = models.ForeignKey(Lesson, verbose_name='课程章节')
    name = models.CharField(max_length=20, verbose_name='视频名')
    url = models.CharField(max_length=100, verbose_name='视频链接', default='')
    learn_times = models.IntegerField(verbose_name='学习时长', default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    """
    课程资源
    """
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=20, verbose_name='名称')
    download = models.FileField(max_length=100, upload_to='course/resource/%Y/%m', verbose_name='课程资源')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name