import xadmin

from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'course_org', 'teacher', 'degree','students', 'fav_nums', 'click_nums']
    search_fields = ['name', 'course_org__name', 'teacher__name', 'degree', 'students', 'fav_nums',  'click_nums']
    list_filter = ['name', 'course_org__name', 'teacher__name', 'degree', 'students', 'fav_nums', 'click_nums']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course__name', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'learn_times', 'add_time']
    search_fields = ['lesson__name', 'name', 'learn_times']
    list_filter = ['lesson__name', 'name', 'learn_times', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course__name', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)