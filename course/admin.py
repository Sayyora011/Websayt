from django.contrib import admin

# Register your models here.
from course.models import Course, TutorLang, CourseLang
from course.models import Subject, Student, Tutor

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image']

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'slug', 'image']
    list_filter = ['course']

class SubjectLanguageAdmin(admin.ModelAdmin):
    list_display = ['lang', 'slug']
    list_filter = ['lang']

class CourseLanguageAdmin(admin.ModelAdmin):
    list_display = ['keywords', 'lang', 'slug']
    prepopulated_fields = {'slug': ('keywords',)}
    list_filter = ['lang']

class TutorLanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'lang']
    list_filter = ['lang']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'image']

class TutorAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'image']
    list_filter = ['subject']




admin.site.register(Course, CourseAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Tutor, TutorAdmin)
admin.site.register(Student, StudentAdmin)


admin.site.register(TutorLang, TutorLanguageAdmin)
admin.site.register(CourseLang, CourseLanguageAdmin)
