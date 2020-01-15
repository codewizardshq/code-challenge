#!/bin/sh
set -e
cd "/var/www/flaskapp/"
gunicorn -b 0.0.0.0:5000 app:app