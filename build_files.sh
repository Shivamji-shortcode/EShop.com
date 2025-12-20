#!/bin/bash

echo "Build Start"

# Use Python from Vercel runtime
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Clear and collect all static files to STATIC_ROOT
python3 manage.py collectstatic --noinput --clear

echo "Build End"
