from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.db.models import Q

from .models import City, CourseOrg, Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavourite

# Create your views here.


class OrgListView(View):
    """
    机构列表
    """
    def get(self, request):
        all_citys = City.objects.all()
        all_orgs = CourseOrg.objects.all()
        hot_orgs = CourseOrg.objects.all().order_by('-students')[:3]

        # 搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords)
                                             )

        #选择机构类别
        category = request.GET.get('cate', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 选择城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'course_nums':
                all_orgs = all_orgs.order_by('-course_nums')

        numbers = all_orgs.count()
        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_citys': all_citys,
            'all_orgs': orgs,
            'numbers': numbers,
            'sort': sort,
            'category': category,
            'city_id': city_id,
            'hot_orgs': hot_orgs,

        })


class AddUserAskView(View):
    """
    用户提交咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    课程机构首页
    """
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id = int(org_id))
        all_courses = Course.objects.filter(course_org_id=org.id)
        all_teachers = Teacher.objects.filter(course_org_id=org.id).order_by('-fav_nums')[:2]
        # 判断有没有收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True

        current_page = 'home'
        return render(request, 'org-detail-homepage.html', {
            'org': org,
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'current_page': current_page,
            'has_fav': has_fav,

        })


class OrgCourseView(View):
    """
    机构课程页面
    """
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        all_courses = Course.objects.filter(course_org_id=org.id)
        # 判断有没有收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True

        current_page = 'course'
        return render(request, 'org-detail-course.html', {
            'org': org,
            'all_courses': all_courses,
            'current_page': current_page,
            'has_fav': has_fav,

        })


class OrgDescView(View):
    """
    机构介绍页面
    """
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        # 判断有没有收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True

        current_page = 'desc'
        return render(request, 'org-detail-desc.html', {
            'org': org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    """
    机构讲师
    """
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = Teacher.objects.filter(course_org_id=org.id).order_by('-fav_nums')
        #判断有没有收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True

        current_page = 'teacher'
        return render(request, 'org-detail-teachers.html', {
            'org': org,
            'all_teachers': all_teachers,
            'current_page': current_page,
            'has_fav': has_fav,

        })


class AddFavView(View):
    """
    用户收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        #判断用户有没有登录
        if request.user.is_authenticated():
            user_fav = UserFavourite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            #判断用户有没有收藏
            if user_fav:
                user_fav.delete()
                #收藏减1
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums -= 1
                    course.save()
                if int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums -= 1
                    org.save()
                if int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums -= 1
                    teacher.save()

                return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')
            else:
                add_user_fav = UserFavourite()
                add_user_fav.user = request.user
                add_user_fav.fav_id = int(fav_id)
                add_user_fav.fav_type = int(fav_type)
                add_user_fav.save()

                # 收藏加1
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                if int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums += 1
                    org.save()
                if int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')

        else:
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')


class TeacherListView(View):
    """
    机构讲师列表
    """
    def get(self, request):
        all_teachers = Teacher.objects.all()
        relate_teachers = Teacher.objects.all().order_by('-fav_nums')[:3]

        # 搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                             Q(points__icontains=search_keywords)
                                             )

        teacher_nums = all_teachers.count()

        #排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 3, request=request)
        all_teachers = p.page(page)


        return render(request, 'teachers-list.html', {
            'all_teachers': all_teachers,
            'relate_teachers': relate_teachers,
            'teacher_nums': teacher_nums,
            'sort': sort,
        })


class TeacherDetailView(View):
    """
    讲师详情页面
    """
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        relate_teachers = Teacher.objects.all().order_by('-fav_nums')[:3]
        all_courses = Course.objects.filter(teacher=teacher)
        #判断是否收藏
        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated():
            user_fav_teacher = UserFavourite.objects.filter(user=request.user, fav_id=teacher_id, fav_type=3)
            user_fav_org = UserFavourite.objects.filter(user=request.user, fav_id=teacher.course_org_id, fav_type=2)
            if user_fav_teacher:
                has_fav_teacher = True
            if user_fav_org:
                has_fav_org = True

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'relate_teachers': relate_teachers,
            'all_courses': all_courses,
            'has_fav_teacher': has_fav_teacher,
            'has_fav_org': has_fav_org,
        })
