#!/bin/bash
gunicorn --pythonpath src --bind 0.0.0.0:5000 --workers 3 wsgi:app
