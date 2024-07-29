#!/usr/bin/env bash

docker exec sandbox-api-container python manage.py makemigrations $@
