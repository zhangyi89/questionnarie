from django.contrib import admin

# Register your models here.
from app01 import models


admin.site.register(models.Questionnaire)
admin.site.register(models.Question)
admin.site.register(models.Option)
admin.site.register(models.Answer)
admin.site.register(models.ClassList)
admin.site.register(models.Student)
admin.site.register(models.UserInfo)
