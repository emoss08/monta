# -*- coding: utf-8 -*-
from django.test import TestCase

from monta_user.factories.user import MontaUserFactory, ProfileFactory


class MontaUserTest(TestCase):
    def setUp(self):
        self.user = MontaUserFactory.create()
        self.profile = ProfileFactory.create(user=self.user)

    def test_user_is_created(self):
        """
        Test that the user is created
        """
        self.assertTrue(self.user)

    def test_user_has_profile(self):
        """
        Test that the user has a profile
        """
        self.assertTrue(self.profile)

    def test_user_has_organization(self):
        """
        Test that the user has an organization
        """
        self.assertTrue(self.profile.organization)

    def test_user_has_job_title(self):
        """
        Test that the user has a job title
        """
        self.assertTrue(self.profile.title)
