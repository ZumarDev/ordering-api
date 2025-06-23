#!/bin/bash
cd ~/projects/ordering-api

# Venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Migrations va collectstatic
cp .env.prod .env
export $(cat .env | xargs)
python manage.py migrate
python manage.py collectstatic --noinput

# Gunicorn restart
sudo systemctl restart ordering-api.service
