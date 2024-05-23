from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Doctor)
admin.site.register(DocInHospital)
admin.site.register(Hospital)
admin.site.register(Emergency)
admin.site.register(Appointment)