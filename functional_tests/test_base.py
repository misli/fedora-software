# ~*~ coding: utf-8 ~*~


"""
fedora-software
Functional tests - test_base.py

This module tests fedora-software's main functionality by user's point
of view.
"""


import os
from selenium import webdriver
from unipath import Path
from django.test import TestCase
from fedora_software.models import FeaturedApp


class FunctionalTest(TestCase):
    """
    Suite of Acceptance tests.
    """
    fixtures = ["fedora_software_testing.json"]
    def setUp(self):
        """
        Sets up a testing environment.
        """
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.get("http://localhost:8000")

    def tearDown(self):
        """
        Cleans the environment before testing.
        """
        self.browser.quit()

    def test_if_fedora_software_is_reachable(self):
        """
        Checks if the browser is able to reach fedora-software
        """
        # Kathe is the user of our example. She has heard about a new
        # exciting software for her Fedora's workstation. She visits it
        # via Firefox.

        # She notices the page title mention 'Fedora-Software'
        self.assertIn("Welcome to Fedora Software", self.browser.title)

    def test_if_featured_apps_are_displayed_correctly(self):
        """
        Tests if the featured apps are correctly displayed on the home
        """
        # She also see a section which seems to contain some packages
        # listed as 'Featured apps'.
        featured_header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual("Featured apps", featured_header_text)

        # She notices that there some apps appears randomly
        app_link = self.browser.find_element_by_id("featured_app_href")
        app_link = app_link.get_attribute("href")
        app_pkgname = "None"

        i = 0
        for app in FeaturedApp.objects.all():
            app_name_from_link = app_link.split("/apps/")[1]
            if app_name_from_link in app.component.type_id:
                app_type_id = app.component.type_id
                break

        self.assertIn(app_name_from_link, app_type_id)

    def test_if_carousel_displays_a_valid_image(self):
        """
        Test if the image displayed by 'carousel-featured' exists
        """
        # She admires the big logo of the 'FeaturedApp' which is
        # currently displayed.
        carousel = self.browser.find_element_by_id("carousel-featured")

        carousel_html = carousel.value_of_css_property("background")
        carousel_image = carousel_html.split('url("')[1]
        carousel_path = carousel_image.split('") no-repeat')[0][1:]
        project_path = Path(__file__).ancestor(2)
        fedorasoftware_app_path = project_path.child("fedora_software")
        carousel_file = os.path.join(
                fedorasoftware_app_path,
                carousel_path
                )

        self.assertTrue(os.path.exists(carousel_file))

