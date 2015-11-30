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
from django.test import RequestFactory
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

    def mock_as_view(self, view, request, *args, **kwargs):
        """
        This is a mock of "as_view()". Returns an instance of view.
        """
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view


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
        sample_component = self.create_sample_component(type_id="gimp.desktop")
        self.create_sample_featured_app(component=sample_component)
        response = self.client.get(reverse('home'))
        template_html = render_to_string(
                'home.html',
                {"LANGUAGES": settings.LANGUAGES[:]}
                )
        self.assertAlmostEqual(
                len(response.content.decode()),
                len(template_html),
                delta=150
                )
    
    def test_homeview_context_contains_a_featured_app(self):
        """
        Tests that HomeView's get_context_data returns a FeaturedApp
        """
        sample_component = self.create_sample_component(type_id="gimp.desktop")
        sample_featuredapp = self.create_sample_featured_app(
                             component=sample_component)
        request = RequestFactory().get("/")
        view = HomeView(template_name="home.html")
        view = self.mock_as_view(view, request)

        context = view.get_context_data()
        
        self.assertIn(sample_featuredapp, context.values())

    def test_homeview_context_contains_only_one_featured_app(self):
        """
        Tests that HomeView's get_context_data returns only one FeaturedApp
        """
        component_one = self.create_sample_component(type_id="gimp.desktop")
        component_two = self.create_sample_component(type_id="xterm.desktop")
        featured_one = self.create_sample_featured_app(component_one)
        featured_two = self.create_sample_featured_app(component_two)
        request = RequestFactory().get("/")
        view = HomeView()
        view = self.mock_as_view(view, request)

        context = view.get_context_data()
        context_values = context.values()

        if featured_one in context_values:
            self.assertNotIn(featured_two, context_values)
        else:
            self.assertNotIn(featured_one, context_values)


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

    def test_component_get_absolute_url(self):
        """
        Tests Component's method 'get_absolute_url'

        If the Component's type equals to 'desktop', it should return a
        valid url.

        If the Component's type doesn't equal to 'desktop', it should
        raise an Exception.
        """
        first_component = self.create_sample_component(
                type_id="sample.desktop", 
                type_="desktop"
                )
        self.assertEqual(first_component.get_absolute_url(), "/apps/sample")

        second_component = self.create_sample_component(
                type_id="test.abstract",
                type_="abstract"
                )
        self.assertRaises(Exception, second_component.get_absolute_url)

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
