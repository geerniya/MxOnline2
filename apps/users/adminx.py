import xadmin

from .models import UserProfile, EmailVerifyRecord, Banner

from xadmin import views


class BaseSetting(object):
    """
    配置主题
    """
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    """
    配置抬头和尾部，以及列表显示
    """
    site_title = '慕学后台管理系统'
    site_footer = '慕学在线网'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['email', 'code', 'send_type', 'add_time']
    search_fields = ['email', 'code', 'send_type']
    list_filter = ['email', 'code', 'send_type', 'add_time']


class BannerAdmin(object):
    list_display = ['title', 'url', 'image', 'index', 'add_time']
    search_fields = ['title', 'url', 'image', 'index']
    list_filter = ['title', 'url', 'image', 'index', 'add_time']

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)