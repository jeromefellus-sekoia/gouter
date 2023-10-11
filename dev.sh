#!/bin/sh

yarn start &

export GOOGLE_CLIENT_ID=50234913226-lh7vje4l45t4ifu5jv9ujetlojlfqq87.apps.googleusercontent.com

exec uvicorn api.main:app --host 127.0.0.1 $OPTS --port 8001 --reload
