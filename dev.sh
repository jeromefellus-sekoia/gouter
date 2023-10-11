#!/bin/sh

yarn start &

export GOOGLE_CLIENT_ID="4862407941-gli3asais585k29vjbnlvnh45sanjvme.apps.googleusercontent.com"

exec uvicorn api.main:app --host 127.0.0.1 $OPTS --port 8001 --reload
