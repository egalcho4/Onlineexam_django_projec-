from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Permision)
admin.site.register(Password_manager)
#admin.site.register(Year_nows)
admin.site.register(Assiment)


