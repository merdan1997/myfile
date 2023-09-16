from django.contrib import admin
from .models import  Hostnames, Roles, Filterlog ,role_text
# Register your models here.


admin.site.register(Hostnames)
admin.site.register(Roles)
admin.site.register(Filterlog)
admin.site.register(role_text)
