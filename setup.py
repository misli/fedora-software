#!/usr/bin/env python3
# encoding: utf-8

import os
from setuptools import setup, find_packages

def files(package, paths):
    skip = len(package)+1
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(os.path.join(package, path)):
            for filename in filenames:
                yield os.path.join(dirpath, filename)[skip:]


setup(
    name         = "fedora-software",
    version      = '0.1',
    description  = "Web interface to Fedora Software database",
    author       = "Jozef Mlích & Jakub Dorňák",
    author_email = "jmlich@redhat.com, jdornak@redhat.com",
    url          = "https://github.com/misli/fedora-software",
    packages     = find_packages(),
    package_data = {
        'fedora_software': list(files('fedora_software', ['templates', 'static'])),
    },
    scripts      = ['bin/fedora-software-manage'],
    data_files   = [
        ('/etc/bash_completion.d', ['conf/bash_completion.d/fedora-software.bash']),
        ('/usr/lib/fedora-software/httpd', ['conf/httpd/fedora-software.conf']),
        ('/var/lib/fedora-software/data', []),
        ('/var/lib/fedora-software/htdocs', ['fedora_software/wsgi.py']),
        ('/var/lib/fedora-software/htdocs/static', []),
        ('/var/lib/fedora-software/htdocs/media', []),
    ],
)
