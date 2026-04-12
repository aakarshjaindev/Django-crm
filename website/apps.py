"""
Application configuration for the website (CRM) app.
"""

from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    """Configuration for the website application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'
    verbose_name = 'Customer Records'
