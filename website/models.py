"""
Models for the website (CRM) application.

Defines the core data models for customer relationship management,
including the Record model for storing customer contact information.
"""

from django.core.validators import RegexValidator
from django.db import models


class Record(models.Model):
    """
    Represents a customer contact record in the CRM system.

    Stores personal and address information for a single customer,
    along with automatic timestamps for creation and last update.
    """

    # -- Validators ----------------------------------------------------------
    phone_regex = RegexValidator(
        regex=r'^\+?\d{7,15}$',
        message="Phone number must be 7–15 digits, optionally starting with '+'.",
    )

    # -- Timestamps ----------------------------------------------------------
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="created at",
        help_text="Timestamp when the record was first created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="updated at",
        help_text="Timestamp when the record was last modified.",
    )

    # -- Personal Information ------------------------------------------------
    first_name = models.CharField(
        max_length=50,
        verbose_name="first name",
        help_text="Customer's first (given) name.",
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="last name",
        help_text="Customer's last (family) name.",
    )
    email = models.EmailField(
        max_length=100,
        verbose_name="email address",
        help_text="Customer's primary email address.",
    )
    phone = models.CharField(
        max_length=15,
        validators=[phone_regex],
        verbose_name="phone number",
        help_text="Customer's phone number (7–15 digits, optional leading '+').",
    )

    # -- Address Information -------------------------------------------------
    address = models.CharField(
        max_length=100,
        verbose_name="street address",
        help_text="Street address or P.O. box.",
    )
    city = models.CharField(
        max_length=50,
        verbose_name="city",
        help_text="City or locality.",
    )
    state = models.CharField(
        max_length=50,
        verbose_name="state",
        help_text="State, province, or region.",
    )
    zipcode = models.CharField(
        max_length=20,
        verbose_name="ZIP / postal code",
        help_text="ZIP or postal code.",
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "customer record"
        verbose_name_plural = "customer records"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
