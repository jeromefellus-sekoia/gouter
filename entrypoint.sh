#!/bin/sh
exec uvicorn api.main:app --host 0.0.0.0 $OPTS
