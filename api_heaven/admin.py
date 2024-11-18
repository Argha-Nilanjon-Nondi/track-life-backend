from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,FlexTable

class CustomUserAdmin(UserAdmin):
    model = CustomUser

class CustomFlexTableAdmin(admin.ModelAdmin):
    model = FlexTable
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FlexTable, CustomFlexTableAdmin)