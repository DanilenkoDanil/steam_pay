from django.contrib import admin
from .models import Code, Setting, Payment, Qiwi, Interhub, UserLimitation


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'username', 'amount', 'status')


@admin.register(UserLimitation)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'now_balance')


@admin.register(Interhub)
class InterhubAdmin(admin.ModelAdmin):
    list_display = ('token', 'balance')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('username', 'amount', 'status', 'user', 'date')
    list_filter = ('user', 'date')


@admin.register(Setting)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'qiwi_limit', 'digi_code', 'auto_course', 'course')


@admin.register(Qiwi)
class QiwiAdmin(admin.ModelAdmin):
    list_display = ('id', 'qiwi_code', 'current_counter', 'timer')
