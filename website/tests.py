"""
Unit tests for the website (CRM) application.

Covers models, forms, views, and URL routing to ensure
core functionality works correctly.
"""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import resolve, reverse

from .forms import RecordForm, SignUpForm
from .models import Record
from .views import (
    add_record,
    delete_record,
    home,
    logout_user,
    record_detail,
    register_user,
    update_record,
)


# =============================================================================
# Model Tests
# =============================================================================

class RecordModelTest(TestCase):
    """Tests for the Record model."""

    def setUp(self):
        """Create a sample record for use across tests."""
        self.record = Record.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            address='123 Main St',
            city='Springfield',
            state='Illinois',
            zipcode='62704',
        )

    def test_string_representation(self):
        """Record __str__ should return 'first_name last_name'."""
        self.assertEqual(str(self.record), 'John Doe')

    def test_ordering_is_newest_first(self):
        """Records should be ordered by created_at descending."""
        older = self.record
        newer = Record.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            phone='9876543210',
            address='456 Oak Ave',
            city='Shelbyville',
            state='Illinois',
            zipcode='62565',
        )
        records = list(Record.objects.all())
        self.assertEqual(records[0], newer)
        self.assertEqual(records[1], older)

    def test_verbose_names(self):
        """Model Meta should have human-readable verbose names."""
        self.assertEqual(Record._meta.verbose_name, 'customer record')
        self.assertEqual(Record._meta.verbose_name_plural, 'customer records')

    def test_auto_timestamps(self):
        """created_at and updated_at should be set automatically."""
        self.assertIsNotNone(self.record.created_at)
        self.assertIsNotNone(self.record.updated_at)


# =============================================================================
# Form Tests
# =============================================================================

class SignUpFormTest(TestCase):
    """Tests for the SignUpForm."""

    def test_valid_form(self):
        """Form should be valid with matching passwords and required fields."""
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        """Form should be invalid when passwords don't match."""
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'password123A',
            'confirm_password': 'differentpass',
        }
        form = SignUpForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)

    def test_password_too_short(self):
        """Form should reject passwords shorter than 8 characters."""
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'short',
            'confirm_password': 'short',
        }
        form = SignUpForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)


class RecordFormTest(TestCase):
    """Tests for the RecordForm."""

    def test_valid_form(self):
        """Form should be valid with all required fields."""
        data = {
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'email': 'alice@example.com',
            'phone': '5551234567',
            'address': '789 Pine Rd',
            'city': 'Denver',
            'state': 'Colorado',
            'zipcode': '80201',
        }
        form = RecordForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        """Form should be invalid with malformed email."""
        data = {
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'email': 'not-an-email',
            'phone': '5551234567',
            'address': '789 Pine Rd',
            'city': 'Denver',
            'state': 'Colorado',
            'zipcode': '80201',
        }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_uses_explicit_fields(self):
        """RecordForm should use 'fields', not 'exclude', for security."""
        self.assertIsNotNone(RecordForm.Meta.fields)
        self.assertFalse(hasattr(RecordForm.Meta, 'exclude'))


# =============================================================================
# View Tests
# =============================================================================

class AuthenticationViewTest(TestCase):
    """Tests for login, logout, and registration views."""

    def setUp(self):
        """Create a test user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
        )

    def test_home_unauthenticated_shows_login(self):
        """Home page should show login form for unauthenticated users."""
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')

    def test_home_authenticated_shows_records(self):
        """Home page should show records table for authenticated users."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Customer Records')

    def test_login_valid_credentials(self):
        """POST with valid credentials should log in and redirect."""
        response = self.client.post(
            reverse('website:home'),
            {'username': 'testuser', 'password': 'testpassword123'},
        )
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_credentials(self):
        """POST with invalid credentials should redirect with error."""
        response = self.client.post(
            reverse('website:home'),
            {'username': 'testuser', 'password': 'wrongpassword'},
        )
        self.assertEqual(response.status_code, 302)

    def test_logout_requires_post(self):
        """GET requests to logout should be rejected (405)."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('website:logout'))
        self.assertEqual(response.status_code, 405)

    def test_logout_post_redirects(self):
        """POST to logout should redirect to home."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('website:logout'))
        self.assertEqual(response.status_code, 302)

    def test_register_get(self):
        """GET to register should show the signup form."""
        response = self.client.get(reverse('website:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')


class RecordCRUDViewTest(TestCase):
    """Tests for record CRUD operations."""

    def setUp(self):
        """Create a test user and sample record."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
        )
        self.client.login(username='testuser', password='testpassword123')
        self.record = Record.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            address='123 Main St',
            city='Springfield',
            state='Illinois',
            zipcode='62704',
        )

    def test_record_detail_view(self):
        """Should display record details for authenticated users."""
        response = self.client.get(
            reverse('website:record', kwargs={'pk': self.record.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')

    def test_record_detail_not_found(self):
        """Should return 404 for non-existent record."""
        response = self.client.get(
            reverse('website:record', kwargs={'pk': 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_add_record_get(self):
        """GET should show the add record form."""
        response = self.client.get(reverse('website:add_record'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add New Record')

    def test_add_record_post(self):
        """POST with valid data should create a record and redirect."""
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'phone': '9876543210',
            'address': '456 Oak Ave',
            'city': 'Shelbyville',
            'state': 'Illinois',
            'zipcode': '62565',
        }
        response = self.client.post(reverse('website:add_record'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Record.objects.filter(first_name='Jane').exists())

    def test_update_record_get(self):
        """GET should show the update form pre-populated with data."""
        response = self.client.get(
            reverse('website:update_record', kwargs={'pk': self.record.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')

    def test_delete_record_post(self):
        """POST should delete the record and redirect."""
        response = self.client.post(
            reverse('website:delete_record', kwargs={'pk': self.record.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Record.objects.filter(pk=self.record.pk).exists())

    def test_delete_record_get_rejected(self):
        """GET requests to delete should be rejected (405)."""
        response = self.client.get(
            reverse('website:delete_record', kwargs={'pk': self.record.pk})
        )
        self.assertEqual(response.status_code, 405)

    def test_search_records(self):
        """Search should filter records by name."""
        response = self.client.get(reverse('website:home'), {'q': 'John'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')

    def test_unauthenticated_redirect(self):
        """CRUD views should redirect unauthenticated users."""
        self.client.logout()
        response = self.client.get(reverse('website:add_record'))
        self.assertEqual(response.status_code, 302)


# =============================================================================
# URL Tests
# =============================================================================

class URLResolutionTest(TestCase):
    """Tests that all URL patterns resolve to the correct views."""

    def test_home_url(self):
        self.assertEqual(resolve(reverse('website:home')).func, home)

    def test_logout_url(self):
        self.assertEqual(resolve(reverse('website:logout')).func, logout_user)

    def test_register_url(self):
        self.assertEqual(resolve(reverse('website:register')).func, register_user)

    def test_record_url(self):
        url = reverse('website:record', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, record_detail)

    def test_add_record_url(self):
        self.assertEqual(resolve(reverse('website:add_record')).func, add_record)

    def test_delete_record_url(self):
        url = reverse('website:delete_record', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, delete_record)

    def test_update_record_url(self):
        url = reverse('website:update_record', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, update_record)
