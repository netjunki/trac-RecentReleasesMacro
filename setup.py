#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from setuptools import setup

setup(
    name = 'TracRecentReleasesMacro',
    version = '0.1',
    packages = ['recentreleases'],
    package_data={ 'recentreleases' : [ 'templates/*.html', 'htdocs/*.*' ] },
    author = "Benjamin Lau",
    description = "Macro to add a form to a wiki page for creating new pages",
    license = "BSD",
    keywords = "trac plugin macro wiki",
    url = "https://github.com/netjunki/trac-RecentReleasesMacro",
    classifiers = [
        'Framework :: Trac',
    ],
    
    entry_points = {
        'trac.plugins': [
            'recentreleases.macro = recentreleases.macro',
        ],
    },
)
