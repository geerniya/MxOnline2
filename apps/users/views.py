import json

from django.shortcuts import render, render_to_response
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm
from utils.send_email import send_email_code
from courses.models import Course
from organization.models import CourseOrg, Teacher
from utils.mixin_utils import LoginRequiredMixin
from .forms import ImageUploadForm, UpdateEmailForm, UserInfoForm
from operation.models import UserCourse, UserFavourite, UserMessage


# Create your views here.


class CustomBackend(ModelBackend):
    """
    重写authenticate方法
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:   #可以捕获除与程序退出sys.exit()相关之外的所有异常
            return None



class LoginView(View):
    """
    用户登录
    """
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        #表单验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            #判断用户是否存在
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    """
    用户退出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    """
    实现注册功能
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')

            userprofile = UserProfile.objects.filter(email=email)
            if userprofile:
                return render(request, 'register.html', {'msg': '邮箱已存在'})
            else:
                user = UserProfile()
                user.email = email
                user.username = email
                user.password = make_password(password)
                user.is_active = False
                user.save()

                #注册成功，发送系统邮件
                message = '系统提示：欢迎新用户！'
                user_message = UserMessage(user=user, message=message, has_read='no')
                user_message.save()

                send_email_code(email, 'register')
                return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, 'register.html', {'register_form':register_form})


class ActiveView(View):
    """
    邮箱激活
    """
    def get(self, request, code):
        all_records = EmailVerifyRecord.objects.filter(code=code)
        if all_records:
            for record in all_records:
                user = UserProfile.objects.get(email=record.email)
                user.is_active = True
                user.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, 'active_wrong.html')


class ForgetPwdView(View):
    """
    忘记密码
    """
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                send_email_code(email, 'forget')
                return HttpResponseRedirect(reverse('login'))
            else:
                return render(request, 'forgetpwd.html', {'msg': '该邮箱不存在'})
        else:
            return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})


class ResetPwdView(View):
    """
    密码重置
    """
    def get(self, request, code):
        email_record = EmailVerifyRecord.objects.filter(code=code)
        if email_record:
            return render(request, 'password_reset.html', {'code':code})
        else:
            return render(request, 'active_wrong.html')

    def post(self, request, code):
        resetpwd_form = ResetPwdForm(request.POST)
        if resetpwd_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 == password2:
                email_record = EmailVerifyRecord.objects.get(code=code)
                user = UserProfile.objects.get(email=email_record.email)
                user.password = make_password(password1)
                user.save()
                return HttpResponseRedirect(reverse('login'))
            else:
                return render(request, 'password_reset.html', {'msg':'两次密码输入不一致，请重新输入'})
        else:
            return render(request, 'password_reset.html', {'resetpwd_form': resetpwd_form})


class IndexView(View):
    """
    首页展示
    """
    def get(self, request):
        banners = Banner.objects.all().order_by('-index')[:5]
        banner_courses = Course.objects.filter(is_banner='yes')[:3]
        all_courses = Course.objects.filter(is_banner='no')[:6]
        all_orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', {
            'banners': banners,
            'banner_courses': banner_courses,
            'all_courses': all_courses,
            'all_orgs': all_orgs,

        })


class UserInfoView(LoginRequiredMixin, View):
    """
    个人信息页面
    """
    def get(self, request):
        user = request.user
        return render(request, 'usercenter-info.html', {
            'user': user,
        })

    def post(self, request):
        userinfo_form = UserInfoForm(request.POST, instance=request.user)
        if userinfo_form.is_valid():
            userinfo_form.save()
            return HttpResponse('{"status":"success"}', content_type = 'application/json')
        else:
            return HttpResponse(json.dumps(userinfo_form.errors), content_type='application/json')


class ImageUploadView(LoginRequiredMixin, View):
    """
    修改头像
    """
    def post(self, request):
        upload_image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if upload_image_form.is_valid():
            upload_image_form.save()
            #感觉此处缺少一个js文件，提示修改成功
        else:
            pass
            #此处缺少失败的提示


class UpdatePwdView(LoginRequiredMixin, View):
    """
    修改密码
    """
    def post(self, request):
        pwd_form = ResetPwdForm(request.POST)
        if pwd_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return HttpResponse('{"status":"fail", "msg":"两次密码不一致"}', content_type = 'application/json')

            else:
                request.user.password = make_password(password1)
                request.user.save()
                return HttpResponse('{"status":"success"}', content_type = 'application/json')
        else:
            return HttpResponse(json.dumps(pwd_form.errors), content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改邮箱
    """
    def post(self, request):
        email_form = UpdateEmailForm(request.POST)
        if email_form.is_valid():
            email = request.POST.get('email', '')
            code = request.POST.get('code', '')
            #判断验证码是否正确
            email_verify = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
            if email_verify:
                request.user.email = email
                request.user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    获取邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type = 'application/json')
        else:
            send_email_code(email, 'update_email')
            return HttpResponse('{"status":"success"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我的收藏——机构
    """
    def get(self, request):
        fav_org_ids = UserFavourite.objects.filter(user=request.user, fav_type=2)
        org_ids = [fav_org_id.fav_id for fav_org_id in fav_org_ids]
        all_orgs = CourseOrg.objects.filter(id__in=org_ids)

        fav_type = 'org'
        return render(request, 'usercenter-fav-org.html', {
            'all_orgs': all_orgs,
            'fav_type': fav_type,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我的收藏——教师
    """
    def get(self, request):
        fav_teacher_ids = UserFavourite.objects.filter(user=request.user, fav_type=3)
        teacher_ids = [fav_teacher_id.fav_id for fav_teacher_id in fav_teacher_ids]
        all_teachers = Teacher.objects.filter(id__in=teacher_ids)

        fav_type = 'teacher'
        return render(request, 'usercenter-fav-teacher.html', {
            'all_teachers': all_teachers,
            'fav_type': fav_type,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我的收藏——课程
    """
    def get(self, request):
        fav_course_ids = UserFavourite.objects.filter(user=request.user, fav_type=1)
        course_ids = [fav_course_id.fav_id for fav_course_id in fav_course_ids]
        all_courses = Course.objects.filter(id__in=course_ids)

        fav_type = 'course'
        return render(request, 'usercenter-fav-course.html', {
            'all_courses': all_courses,
            'fav_type': fav_type,
        })


class MyMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        my_messages = UserMessage.objects.filter(user=request.user)
        return render(request, 'usercenter-message.html', {
            'my_messages': my_messages,
        })


def page_not_found(request):
    """
    404页面
    """
    # responce = render_to_response('404.html', {})
    # responce.status_code = 404
    # return responce
    return render(request, '404.html')

def page_errors(request):
    """
    500页面
    """
    responce = render_to_response('500.html', {})
    responce.status_code = 500
    return responce