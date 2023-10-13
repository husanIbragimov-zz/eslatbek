from django.contrib import admin
from .models import BotUser, Target, DailyTarget


class BotUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'full_name', 'username', 'full_name', 'age', 'phone_number', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('username', 'full_name', 'phone_number', 'telegram_id')
    readonly_fields = ('updated_at', 'created_at')


class TargetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'user', 'is_active', 'created_at')
    list_filter = ('weekday', 'status', 'is_active')
    filter_horizontal = ('weekday',)
    search_fields = ('name', 'description', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(BotUser, BotUserAdmin)
admin.site.register(Target, TargetAdmin)
