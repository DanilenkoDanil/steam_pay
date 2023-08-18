from django.contrib import admin
from .models import Code, Setting, Payment, Qiwi, Interhub, UserLimitation
import datetime


class CustomDateFilter(admin.SimpleListFilter):
    title = ('Дата', )
    parameter_name = 'custom_date'

    def lookups(self, request, model_admin):
        return []

    def queryset(self, request, queryset):
        if self.value():
            selected_date = self.value()
            return queryset.filter(created_at__date=selected_date)


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
    list_filter = ('user', 'date',)
    search_fields = ('date', 'username')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            date_search = datetime.datetime.strptime(search_term, '%Y-%m-%d')
            queryset |= self.model.objects.filter(date=date_search)
        except ValueError:
            pass
        return queryset, use_distinct


@admin.register(Setting)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'qiwi_limit', 'digi_code', 'auto_course', 'course')


@admin.register(Qiwi)
class QiwiAdmin(admin.ModelAdmin):
    list_display = ('id', 'qiwi_code', 'current_counter', 'timer')
