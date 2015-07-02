# ~*~ coding: utf-8 ~*~
#!/usr/bin/env python


"""
fedora-software
Functional tests - fedora-software-fixtures.py

This module is responsible for building the fixtures needed by the test
suite.
"""


import os
from unipath import Path


def _prepare_fixtures_dir(path):
    """
    Creates the fixtures' directory if it doesn't already exist.
    """
    if not(os.path.exists(path)):
        os.mkdir(path)

def _prepare_tables_string(tables_list):
    """
    Writes down the tables' names, as requested by the function
    'build_command'.
    """
    tables_string = ""
    for table in tables_list:
        tables_string = "{0} {1}".format(tables_string, table)
    return tables_string

def _build_command(tables, fixtures_path, fixture_name):
    """
    Builds the appropriate command for generating the fixture.
    """
    command = "python manage.py dumpdata{0} --indent=4 > {1}/{2}".format(
            tables, fixtures_path, fixture_name
            )
    return command

def create_fixtures(tables_list, project_path, fixtures_path, fixture_name):
    """
    Creates fixtures from the existing database.

    'tables_list' should be an iterable and contain items in format
     'app.table', rappresented by strings.
    'project_path' should be the dir which contains the apps.
    'fixtures_path' is the path where the fixtures are stored.
    'fixture_name' is the name of the output file.
    """
    tables = _prepare_tables_string(tables_list)
    _prepare_fixtures_dir(fixtures_path)
    command = _build_command(tables, fixtures_path, fixture_name)
    os.chdir(project_path)
    os.system(command)
    return 0

def create_testing_fixtures(project_path):
    """
    Creates the fixtures needed by the tests of fedora-software.
    """
    functional_testing_tables = [
            "fedora_software.FeaturedApp", 
            "fedora_software.Component"
            ]
    app_path = project_path.child("fedora_software")
    fixtures_path = app_path.child("fixtures")
    functional_testing_fixture = "fedora_software_testing.json"
    return create_fixtures(
            functional_testing_tables,
            project_path,
            fixtures_path,
            functional_testing_fixture
            )

if __name__ == "__main__":
    project_path = Path(os.path.abspath(__file__)).ancestor(2)
    print("Creating fixtures for testing...")
    exit_code = create_testing_fixtures(project_path)
    if exit_code == 0:
        print ("Completed!")
