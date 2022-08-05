from django.contrib import admin
from .models import Code, Qiwi


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'username', 'amount', 'status')


@admin.register(Qiwi)
class QiwiAdmin(admin.ModelAdmin):
    list_display = ('id', 'code')
