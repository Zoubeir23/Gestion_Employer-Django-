from django.contrib import admin
from .models import Service, Employer, Conge

# Register your models here.
admin.site.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Employer)
class EmployeeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Conge)
class CongeAdmin(admin.ModelAdmin):
    pass
