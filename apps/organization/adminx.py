import xadmin

from .models import City, CourseOrg, Teacher


class CityAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['city', 'name', 'desc', 'category',  'fav_nums', 'course_nums', 'add_time']
    search_fields = ['city__name', 'name', 'desc', 'category', 'fav_nums', ]
    list_filter = ['city__name', 'name', 'desc', 'category', 'fav_nums', 'add_time']


class TeacherAdmin(object):
    list_display = ['course_org', 'name', 'work_years', 'work_company', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['course_org__name', 'name', 'work_years', 'work_company', 'click_nums', 'fav_nums']
    list_filter = ['course_org__name', 'name', 'work_years', 'work_company', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)

