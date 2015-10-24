#!/bin/bash
coverage run --source=tiny_rest testproject/manage.py test tiny_rest blog
coverage report -m
