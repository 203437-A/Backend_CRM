from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import Employee, Client, Category, ClientCategory

class EmployeeAdmin(UserAdmin):
    model = Employee
    list_display = ['username', 'email', 'phone_number']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Client)
admin.site.register(Category)
admin.site.register(ClientCategory)
