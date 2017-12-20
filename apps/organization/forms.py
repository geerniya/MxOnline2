import re

from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'telephone', 'course_name']

    def clean_telephone(self):
        """
        手机号码验证
        """
        telephone = self.cleaned_data['telephone']
        REGEX_MOBILE = '^1[358]\d{9}$|^170\d{8}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(telephone):
            return telephone
        else:
            raise forms.ValidationError('手机号码非法', code='telephone_invalid')
