from django.contrib import admin
from .models import Code, Setting


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'username', 'amount', 'status')


@admin.register(Setting)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'qiwi_code', 'digi_code')
