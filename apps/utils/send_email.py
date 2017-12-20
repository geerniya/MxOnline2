import random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline2.settings import EMAIL_FROM


def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def send_email_code(email, send_type='register'):
    """
    发送邮箱验证码
    """
    email_code = EmailVerifyRecord()
    if send_type == 'update_email':
        random_str = generate_random_str(4)
    else:
        random_str = generate_random_str(16)
    email_code.email = email
    email_code.code = random_str
    email_code.send_type = send_type
    email_code.save()

    if send_type == 'register':
        email_title = '慕学在线网注册激活平台'
        email_body = '请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(random_str)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    if send_type == 'forget':
        email_title = '慕学在线网用户密码重置'
        email_body = '请点击下面的链接重置你的密码：http://127.0.0.1:8000/resetpwd/{0}'.format(random_str)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    if send_type == 'update_email':
        email_title = '慕学在线网用户邮箱重置'
        email_body = '下面是你重置邮箱的验证码：{0}'.format(random_str)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

