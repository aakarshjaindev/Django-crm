"""
Views for the website (CRM) application.

Handles authentication (login, logout, registration) and CRUD
operations for customer records with search functionality.
"""

import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import RecordForm, SignUpForm
from .models import Record

logger = logging.getLogger(__name__)


# =============================================================================
# Authentication Views
# =============================================================================

@require_http_methods(["GET", "POST"])
def home(request):
    """
    Home page view.

    - **Authenticated users**: displays the customer records dashboard
      with optional search filtering via the ``q`` query parameter.
    - **Unauthenticated users**: displays the login form and processes
      login submissions.
    """
    if request.user.is_authenticated:
        records = Record.objects.all()
        query = request.GET.get('q', '').strip()

        if query:
            records = records.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
                | Q(phone__icontains=query)
                | Q(city__icontains=query)
                | Q(state__icontains=query)
            )
            logger.debug("Search for '%s' returned %d results.", query, records.count())

        return render(request, 'home.html', {'records': records, 'query': query})

    # -- Handle login for unauthenticated users ------------------------------
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            logger.info("User '%s' logged in.", username)
            return redirect('website:home')

        messages.error(request, "Error logging in. Please check your credentials.")
        logger.warning("Failed login attempt for username '%s'.", username)
        return redirect('website:home')

    return render(request, 'home.html')


@require_POST
def logout_user(request):
    """Log the current user out and redirect to the home page."""
    logger.info("User '%s' logged out.", request.user.username)
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('website:home')


@require_http_methods(["GET", "POST"])
def register_user(request):
    """
    User registration view.

    Displays and processes the sign-up form. On successful registration,
    the user is redirected to the login page with a success message.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "User registered successfully! Please login.")
            logger.info("New user registered: '%s'.", user.username)
            return redirect('website:home')

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


# =============================================================================
# Record CRUD Views
# =============================================================================

@login_required(login_url='website:home')
def record_detail(request, pk):
    """Display detailed information for a single customer record."""
    customer_record = get_object_or_404(Record, pk=pk)
    return render(request, 'record.html', {'customer_record': customer_record})


@login_required(login_url='website:home')
@require_POST
def delete_record(request, pk):
    """Delete a customer record and redirect to the home page."""
    customer_record = get_object_or_404(Record, pk=pk)
    logger.info(
        "User '%s' deleted record #%d (%s).",
        request.user.username, pk, customer_record,
    )
    customer_record.delete()
    messages.success(request, "Record deleted successfully.")
    return redirect('website:home')


@login_required(login_url='website:home')
@require_http_methods(["GET", "POST"])
def add_record(request):
    """
    Create a new customer record.

    Displays an empty form on GET and processes the submission on POST.
    """
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            messages.success(request, "Record added successfully!")
            logger.info("User '%s' added record #%d.", request.user.username, record.pk)
            return redirect('website:home')
    else:
        form = RecordForm()

    return render(request, 'add_record.html', {'form': form})


@login_required(login_url='website:home')
@require_http_methods(["GET", "POST"])
def update_record(request, pk):
    """
    Update an existing customer record.

    Pre-populates the form with current values on GET and
    processes the updated submission on POST.
    """
    customer_record = get_object_or_404(Record, pk=pk)

    if request.method == 'POST':
        form = RecordForm(request.POST, instance=customer_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully!")
            logger.info("User '%s' updated record #%d.", request.user.username, pk)
            return redirect('website:home')
    else:
        form = RecordForm(instance=customer_record)

    return render(request, 'update_record.html', {'form': form})