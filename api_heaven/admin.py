from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,FlexTable,FileStorageTable,FlexRecordTable

class CustomUserAdmin(UserAdmin):
    model = CustomUser

class CustomFlexTableAdmin(admin.ModelAdmin):
    model = FlexTable

class CustomFlexRecordTableAdmin(admin.ModelAdmin):
    model = FlexRecordTable

class CustomFileStorageTableAdmin(admin.ModelAdmin):
    model = FileStorageTable
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FileStorageTable,CustomFileStorageTableAdmin)
admin.site.register(FlexTable, CustomFlexTableAdmin)
admin.site.register(FlexRecordTable, CustomFlexRecordTableAdmin)