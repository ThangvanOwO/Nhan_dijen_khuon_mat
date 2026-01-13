#!/usr/bin/env python3
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')

import django
django.setup()

from portal.models import Class, Student, Session, Attendance

print('=== DATABASE STATUS ===')
print(f'Classes: {Class.objects.count()}')
print(f'Students: {Student.objects.count()}')  
print(f'Sessions: {Session.objects.count()}')
print(f'Attendances: {Attendance.objects.count()}')
print()

print('=== CLASSES ===')
for c in Class.objects.all():
    print(f'  {c.class_id} - {c.name}')
print()

print('=== SESSIONS ===')
for s in Session.objects.all()[:10]:
    print(f'  {s.session_id} - {s.topic} - {s.date}')
print()

print('=== STUDENTS ===')
for st in Student.objects.all()[:10]:
    print(f'  {st.student_id} - {st.full_name} - Class: {st.class_obj}')
print()

print('=== ATTENDANCES ===')
for a in Attendance.objects.all()[:10]:
    print(f'  {a.student.full_name} @ {a.session.session_id} - {a.status}')
