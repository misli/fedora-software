fedora-software
===============

Web interface to Fedora Software database


Installation
------------

Install appstream-data, gnome-software and httpd stuff:

    dnf install appstream-data gnome-software httpd mod_wsgi python-django python-openid python-django-fas

Install the package:

    python setup.py install

Initialize database:

    fedora-software-manage syncdb

Import components form appstream-data (takes a while)

    fedora-software-manage importcomponents [ <path to xml.gz file> ]

Import featured apps form gnome-software

    fedora-software-manage importteaturedapps [ <path to ini file> ]

Collect static files

    fedora-software-manage collectstatic

Copy and check httpd configuration

    cp /usr/lib/fedora-software/httpd/fedora-software.conf \
       /etc/httpd/conf.d/

Ensure that apache is able to write to the database:

    chgrp -R apache /var/lib/fedora-software/data
    chmod -R g+w    /var/lib/fedora-software/data

Restart httpd server

    service httpd restart


Development instance
--------------------

Install appstream-data, gnome-software and httpd stuff:

    dnf install appstream-data gnome-software httpd mod_wsgi python-django

Initialize database:

    ./manage.py syncdb

Import components form appstream-data (takes a while)

    ./manage.py importcomponents [ <path to xml.gz file> ]

Import featured apps form gnome-software

    ./manage.py importteaturedapps [ <path to ini file> ]

Run development server:

    ./manage.py runserver

Note that management instance by default runs with DEBUG=True.
To disable debug mode set environment variable DEBUG to '':

    DEBUG='' ./manage.py runserver


Translations
------------

https://docs.djangoproject.com/en/1.8/topics/i18n/translation/

Update translations:

    pushd fedora_software
        django-admin makemessages -l cs
        vim locale/cs/LC_MESSAGES/django.po
        django-admin compilemessages
    popd

The translations could be done online at fedora zanata.

https://fedora.zanata.org/project/view/fedora-software


Test Suite
------------
An automated test suite is currently in development state.
If you want to try it, please follow these steps.

Create a development instance of fedora-software.

Install the browser Mozilla Firefox via dnf:

    dnf install firefox

Install 'selenium' and 'unipath' via pip or dnf:

    pip install selenium unipath
    dnf install python-selenium python-unipath

Create the testing fixtures retreiving data from your db:

    python bin/fedora-software-fixtures.py

Run the development server:

    ./manage.py runserver

Run the full test suite:

    ./manage.py test
