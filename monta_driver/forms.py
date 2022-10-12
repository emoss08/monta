# -*- coding: utf-8 -*-
"""
COPYRIGHT 2022 MONTA

This file is part of Monta.

Monta is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Monta is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Monta.  If not, see <https://www.gnu.org/licenses/>.
"""
# Standard Library Imports
from typing import Type

# Core Django Imports
from django import forms

# Third Party Imports
from localflavor.us.forms import USStateSelect, USZipCodeField

# Core Monta Imports
from monta_driver.models import Driver, DriverProfile, DriverContact


class AddDriverForm(forms.ModelForm):
    """
    Form for adding a driver to the database.

    Args:
        forms.ModelForm (ModelForm): Django ModelForm class.

    Returns:
        None
    """

    first_name = forms.CharField(
        max_length=255,
        help_text="First name of the driver",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter First Name",
                "class": "form-control form-control-solid",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=255,
        help_text="Last name of the driver",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Last Name",
                "class": "form-control form-control-solid",
            }
        ),
    )

    class Meta:
        """
        Metaclass for AddDriverForm.
        """

        model: Type[Driver] = Driver
        fields = ("first_name", "last_name")


class AddDriverProfileForm(forms.ModelForm):
    """
    Form for adding a driver profile to the database.

    Args:
        forms.ModelForm (ModelForm): Django ModelForm class.

    Returns:
        None
    """

    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
    )
    profile_picture = forms.ImageField(required=False)
    address_line_1 = forms.CharField(
        max_length=100,
        help_text="Address for the driver",
    )
    address_line_2 = forms.CharField(
        max_length=100,
        help_text="Address for the driver",
        required=False,
    )
    city = forms.CharField(max_length=100, help_text="City for the driver")
    state = USStateSelect()
    zip_code = USZipCodeField()
    license_number = forms.CharField(
        max_length=100, help_text="License Number for driver"
    )
    license_state = forms.CharField(max_length=2, help_text="License State for driver")
    license_expiration = forms.DateField(help_text="License Expiration for driver")
    is_hazmat = forms.BooleanField(help_text="Is Hazmat for driver")
    is_tanker = forms.BooleanField(help_text="Is Tanker for driver")
    is_double_triple = forms.BooleanField(help_text="Is Double Triple for driver")
    is_passenger = forms.BooleanField(help_text="Is Passenger for driver")

    class Meta:
        model: Type[DriverProfile] = DriverProfile
        fields = (
            "driver",
            "profile_picture",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "zip_code",
            "license_number",
            "license_state",
            "license_expiration",
            "is_hazmat",
            "is_tanker",
            "is_double_triple",
            "is_passenger",
        )


class AddDriverContactForm(forms.ModelForm):
    driver = forms.ModelChoiceField(queryset=Driver.objects.all())
    contact_name = forms.CharField(
        max_length=255, help_text="Contact name for the driver"
    )
    contact_email = forms.EmailField(
        max_length=255, help_text="Contact email for the driver"
    )
    contact_phone = forms.CharField(
        max_length=10, help_text="Contact phone for the driver"
    )
    is_primary = forms.BooleanField(help_text="Is Primary for driver", required=False)
    is_emergency = forms.BooleanField(
        help_text="Is Emergency for driver", required=False
    )

    class Meta:
        model: Type[DriverContact] = DriverContact
        fields: list[str] = [
            "driver",
            "contact_name",
            "contact_email",
            "contact_phone",
            "is_primary",
            "is_emergency",
        ]


DriverContactFormset = forms.inlineformset_factory(
    Driver,
    DriverContact,
    form=AddDriverContactForm,
    extra=2,
)

DriverProfileFormset = forms.inlineformset_factory(
    Driver,
    DriverProfile,
    form=AddDriverProfileForm,
)


class UpdateDriverForm(forms.Form):
    """Update the Driver Information"""

    first_name = forms.CharField(max_length=255, help_text="First name of the driver")
    middle_name = forms.CharField(
        max_length=255, help_text="Middle name of the driver", required=False
    )
    last_name = forms.CharField(max_length=255, help_text="Last name of the driver")
    profile_picture = forms.ImageField(required=False)
    address_line_1 = forms.CharField(max_length=100, help_text="Address for the driver")
    address_line_2 = forms.CharField(
        max_length=100, help_text="Address for the driver", required=False
    )
    city = forms.CharField(max_length=100, help_text="City for the driver")
    state = USStateSelect()
    zip_code = USZipCodeField()
    license_number = forms.IntegerField(help_text="License Number for driver")
    license_state = forms.CharField(max_length=2, help_text="License State for driver")
    license_expiration = forms.DateField(help_text="License Expiration for driver")
    is_hazmat = forms.BooleanField(help_text="Is Hazmat for driver")
    is_tanker = forms.BooleanField(help_text="Is Tanker for driver")
    is_double_triple = forms.BooleanField(help_text="Is Double Triple for driver")
    is_passenger = forms.BooleanField(help_text="Is Passenger for driver")

    def save(self, driver: Driver) -> None:
        """
        Save the Driver Information

        Args:
            driver (Driver): Driver to update

        Returns:
            None
        """
        driver.first_name = self.cleaned_data["first_name"]
        driver.middle_name = self.cleaned_data["middle_name"]
        driver.last_name = self.cleaned_data["last_name"]
        driver.save()

        driver_profile = driver.profile
        driver_profile.profile_picture = self.cleaned_data["profile_picture"]
        driver_profile.address_line_1 = self.cleaned_data["address_line_1"]
        driver_profile.address_line_2 = self.cleaned_data["address_line_2"]
        driver_profile.city = self.cleaned_data["city"]
        driver_profile.state = self.cleaned_data["state"]
        driver_profile.zip_code = self.cleaned_data["zip_code"]
        driver_profile.license_number = self.cleaned_data["license_number"]
        driver_profile.license_state = self.cleaned_data["license_state"]
        driver_profile.license_expiration = self.cleaned_data["license_expiration"]
        driver_profile.is_hazmat = self.cleaned_data["is_hazmat"]
        driver_profile.is_tanker = self.cleaned_data["is_tanker"]
        driver_profile.is_double_triple = self.cleaned_data["is_double_triple"]
        driver_profile.is_passenger = self.cleaned_data["is_passenger"]
        driver_profile.save()


class SearchForm(forms.Form):
    """
    Search Form
    """

    query = forms.CharField(
        label="Search for Driver",
        max_length=255,
        help_text="Search for a driver",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search for a driver",
                "class": "form-control form-control-solid",
            }
        ),
    )


class LicenseValidateForm(forms.Form):
    """
    License Validate Form
    """

    license_number = forms.CharField(
        max_length=100, help_text="License Number for driver"
    )
