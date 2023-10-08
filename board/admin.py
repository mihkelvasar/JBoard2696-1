from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Curriculum, JobPosition, JobApply
# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete=False
    verbose_name_plural="userprofile"

class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]

class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Name", {"fields" : ["first_name"]}),
        ("Surname", {"fields" : ["last_name"]}),
        ("User", {"fields" : ["user"]}),
        ("DOB", {"fields" : ["date_of_birth"]}),
        ("Company", {"fields" : ["company_name"]}),
        ("Company number", {"fields" : ["creg_number"]}),
        ("Is Company", {"fields" : ["is_seeker"]}),
    ]

    list_display = ["user"]
    list_filter = []

class CurriculumAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Profile", {"fields" : ["cv_uname"]}),
        ("CV Fname", {"fields" : ["cv_fname"]}),
        ("CV Lname", {"fields" : ["cv_lname"]}),
        ("CV Date", {"fields" : ["cv_date"]}),
    ]
    list_display = ["cv_lname", "cv_date"]


class JobPositionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title", {"fields" : ["job_title"]}),
        ("Company", {"fields" : ["job_source"]}),
        ("Poster", {"fields" : ["job_user"]}),
    ]
    list_display = ["job_title", "job_source", "job_user"]

class JobApplyAdmin(admin.ModelAdmin):
    fieldsets = [
        ("User", {"fields" : ["applicant"]}),
        ("Job", {"fields" : ["sourcejob"]}),
        ("Date", {"fields" : ["applydate"]}),
    ]
    list_display = ["applicant", "sourcejob", "applydate"]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(JobPosition, JobPositionAdmin)
admin.site.register(JobApply, JobApplyAdmin)