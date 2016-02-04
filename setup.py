#!/usr/bin/env python

from setuptools import setup

setup(
    name='geowatch-util',
    version='0.0.2',
    install_requires=[],
    author='GeoWatch Developers',
    author_email='geowatch.dev@gmail.com',
    license='BSD License',
    url='https://github.com/geowatch/geowatch-util/',
    keywords='python gis geowatch',
    description='A python utility library for GeoWatch',
    long_description=open('README.rst').read(),
    download_url="https://github.com/geowatch/geowatch-util/zipball/master",
    #py_modules=["geowatchutil"],
    packages=[
        "geowatchutil",
        "geowatchutil.broker",
        "geowatchutil.buffer",
        "geowatchutil.channel",
        "geowatchutil.client",
        "geowatchutil.codec",
        "geowatchutil.mapping",
        "geowatchutil.node",
        "geowatchutil.store",
        "geowatchutil.tests"],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
