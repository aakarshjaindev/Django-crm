"""
URL configuration for the website (CRM) application.

Maps URL paths to view functions for authentication and
customer record CRUD operations.
"""

from django.urls import path

from . import views

app_name = 'website'

urlpatterns = [
    # -- Authentication ------------------------------------------------------
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    # -- Record CRUD ---------------------------------------------------------
    path('record/<int:pk>/', views.record_detail, name='record'),
    path('record/<int:pk>/delete/', views.delete_record, name='delete_record'),
    path('record/<int:pk>/update/', views.update_record, name='update_record'),
    path('record/add/', views.add_record, name='add_record'),
]
