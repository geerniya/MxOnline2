from django import forms
from captcha.fields import CaptchaField

from users.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField()


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()


class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6, max_length=20)
    password2 = forms.CharField(required=True, min_length=6, max_length=20)


class ImageUploadForm(forms.ModelForm):
    """
    修改头像
    """
    class Meta:
        model = UserProfile
        fields = ['image']


class UpdateEmailForm(forms.Form):
    """
    修改邮箱
    """
    email = forms.EmailField(required=True)
    code = forms.CharField(required=True)


class UserInfoForm(forms.ModelForm):
    """
    修改个人信息
    """
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'telephone']

