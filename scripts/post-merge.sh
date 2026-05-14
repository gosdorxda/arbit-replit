#!/bin/bash
set -e

python -c "import flask, flask_sqlalchemy, gunicorn, psycopg2, requests, sqlalchemy" && echo "All dependencies OK"
