from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Administrator)
admin.site.register(AdministratorAdditional)
admin.site.register(Domain)
admin.site.register(Category)
admin.site.register(Complaints)
admin.site.register(Workers)
admin.site.register(Reviews)

