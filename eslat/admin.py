from django.contrib import admin
from .models import User, Target


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'first_name', 'last_name', 'phone_number', 'is_active',
        'last_login', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number', 'email')
    readonly_fields = ('last_login', 'date_joined')


class TargetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'period', 'user', 'is_active', 'created_at')
    list_filter = ('status', 'is_active')
    search_fields = ('name', 'description', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(User, UserAdmin)
admin.site.register(Target, TargetAdmin)
