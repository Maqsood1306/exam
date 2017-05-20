from django.contrib import admin
from .models import stud_id,student,subject,result,dept,photo,reval,hallticket,nc_student,notice


# Register your models here.
admin.site.register(stud_id)
admin.site.register(subject)
admin.site.register(student)
admin.site.register(dept)
admin.site.register(result)
admin.site.register(photo)
admin.site.register(reval)
admin.site.register(hallticket)
admin.site.register(nc_student)
admin.site.register(notice)