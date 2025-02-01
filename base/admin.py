from django.contrib import admin
from .models import FAQ

# Register your models here.


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at', 'updated_at')
    search_fields = ('question', 'answer')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('question', 'answer')
        }),
        ('Hindi Translation', {
            'fields': ('question_hi', 'answer_hi'),
            'classes': ('collapse',)
        }),
        ('Bengali Translation', {
            'fields': ('question_bn', 'answer_bn'),
            'classes': ('collapse',)
        }),
        ('Gujarati Translation', {
            'fields': ('question_gu', 'answer_gu'),
            'classes': ('collapse',)
        }),
        ('Punjabi Translation', {
            'fields': ('question_pa', 'answer_pa'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
