from datetime import datetime

from django.db import models


# Create your models here.


class City(models.Model):
    """
    城市
    """
    name = models.CharField(verbose_name='名称', max_length=20)
    desc = models.TextField(verbose_name='描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    """
    课程机构
    """
    city = models.ForeignKey(City, verbose_name='所在城市')
    name = models.CharField(verbose_name='名称', max_length=20)
    desc = models.TextField(verbose_name='课程描述')
    address = models.CharField(verbose_name='机构地址', max_length=100, default='')
    fav_nums = models.IntegerField(verbose_name='收藏数', default=0)
    students = models.IntegerField(verbose_name='学习人数', default=0)
    course_nums = models.IntegerField(verbose_name='课程数', default=0)
    category= models.CharField(choices=(('pxjg', '培训机构'), ('gx', '高校'), ('gr', '个人')), default='pxjg', verbose_name='机构类别', max_length=20)
    image = models.ImageField(upload_to='org/image/%Y/%m', max_length=100, verbose_name='封面图')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def get_course_nums(self):
        """
        获取机构的课程数
        """
        return self.course_set.all().count()

    def get_teacher_nums(self):
        """
        获取机构的教师数
        """
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """
    机构讲师
    """
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构')
    name = models.CharField(verbose_name='姓名', max_length=20)
    age = models.IntegerField(verbose_name='年龄', default=18)
    work_years = models.IntegerField(verbose_name='工作年限', default=1)
    work_position = models.CharField(verbose_name='工作职位', default='', max_length=20)
    work_company = models.CharField(verbose_name='就职公司', default='', max_length=20)
    points = models.TextField(verbose_name='教学特点', null=True, blank=True)
    fav_nums = models.IntegerField(verbose_name='收藏数', default=0)
    click_nums = models.IntegerField(verbose_name='点击数', default=0)
    course_nums = models.IntegerField(verbose_name='课程数', default=0)
    image = models.ImageField(upload_to='org/teacher/%Y/%m', max_length=100, verbose_name='头像')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '机构讲师'
        verbose_name_plural = verbose_name

    def get_course(self):
        """
        得到该教师名下最受欢迎的课程
        """
        course = self.course_set.all().order_by('-students').first()
        return course

    def __str__(self):
        return self.name

