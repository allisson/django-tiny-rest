# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import tiny_rest

requires = [
    'six',
    'django-qurl',
    'python-status',
]

setup(
    name='django-tiny-rest',
    version=tiny_rest.__version__,
    author=tiny_rest.__author__,
    author_email=tiny_rest.__author_email__,
    packages=find_packages(),
    license='MIT',
    description=tiny_rest.__description__,
    url='https://github.com/allisson/django-tiny-rest',
    keywords='Django, REST, API',
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],
)
