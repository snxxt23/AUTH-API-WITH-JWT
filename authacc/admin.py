from django.contrib import admin
from authacc.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id','email','first_name','profile_picture','is_admin')
    list_filter = ('is_admin',)
    fieldsets=(
        ('User Credentials',{'fields':('username','email','password')}),
        ('Personal Info',{'fields':('first_name','last_name','profile_picture')}),
        ('Permissions',{'fields':('is_admin',)}),
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('username','email','password1','password2')
        }),
    )
    search_fields = ('username','email')
    ordering = ('id','email',)
    filter_horizontal = () 
