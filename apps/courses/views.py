from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.http import HttpResponse

from .models import Course, CourseResource
from operation.models import UserFavourite, UserCourse, UserComment
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    """
    公开课列表
    """
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        #搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|
                                             Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords)
                                             )

        #排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            if sort == 'students':
                all_courses = all_courses.order_by('-students')

        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        all_courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': all_courses,
            'sort': sort,
            'hot_courses': hot_courses,

        })


class CourseDetailView(View):
    """
    课程详情页面
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        #课程点击数加1
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        # 判断是否收藏
        if request.user.is_authenticated():
            user_fav_course = UserFavourite.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1)
            user_fav_org = UserFavourite.objects.filter(user=request.user, fav_id=int(course.course_org_id), fav_type=2)
            if user_fav_course:
                has_fav_course = True
            if user_fav_org:
                has_fav_org = True

        #相关课程推荐
        tag = course.tag
        if tag:
            # relate_courses = Course.objects.filter(Q(tag=tag)&~Q(id=course_id)).order_by('-click_nums')[:1]
            relate_courses = Course.objects.filter(tag=tag).exclude(id=course_id).order_by('-click_nums')[:1]
        else:
            relate_courses = []

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_course': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,

        })


class CourseVideoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)

        #进入后，课程学习人数加1
        course.students += 1
        course.save()

        #用户如果没学习过，添加学习
        user_course = UserCourse.objects.filter(user=request.user, course_id=course_id)
        if not user_course:
            add_user_course = UserCourse()
            add_user_course.user = request.user
            add_user_course.course = course
            add_user_course.save()

        #课程资源
        course_resource = CourseResource.objects.filter(course=course)

        #该课的同学还学过
        users_id = [learn_user.user.id for learn_user in course.get_learn_users()]
        user_courses = UserCourse.objects.filter(user_id__in=users_id)
        courses_id = [user_course.course.id for user_course in user_courses]
        relate_courses = Course.objects.filter(id__in=courses_id)

        return render(request, 'course-video.html', {
            'course': course,
            'course_resource': course_resource,
            'relate_courses': relate_courses,

        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)

        #课程评论
        course_comments = UserComment.objects.filter(course=course).order_by('-add_time')

        # 课程资源
        course_resource = CourseResource.objects.filter(course=course)

        # 该课的同学还学过
        users_id = [learn_user.user.id for learn_user in course.get_learn_users()]
        user_courses = UserCourse.objects.filter(user_id__in=users_id)
        courses_id = [user_course.course.id for user_course in user_courses]
        relate_courses = Course.objects.filter(id__in=courses_id)

        return render(request, 'course-comment.html', {
            'course': course,
            'course_resource': course_resource,
            'relate_courses': relate_courses,
            'course_comments': course_comments,

        })


class AddCommentView(LoginRequiredMixin, View):
    """
    用户添加评论
    """
    def post(self, request):
        comments = request.POST.get('comments', '')
        course_id = request.POST.get('course_id', '')
        if comments:
            user_comment = UserComment(user=request.user, course_id=int(course_id), comment=comments)
            user_comment.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')