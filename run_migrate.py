#!/usr/bin/env python
"""Script to run migrations"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')

import django
django.setup()

from django.core.management import call_command

print("Creating migrations...")
call_command('makemigrations', 'portal', verbosity=2)

print("\nApplying migrations...")
call_command('migrate', verbosity=2)

print("\nDone!")
