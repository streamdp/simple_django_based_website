#!/bin/bash
pkill gunicorn 
gunicorn -c /etc/gunicorn.d/django_conf.py ask.wsgi:application > /dev/null 2>&1 &
