# ~*~ coding: utf-8 ~*~


"""
fedora-software
Unit tests - test.py

This module tests fedora-software's in order to ensure that the various
parts (units) behave as expected
"""

from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.template.loader import render_to_string
from django.test import TestCase
from fedora_software.views import HomeView
from fedora_software.models import Component, FeaturedApp


class HelperSuite(TestCase):
    """
    Suite which shares common helper methods between various test
    cases.
    """
    def create_sample_component(self, type_id, type_="desktop"):
        """
        Helper method created in order to populate the table
        'Component'
        """
        sample_component = Component()
        sample_component.type = type_
        sample_component.type_id = type_id
        sample_component.save()
        return sample_component

    def create_sample_featured_app(self, component):
        """
        Helper method created in order to populate the table
        'FeaturedApp'
        """
        sample_featured_app = FeaturedApp()
        sample_featured_app.component = component
        sample_featured_app.save()
        return sample_featured_app


class ViewTest(HelperSuite):
    """
    Suite of unit tests performed against views
    """
    def test_root_url_resolves_to_home(self):
        """
        Tests that the home page's url is correctly resolved
        """
        resolved = resolve("/")
        self.assertEqual(type(resolved.func), type(HomeView.as_view()))

    def test_home_page_returns_correct_html(self):
        """
        Tests that the HomeView seems to use the correct template
        """
        # this test should be improved and made more useful
        sample_component = self.create_sample_component(type_id="gimp.desktop")
        self.create_sample_featured_app(component=sample_component)
        response = self.client.get(reverse('home'))
        template_html = render_to_string(
                'home.html',
                {"LANGUAGES": settings.LANGUAGES[:]}
                )
        self.assertAlmostEqual(
                len(response.content.decode())/1000,
                len(template_html)/1000, 
                )


class ModelTest(HelperSuite):
    """
    Suite of unit tests performed against models
    """
    def test_create_component(self):
        """
        Tests the creation of a Component
        """
        first_component = Component()
        first_component.type = "desktop"
        first_component.type_id = "firefox.desktop"
        first_component.save()

        second_component = Component()
        second_component.type = "desktop"
        second_component.type_id = "xchat.desktop"
        second_component.save()

        saved_components = Component.objects.all()
        self.assertEqual(saved_components.count(), 2)

    def test_create_featured_app(self):
        """
        Tests the creation of a FeaturedApp
        """
        sample_component =self.create_sample_component(
                type_id="firefox.desktop"
                )
        first_featured_app = FeaturedApp()
        first_featured_app.component = sample_component
        first_featured_app.save()

        sample_component = self.create_sample_component(
                type_id="ardour.desktop"
                )
        second_featured_app = FeaturedApp()
        second_featured_app.component = sample_component
        second_featured_app.save()

        saved_featured_apps = FeaturedApp.objects.all()
        self.assertEqual(saved_featured_apps.count(), 2)
