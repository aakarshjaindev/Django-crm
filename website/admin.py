"""
Django admin configuration for the website (CRM) application.

Registers the Record model with a customized admin interface
including list display, filtering, search, and pagination.
"""

from django.contrib import admin

from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    """Admin interface configuration for customer records."""

    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'city',
        'state',
        'created_at',
    )
    list_filter = ('state', 'city', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'city', 'state')
    list_per_page = 25
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
