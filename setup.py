#!/usr/bin/env python3
# encoding: utf-8

from setuptools import setup, find_packages

setup(
    name         = "fedora-software",
    version      = '0.1',
    description  = "Web interface to Fedora Software database",
    author       = "Jozef Mlích & Jakub Dorňák",
    author_email = "jmlich@redhat.com, jdornak@redhat.com",
    url          = "https://github.com/misli/fedora-software",
    packages     = find_packages(),
    scripts      = ['fedora-software-manage'],
    data_files   = [('/etc/bash_completion.d', ['fedora-software.bash'])],
)
