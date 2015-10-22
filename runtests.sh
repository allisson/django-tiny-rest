#!/bin/bash
coverage run --source=tiny_rest testproject/manage.py test
coverage report -m