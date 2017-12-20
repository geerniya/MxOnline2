import xadmin

from .models import UserAsk, UserComment, UserFavourite, UserMessage, UserCourse


class UserAskAdmin(object):
    list_display = ['name', 'telephone', 'course_name', 'add_time']
    search_fields = ['name', 'telephone', 'course_name']
    list_filter = ['name', 'telephone', 'course_name', 'add_time']


class UserCommentAdmin(object):
    list_display = ['user', 'course', 'comment', 'add_time']
    search_fields = ['user__username', 'course__name', 'comment']
    list_filter = ['user__username', 'course__name', 'comment', 'add_time']


class UserFavouriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user__username', 'fav_id', 'fav_type']
    list_filter = ['user__username', 'fav_id', 'fav_type', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'add_time']
    search_fields = ['user__username', 'message']
    list_filter = ['user__username', 'message', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user__username', 'course__name']
    list_filter = ['user__username', 'course__name', 'add_time']

xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserComment, UserCommentAdmin)
xadmin.site.register(UserFavourite, UserFavouriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)